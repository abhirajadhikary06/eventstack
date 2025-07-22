// (No JS forcibly changes icon/image color in dark mode. Icons/images retain their original appearance.)
// General application JavaScript

// Utility functions
function showNotification(message, type = "info") {
  // Create notification element
  const notification = document.createElement("div");
  notification.className = `fixed top-4 right-4 z-50 p-4 rounded-md shadow-lg transition-all duration-300 ${
    type === "success"
      ? "bg-green-500 text-white"
      : type === "error"
      ? "bg-red-500 text-white"
      : type === "warning"
      ? "bg-yellow-500 text-white"
      : "bg-blue-500 text-white"
  }`;

  notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas ${
              type === "success"
                ? "fa-check"
                : type === "error"
                ? "fa-exclamation-triangle"
                : type === "warning"
                ? "fa-exclamation"
                : "fa-info"
            }"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white/80 hover:text-white">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

  document.body.appendChild(notification);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (notification.parentElement) {
      notification.remove();
    }
  }, 5000);
}

// Handle form submissions with better UX
function handleFormSubmit(form, options = {}) {
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalText = submitBtn.innerHTML;

  // Show loading state
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin mr-2"></i>Loading...`;

  // Reset after timeout or on completion
  const resetButton = () => {
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
  };

  // Reset after 5 seconds as fallback
  setTimeout(resetButton, 5000);

  return resetButton;
}

// Format datetime for display
function formatDateTime(dateTimeString) {
  const date = new Date(dateTimeString);
  return date.toLocaleString("en-US", {
    weekday: "short",
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Copy link to clipboard
function copyEventLink(eventId) {
  const url = `${window.location.origin}/event/${eventId}`;

  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(url)
      .then(() => {
        showNotification("Event link copied to clipboard!", "success");
      })
      .catch(() => {
        fallbackCopyTextToClipboard(url);
      });
  } else {
    fallbackCopyTextToClipboard(url);
  }
}

function fallbackCopyTextToClipboard(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;

  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    const successful = document.execCommand("copy");
    if (successful) {
      showNotification("Event link copied to clipboard!", "success");
    } else {
      showNotification("Failed to copy link", "error");
    }
  } catch (err) {
    showNotification("Failed to copy link", "error");
  }

  document.body.removeChild(textArea);
}

// Initialize tooltips for avatars
function initializeTooltips() {
  const tooltipElements = document.querySelectorAll("[title]");
  tooltipElements.forEach((element) => {
    element.addEventListener("mouseenter", function (e) {
      const tooltip = document.createElement("div");
      tooltip.className =
        "absolute z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg";
      tooltip.textContent = this.getAttribute("title");
      tooltip.style.top = e.pageY - 30 + "px";
      tooltip.style.left = e.pageX - tooltip.offsetWidth / 2 + "px";
      tooltip.id = "tooltip";

      document.body.appendChild(tooltip);
      this.removeAttribute("title");
      this.setAttribute("data-original-title", tooltip.textContent);
    });

    element.addEventListener("mouseleave", function () {
      const tooltip = document.getElementById("tooltip");
      if (tooltip) {
        tooltip.remove();
      }
      this.setAttribute("title", this.getAttribute("data-original-title"));
    });
  });
}

// Initialize when DOM is loaded

function createDarkModeToggle() {
  const toggle = document.createElement("button");
  toggle.id = "dark-mode-toggle";
  toggle.type = "button";
  toggle.setAttribute("aria-label", "Toggle dark mode");
  toggle.style.position = "fixed";
  toggle.style.bottom = "24px";
  toggle.style.right = "24px";
  toggle.style.zIndex = "100";
  toggle.style.background = "#23272f";
  toggle.style.color = "#f3f4f6";
  toggle.style.border = "none";
  toggle.style.borderRadius = "50%";
  toggle.style.width = "48px";
  toggle.style.height = "48px";
  toggle.style.boxShadow = "0 2px 8px rgba(0,0,0,0.15)";
  toggle.style.cursor = "pointer";
  toggle.style.display = "flex";
  toggle.style.alignItems = "center";
  toggle.style.justifyContent = "center";
  toggle.style.fontSize = "1.5rem";
  toggle.innerHTML = '<span id="dark-mode-icon">🌙</span>';
  return toggle;
}

function setDarkMode(enabled) {
  const html = document.documentElement;
  const featureIcons = document.querySelectorAll(".card .feature-icon");
  if (enabled) {
    html.classList.add("dark-mode");
    document.getElementById("dark-mode-icon").textContent = "☀️";
    // Set feature icon backgrounds to dark gray for visibility
    featureIcons.forEach((icon) => {
      icon.style.background = "#23272f";
      icon.style.backgroundColor = "#23272f";
    });
  } else {
    html.classList.remove("dark-mode");
    document.getElementById("dark-mode-icon").textContent = "🌙";
    // Restore feature icon backgrounds to white
    featureIcons.forEach((icon) => {
      icon.style.background = "#fff";
      icon.style.backgroundColor = "#fff";
    });
  }
}

function getDarkModePref() {
  if (localStorage.getItem("darkMode") !== null) {
    return localStorage.getItem("darkMode") === "true";
  }
  // fallback to system preference
  return (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  );
}

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips
  initializeTooltips();

  // Handle form submissions
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function () {
      const resetButton = handleFormSubmit(this);
    });
  });

  // Add dark mode toggle button
  if (!document.getElementById("dark-mode-toggle")) {
    const toggle = createDarkModeToggle();
    document.body.appendChild(toggle);
    // Set initial mode
    setDarkMode(getDarkModePref());
    // Listen for toggle
    toggle.addEventListener("click", function () {
      const enabled = !document.documentElement.classList.contains("dark-mode");
      setDarkMode(enabled);
      localStorage.setItem("darkMode", enabled);
    });
  }
  // Respond to system changes
  if (window.matchMedia) {
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", (e) => {
        if (localStorage.getItem("darkMode") === null) {
          setDarkMode(e.matches);
        }
      });
  }
});

// Mobile menu toggle (if needed)
function toggleMobileMenu() {
  const menu = document.getElementById("mobile-menu");
  if (menu) {
    menu.classList.toggle("hidden");
  }
}

// Smooth scrolling for anchor links
document.addEventListener("click", function (e) {
  if (e.target.matches('a[href^="#"]')) {
    e.preventDefault();
    const targetId = e.target.getAttribute("href").substring(1);
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }
});
