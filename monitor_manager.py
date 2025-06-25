import threading
import time
import psutil

class MonitorManager:
    def __init__(self, config_manager, program_manager, logger, ui_manager=None):
        self.config_manager = config_manager
        self.program_manager = program_manager
        self.logger = logger
        self.ui_manager = ui_manager
        self.monitor_thread = None
        self.is_running = False
    
    def set_ui_manager(self, ui_manager):
        """Set UI manager reference"""
        self.ui_manager = ui_manager
    
    def start_monitoring(self):
        """Start CG monitoring"""
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self.is_running = True
            self.monitor_thread = threading.Thread(target=self.monitor_programs, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop CG monitoring"""
        self.is_running = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
    
    def monitor_programs(self):
        """Monitor CG status"""
        check_interval = self.config_manager.config['monitoring']['check_interval']
        
        while self.is_running:
            try:
                # Check status of each CG
                for program_id, info in list(self.program_manager.get_programs().items()):
                    if not self.program_manager.check_program_status(program_id):
                        # CG was closed, update UI
                        if self.ui_manager:
                            self.ui_manager.update_program_list()
                
                time.sleep(check_interval)
                
            except Exception as e:
                self.logger.log(self.config_manager.get_message('errors.monitoring_error', error=str(e)))
                time.sleep(check_interval) 