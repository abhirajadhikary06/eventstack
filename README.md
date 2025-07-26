# 🎉 EventStack

<p align="center">
  <img src="static/images/favicon.png" alt="EventStack Logo" width="120" height="120">
</p>

<p align="center">
  <b>Simplify event planning and coordination with EventStack</b>
</p>

---

## 🧐 What is EventStack?

**EventStack** is a modern and collaborative platform designed to make event planning and coordination effortless. Whether you're organizing team meetings, social hangouts, or community events, EventStack helps you find the perfect time that works for everyone — democratically and transparently.

---

## ⭐ Star this Repository

If you find this project useful, please consider giving it a ⭐ on [GitHub](https://github.com/abhirajadhikary06/eventstack/stargazers)!

[![GitHub stars](https://img.shields.io/github/stars/abhirajadhikary06/eventstack?style=social)](https://github.com/abhirajadhikary06/eventstack/stargazers)

---

## 🚀 Features

### 🔐 Simple Authentication
- Secure sign-in using your GitHub account.
- No password management required.

### 📝 Easy Event Creation
Create events in seconds:
1. Enter a title and description.
2. Add location details.
3. Propose multiple time slots.

### 🗳️ Democratic Time Selection
- Participants vote on preferred slots.
- Real-time voting updates.
- Finalize the most popular option.

### 🔄 Real-Time Updates
- Live data sync using websockets.
- Seamless planning experience.

### 💬 Event Discussion
- Built-in comment thread per event.
- Collaborate, clarify, and coordinate.

### 📱 Responsive UI
- Accessible on desktop, tablet, and mobile.
- Plan events from anywhere.

### 🐳 Docker Support
- Easy to build and deploy via Docker.

---

## 🔧 How It Works

1. **Create an Event** → Add details and time slots.
2. **Share with Participants** → Share the generated event link.
3. **Collect Votes** → Attendees vote on suitable times.
4. **Finalize the Event** → Choose the best slot.
5. **Discuss Details** → Use the built-in comment section.

---

## 💡 Use Cases

- 🧑‍💼 Team Meetings  
- 🍕 Social Gatherings  
- 📚 Study Groups  
- 🛠️ Community Workshops  
- 👨‍👩‍👧 Family Reunions

---

## 🧪 Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Tornado)  
- **Database**: SQLite

---

## 📁 File Structure :-

```bash
eventstack/

├── .vercel/                # Vercel deployment config
├── handlers/               # Tornado request handlers
│   └── __pycache__/        # Compiled Python cache files
├── models/                 # Database and application models
├── static/                 # Static assets
│   ├── css/                # Stylesheets
│   ├── images/             # Icons and images
│   └── js/                 # JavaScript files
├── templates/              # HTML templates (Jinja2)
├── use/                    # Utility modules
│   ├── shareable_links/    # Modules for generating sharable links
│   └── tests/              # Test cases and test utilities
├── .gitignore              # Specifies files/folders to ignore in Git
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container Docker configuration
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies list
├── README.md               # Project overview and documentation
├── LICENSE.md              # Project license (MIT License)
├── CONTRIBUTING.md         # Guidelines for contributing to the project
└── CODE_OF_CONDUCT.md      # Code of conduct for contributors and community
            
```

---

## 🐳 Running with Docker

1. **Build the Docker image:**
   ```sh
   docker compose build
   ```

2. **Start the application:**
   ```sh
   docker compose up
   ```

3. **Access the app:**
   Open your browser and go to [http://localhost:5050](http://localhost:5050)

4. **Stop the application:**
   Press `Ctrl+C` in the terminal, then run:
   ```sh
   docker compose down
   ```

> Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

---

# 👥 Contributors
Thanks to all the amazing people who have contributed to this project:

[![Contributors](https://contrib.rocks/image?repo=abhirajadhikary06/eventstack)](https://github.com/abhirajadhikary06/eventstack/graphs/contributors)


## 🛠️ Contributing

We welcome contributions to make EventStack even better.  
Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

---

## 💬 Code of Conduct

Before participating in our community, please review our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ for better event planning
</p>

