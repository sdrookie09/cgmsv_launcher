import tkinter as tk
import time
import os

from config_manager import ConfigManager
from program_manager import ProgramManager
from ui_manager import UIManager
from monitor_manager import MonitorManager
from logger import Logger

class MultiProgramLauncher:
    def __init__(self, root):
        self.root = root
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.logger = Logger()
        self.program_manager = ProgramManager(self.config_manager, self.logger)
        
        # Apply launcher settings
        self.root.title(self.config_manager.config['launcher']['title'])
        self.root.geometry(self.config_manager.config['launcher']['window_size'])
        
        # Initialize UI
        self.ui_manager = UIManager(self.root, self.config_manager, self.program_manager, self.logger)
        
        # Set log widget reference
        self.logger.set_log_widget(self.ui_manager.log_text)
        
        # Initialize monitor with UI manager reference
        self.monitor_manager = MonitorManager(self.config_manager, self.program_manager, self.logger, self.ui_manager)
        
        # Close all programs when launcher closes
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start monitoring
        self.monitor_manager.start_monitoring()
    
    def on_closing(self):
        """Close launcher and terminate all programs"""
        self.logger.log(self.config_manager.get_message('launcher_closing'))
        self.program_manager.terminate_all_programs()
        self.monitor_manager.stop_monitoring()
        time.sleep(2)  # Wait for termination
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MultiProgramLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 