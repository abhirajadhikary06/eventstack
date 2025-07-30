"""
Flash message utilities for Tornado web application
"""

class FlashMessages:
    """Simple flash message system for Tornado applications"""
    
    @staticmethod
    def add_message(handler, category, text):
        """Add a flash message to the handler's session/cookies"""
        # Store messages in secure cookie for simplicity
        messages = handler.get_secure_cookie("flash_messages")
        if messages:
            try:
                import json
                messages = json.loads(messages)
            except:
                messages = []
        else:
            messages = []
        
        messages.append({
            'category': category,
            'text': text
        })
        
        import json
        handler.set_secure_cookie("flash_messages", json.dumps(messages))
    
    @staticmethod
    def get_messages(handler):
        """Get and clear flash messages from the handler's session/cookies"""
        messages = handler.get_secure_cookie("flash_messages")
        if messages:
            try:
                import json
                messages = json.loads(messages)
                # Clear messages after retrieving them
                handler.clear_cookie("flash_messages")
                return messages
            except:
                pass
        return []
    
    @staticmethod
    def success(handler, text):
        """Add a success message"""
        FlashMessages.add_message(handler, 'success', text)
    
    @staticmethod
    def error(handler, text):
        """Add an error message"""
        FlashMessages.add_message(handler, 'error', text)
    
    @staticmethod
    def warning(handler, text):
        """Add a warning message"""
        FlashMessages.add_message(handler, 'warning', text)
    
    @staticmethod
    def info(handler, text):
        """Add an info message"""
        FlashMessages.add_message(handler, 'info', text)
