import sqlite3

def check_tables():
    conn = sqlite3.connect('quickmeet.db')
    cursor = conn.cursor()
    
    # Get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")
        
        # Show columns for each table
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"  Columns: {', '.join([col[1] for col in columns])}")
    
    conn.close()

if __name__ == "__main__":
    check_tables()
