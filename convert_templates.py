#!/usr/bin/env python3
"""
Template Conversion Script
Converts Django-style templates to Tornado-compatible templates
"""

import os
import re
from pathlib import Path

def convert_template(file_path):
    """Convert a single template file from Django to Tornado syntax"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove Django template inheritance
    content = re.sub(r'{% extends "base\.html" %}\s*', '', content)
    content = re.sub(r'{% block title %}(.*?){% end %}\s*', '', content)
    content = re.sub(r'{% block title %}(.*?){% endblock %}\s*', '', content)
    content = re.sub(r'{% block content %}\s*', '', content)
    content = re.sub(r'{% endblock %}\s*', '', content)
    content = re.sub(r'{% end %}\s*', '', content)
    
    # Convert Django template syntax to Tornado
    content = re.sub(r'{{ url_for\([\'"]([^\'"]+)[\'"]\) }}', r'/\1', content)
    content = re.sub(r'{{ url_for\([\'"]([^\'"]+)[\'"], path=[\'"]([^\'"]+)[\'"]\) }}', r'{{ static_url(\2) }}', content)
    content = re.sub(r'{% endif %}', r'{% end %}', content)
    content = re.sub(r'{% endfor %}', r'{% end %}', content)
    content = re.sub(r'{% if ([^%]+) and ([^%]+) %}', r'{% if \1 and \2 %}', content)
    content = re.sub(r'{% if ([^%]+) and ([^%]+) %}', r'{% if \1 and \2 %}', content)
    
    # Convert Django filters to Tornado syntax
    content = re.sub(r'{{ ([^|]+)\|length }}', r'{{ len(\1) }}', content)
    content = re.sub(r'{{ ([^|]+)\|length }}', r'{{ len(\1) }}', content)
    
    # Convert object attribute access to dictionary access
    content = re.sub(r'{{ ([^\.]+)\.([^}]+) }}', r'{{ \1[\2] }}', content)
    
    # Add complete HTML structure
    html_template = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title or "EventStack" }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
      rel="stylesheet" />
    <link rel="stylesheet" href="{{ static_url('css/custom.css') }}" />
    <link rel="icon" type="image/png" href="{{ static_url('images/favicon.png') }}" />
    <script>
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "eventstack-orange": "#D67253",
              "eventstack-orange-dark": "#C5634A",
              "eventstack-orange-light": "#E08B73",
              "eventstack-bg": "#F9F6F1",
              "eventstack-bg-dark": "#F0EDE6",
              github: "#24292e",
              "github-blue": "#0366d6",
              "github-green": "#28a745",
              "github-gray": "#f6f8fa",
            },
          },
        },
      };
    </script>
  </head>
  <body class="bg-eventstack-bg dark:bg-gray-900 text-gray-900 dark:text-white min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <a href="/" class="flex items-center space-x-3 group">
              <div class="w-20 h-20 relative group-hover:scale-110 transition-transform duration-200">
                <img src="{{ static_url('images/image 3.png') }}" alt="EventStack Logo" class="w-full h-full object-contain" />
              </div>
            </a>
          </div>
          <div class="flex items-center space-x-4">
            {% if user %}
            <!-- 🔔 Notification bell -->
            <div class="relative">
              <button id="notificationButton" class="relative p-2 text-gray-400 hover:text-eventstack-orange focus:outline-none">
                <i class="fas fa-bell text-xl"></i>
                {% if upcoming_events and len(upcoming_events) > 0 %}
                <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-4 h-4 rounded-full flex items-center justify-center">
                  {{ len(upcoming_events) }}
                </span>
                {% end %}
              </button>
              <div id="notificationDropdown" class="absolute right-0 mt-2 w-72 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg z-50 hidden">
                <div class="p-3 border-b border-gray-200 dark:border-gray-700 font-medium">
                  Upcoming Events
                </div>
                <ul class="max-h-60 overflow-y-auto">
                  {% if upcoming_events %}
                  {% for event in upcoming_events %}
                  <li class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 transition">
                    <div class="text-sm font-semibold text-eventstack-orange">{{ event['title'] }}</div>
                    <div class="text-xs text-gray-500 dark:text-gray-400">
                      {{ event['start_time'].strftime('%b %d, %Y %I:%M %p') }}
                    </div>
                  </li>
                  {% end %}
                  {% else %}
                  <li class="px-4 py-2 text-sm text-gray-500">No upcoming events</li>
                  {% end %}
                </ul>
              </div>
            </div>

            <a href="/create" class="bg-gray-900 text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition duration-200">
              <i class="fas fa-plus mr-2"></i>New Event
            </a>
            <div class="flex items-center space-x-3">
              <a href="/dashboard" class="group flex items-center space-x-2 hover:bg-gray-100 dark:hover:bg-black px-3 py-2 rounded-lg transition duration-200">
                <img src="{{ user['avatar_url'] }}" alt="Avatar" class="w-8 h-8 rounded-full border-2 border-eventstack-orange" />
                <span class="text-gray-700 dark:text-gray-300 font-medium group-hover:text-black dark:group-hover:text-white username-span">{{ user['username'] }}</span>
              </a>
              <div class="relative group">
                <a href="/logout" class="text-gray-400 hover:text-red-500 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200">
                  <i class="fas fa-sign-out-alt"></i>
                </a>
                <span class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 hidden group-hover:inline-block bg-black text-white text-xs rounded px-2 py-1 whitespace-nowrap z-10 shadow-md transition-opacity duration-200 opacity-0 group-hover:opacity-100">
                  Sign out
                </span>
              </div>
            </div>
            {% else %}
            <a class="btn btn-primary" href="/login">Login</a>
            {% end %}
          </div>
        </div>
      </div>
    </nav>
    
    <!-- Flash Messages -->
    <div class="container mt-4">
      {% if flash_messages %}
        {% for category, message in flash_messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>
        {% end %}
      {% end %}
    </div>

    <!-- Main Content -->
    <main>
      {content}
    </main>

    <!-- Scripts -->
    <script>
      document.getElementById("notificationButton")?.addEventListener("click", function (e) {
        e.stopPropagation();
        const dropdown = document.getElementById("notificationDropdown");
        dropdown?.classList.toggle("hidden");
      });
      document.addEventListener("click", function () {
        document.getElementById("notificationDropdown")?.classList.add("hidden");
      });
    </script>
    <script src="{{ static_url('js/app.js') }}"></script>
  </body>
</html>'''
    
    # Insert the content into the template
    final_content = html_template.replace('{content}', content)
    
    # Write the converted template
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Converted: {file_path}")

def main():
    """Convert all template files"""
    templates_dir = Path("templates")
    
    # Files to convert (excluding already converted ones)
    files_to_convert = [
        "dashboard.html",
        "event.html", 
        "create_event.html",
        "edit_event.html",
        "about.html",
        "privacy.html",
        "support.html"
    ]
    
    for filename in files_to_convert:
        file_path = templates_dir / filename
        if file_path.exists():
            convert_template(file_path)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main() 