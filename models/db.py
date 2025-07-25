import sqlite3
import os
from datetime import datetime

# Try to import and load dotenv, but continue without it if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not available, using default environment variables")

def get_db_connection():
    db_path = os.environ.get('DATABASE_PATH', 'quickmeet.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Read schema from file
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
        schema = f.read()
    
    # Execute schema script
    conn.executescript(schema)
    
    # Migration for max_applicants
    cursor.execute("PRAGMA table_info(events)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'max_applicants' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN max_applicants INTEGER DEFAULT NULL")
    conn.commit()
    
    conn.commit()
    cursor.close()
    conn.close()

def create_user(github_id, username, email, avatar_url):
    """Create or update a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE github_id = ?", (github_id,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        # Update existing user
        cursor.execute("""
            UPDATE users 
            SET username = ?, email = ?, avatar_url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE github_id = ?
        """, (username, email, avatar_url, github_id))
        user_id = existing_user["id"]
    else:
        # Create new user
        cursor.execute("""
            INSERT INTO users (github_id, username, email, avatar_url)
            VALUES (?, ?, ?, ?)
        """, (github_id, username, email, avatar_url))
        user_id = cursor.lastrowid
    
    conn.commit()
    
    # Return user data
    if user_id:
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(user) if user else None
    else:
        cursor.close()
        conn.close()
        return None

def get_user_by_github_id(github_id):
    """Get user by GitHub ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE github_id = ?", (github_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return dict(user) if user else None

def create_event(event_id, title, description, location, created_by, max_applicants=None):
    """Create a new event"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (id, title, description, location, max_applicants, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (event_id, title, description, location, max_applicants, created_by))
    conn.commit()
    cursor.close()
    conn.close()
    return get_event_by_id(event_id)

def get_event_by_id(event_id):
    """Get event by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.*, u.username as creator_username, u.avatar_url as creator_avatar
        FROM events e
        JOIN users u ON e.created_by = u.id
        WHERE e.id = ?
    """, (event_id,))
    event = cursor.fetchone()
    cursor.close()
    conn.close()
    return dict(event) if event else None

def get_events_by_user(user_id, created_by=True):
    """Get events created by or participated in by user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if created_by:
        cursor.execute("""
            SELECT e.*, u.username as creator_username
            FROM events e
            JOIN users u ON e.created_by = u.id
            WHERE e.created_by = ?
            ORDER BY e.created_at DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT DISTINCT e.*, u.username as creator_username
            FROM events e
            JOIN users u ON e.created_by = u.id
            JOIN votes v ON e.id = v.event_id
            WHERE v.user_id = ? AND e.created_by != ?
            ORDER BY e.created_at DESC
        """, (user_id, user_id))
    
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(event) for event in events]

def add_time_slot(event_id, slot_datetime):
    """Add a time slot to an event"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO time_slots (event_id, slot_datetime)
        VALUES (?, ?)
    """, (event_id, slot_datetime))
    conn.commit()
    cursor.close()
    conn.close()

def get_time_slots_by_event(event_id):
    """Get all time slots for an event"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM time_slots 
        WHERE event_id = ? 
        ORDER BY slot_datetime
    """, (event_id,))
    slots = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(slot) for slot in slots]

def vote_for_slot(event_id, slot_id, user_id, is_vote=True):
    """Vote for or unvote a time slot"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if is_vote:
        # Add vote (ignore if already exists)
        try:
            cursor.execute("""
                INSERT INTO votes (event_id, time_slot_id, user_id)
                VALUES (?, ?, ?)
            """, (event_id, slot_id, user_id))
        except sqlite3.IntegrityError:
            # Vote already exists, ignore
            pass
    else:
        # Remove vote
        cursor.execute("""
            DELETE FROM votes 
            WHERE event_id = ? AND time_slot_id = ? AND user_id = ?
        """, (event_id, slot_id, user_id))
    
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    
    # Broadcast update via WebSocket
    from handlers.websocket import VoteWebSocketHandler
    VoteWebSocketHandler.broadcast_vote_update(event_id)
    
    return affected_rows > 0

def get_votes_by_event(event_id):
    """Get all votes for an event with user info"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.*, u.username, u.avatar_url
        FROM votes v
        JOIN users u ON v.user_id = u.id
        WHERE v.event_id = ?
        ORDER BY v.created_at
    """, (event_id,))
    votes = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(vote) for vote in votes]

def add_comment(event_id, user_id, comment_text):
    """Add a comment to an event"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO comments (event_id, user_id, comment_text)
        VALUES (?, ?, ?)
    """, (event_id, user_id, comment_text))
    conn.commit()
    cursor.close()
    conn.close()

def get_comments_by_event(event_id):
    """Get all comments for an event"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, u.username, u.avatar_url
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.event_id = ?
        ORDER BY c.created_at
    """, (event_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(comment) for comment in comments]

def finalize_event(event_id, slot_id):
    """Finalize an event with selected time slot"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE events 
        SET finalized_slot_id = ?, is_finalized = 1
        WHERE id = ?
    """, (slot_id, event_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_event(event_id, title, description, location, max_applicants):
    """Update an existing event"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE events
        SET title = ?, description = ?, location = ?, max_applicants = ?
        WHERE id = ?
    """, (title, description, location, max_applicants, event_id))
    conn.commit()
    cursor.close()
    conn.close()
    return get_event_by_id(event_id)
