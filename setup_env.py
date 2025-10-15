import os

def setup_environment():
    print("Setting up environment variables...")
    
    # Get GitHub OAuth credentials
    print("\n=== GitHub OAuth Configuration ===")
    client_id = input("Enter your GitHub OAuth Client ID: ").strip()
    client_secret = input("Enter your GitHub OAuth Client Secret: ").strip()
    
    # Set default callback URL
    default_callback = "http://localhost:8888/complete/github/"
    print(f"\nUsing default callback URL: {default_callback}")
    print("Make sure this matches your GitHub OAuth app settings!")
    
    # Create .env file content
    env_content = f"""# GitHub OAuth Configuration
GITHUB_CLIENT_ID={client_id}
GITHUB_CLIENT_SECRET={client_secret}
GITHUB_CALLBACK_URL={default_callback}

# App Configuration
COOKIE_SECRET=your_secure_cookie_secret_here  # Change this to a secure random string
PORT=8888
"""
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file created successfully!")
    print("\nNext steps:")
    print("1. Make sure your GitHub OAuth app has the following settings:")
    print(f"   - Homepage URL: http://localhost:8888")
    print(f"   - Authorization callback URL: {default_callback}")
    print("2. Restart your application for the changes to take effect")

if __name__ == "__main__":
    setup_environment()
