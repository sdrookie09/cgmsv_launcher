import time
import tkinter as tk

class Logger:
    def __init__(self, log_text_widget=None):
        self.log_text = log_text_widget
        self.messages = []
        self.max_messages = 1000  # Keep last 1000 messages
    
    def set_log_widget(self, log_text_widget):
        """Set the log text widget"""
        self.log_text = log_text_widget
    
    def log(self, message):
        """Add log message"""
        timestamp = time.strftime('%H:%M:%S')
        log_entry = f"{timestamp} - {message}"
        
        # Store message
        self.messages.append(log_entry)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        
        # Update UI if available
        if self.log_text:
            def update_log():
                self.log_text.insert(tk.END, log_entry + "\n")
                self.log_text.see(tk.END)
            self.log_text.after(0, update_log)
        
        # Also print to console for debugging
        print(log_entry)
    
    def get_messages(self):
        """Get all stored messages"""
        return self.messages.copy()
    
    def clear_messages(self):
        """Clear all messages"""
        self.messages.clear()
        if self.log_text:
            def clear_log():
                self.log_text.delete(1.0, tk.END)
            self.log_text.after(0, clear_log) 