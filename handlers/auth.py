import tornado.web
import tornado.auth
import requests
import json
import os
from models.db import get_db_connection, create_user, get_user_by_github_id

# Try to import and load dotenv, but continue without it if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        user_cookie = self.get_secure_cookie("user")
        user = None
        if user_cookie:
            try:
                user = json.loads(user_cookie)
                self.redirect("/dashboard")
                return
            except:
                pass
        
        self.render("login.html", user=user)

class GitHubAuthHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument("code", None)
        if not code:
            # Redirect to GitHub OAuth
            github_client_id = os.getenv("GITHUB_CLIENT_ID", "")
            # Use the callback URL from environment variable
            redirect_uri = os.getenv("GITHUB_CALLBACK_URL", f"{self.request.protocol}://{self.request.host}/complete/github/")
            github_url = f"https://github.com/login/oauth/authorize?client_id={github_client_id}&redirect_uri={redirect_uri}&scope=user:email"
            self.redirect(github_url)
        else:
            # Handle callback
            self.exchange_code_for_token(code)
    
    def exchange_code_for_token(self, code):
        client_id = os.getenv("GITHUB_CLIENT_ID", "")
        client_secret = os.getenv("GITHUB_CLIENT_SECRET", "")
        # Use the callback URL from environment variable
        redirect_uri = os.getenv("GITHUB_CALLBACK_URL", f"{self.request.protocol}://{self.request.host}/complete/github/")
        
        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri
        }
        
        headers = {"Accept": "application/json"}
        response = requests.post(token_url, data=token_data, headers=headers)
        
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info.get("access_token")
            
            if access_token:
                self.get_user_info(access_token)
            else:
                self.redirect("/login?error=token_failed")
        else:
            self.redirect("/login?error=auth_failed")
    
    def get_user_info(self, access_token):
        # Get user info from GitHub API
        user_url = "https://api.github.com/user"
        headers = {"Authorization": f"token {access_token}"}
        
        response = requests.get(user_url, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            
            # Create or update user in database
            user = create_user(
                github_id=user_data["id"],
                username=user_data["login"],
                email=user_data.get("email", ""),
                avatar_url=user_data.get("avatar_url", "")
            )
            
            if user:
                # Set secure cookie
                user_cookie = json.dumps({
                    "id": user["id"],
                    "github_id": user["github_id"],
                    "username": user["username"],
                    "avatar_url": user["avatar_url"]
                })
                self.set_secure_cookie("user", user_cookie)
                self.redirect("/dashboard")
            else:
                self.redirect("/login?error=user_creation_failed")
        else:
            self.redirect("/login?error=user_info_failed")

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")