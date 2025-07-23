# 🔗 Shareable Event Links Module

This module provides utilities for generating clean, shareable URLs for events in the EventStack platform. Each link combines a readable event name with a unique ID, allowing users to easily share events while ensuring reliable routing.

---

## 🚀 Features

- Slugifies event names for URL safety
- Appends a short UUID to guarantee uniqueness
- Output format:  
  `https://eventstack.onrender.com/event/hackathon-kickoff-8f2d2a7e`
- Designed to be modular, scalable, and secure

---

## 📦 Folder Structure


## 🚀 Deployment on PythonAnywhere

This project is now deployed at: [https://sushritasingh01.pythonanywhere.com](https://sushritasingh01.pythonanywhere.com)

### 🔧 Setup Steps for Contributors

To deploy or replicate the app on [PythonAnywhere](https://www.pythonanywhere.com/):

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abhirajadhikary06/eventstack.git
   cd eventstack
- 
Configure WSGI file on PythonAnywhere: Inside /var/www/sushritasingh01_pythonanywhere_com_wsgi.py, use:
import sys
import os

path = '/home/sushritasingh01/eventstack'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['FLASK_APP'] = 'app.py'
from app import app as application