import yaml
import os

class ConfigManager:
    def __init__(self, config_file='config.yml'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load config file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print("Config file not found. Using default settings.")
            return self.get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            'launcher': {'title': 'CGMSV Launcher', 'window_size': '900x700', 'log_height': 12},
            'ui': {
                'add_program': {'title': 'Add New CG', 'program_label': 'CG Program:', 'program_placeholder': 'Please select a CG program'},
                'program_list': {'title': 'Running CGs'},
                'controls': {'position_adjust': 'Adjust Position', 'terminate_program': 'Terminate CG', 'terminate_all': 'Terminate All CGs'},
                'position_change': {'title': 'Change Position'},
                'log': {'title': 'Execution Log'}
            },
            'positions': {
                'top_left': {'name': 'Top Left', 'coords': [0, 0]},
                'top_mid': {'name': 'Top Center', 'coords': [640, 0]},
                'top_right': {'name': 'Top Right', 'coords': [1280, 0]},
                'bottom_left': {'name': 'Bottom Left', 'coords': [0, 480]},
                'bottom_mid': {'name': 'Bottom Center', 'coords': [640, 480]},
                'bottom_right': {'name': 'Bottom Right', 'coords': [1280, 480]}
            },
            'defaults': {'position': 'top_left', 'window_size': [640, 480]},
            'messages': {
                'program_selected': 'CG selected: {filename}',
                'errors': {'no_program_selected': '❌ Please select a CG program first.'}
            },
            'default_params': '',
            'monitoring': {'check_interval': 5, 'max_position_attempts': 10, 'position_attempt_interval': 2, 'timeout': 5}
        }
    
    def get_message(self, message_key, **kwargs):
        """Get message (with formatting)"""
        try:
            # Handle nested keys (e.g., 'errors.no_program_selected')
            keys = message_key.split('.')
            value = self.config['messages']
            for key in keys:
                value = value[key]
            
            return value.format(**kwargs)
        except (KeyError, TypeError):
            return f"Message not found: {message_key}"
    
    def get_position_coords(self, position_name):
        """Convert position name to coordinates"""
        if position_name in self.config['positions']:
            return tuple(self.config['positions'][position_name]['coords'])
        return (0, 0)
    
    def get_position_name(self, coords):
        """Convert coordinates to position name"""
        for pos_key, pos_info in self.config['positions'].items():
            if tuple(pos_info['coords']) == coords:
                return pos_info['name']
        return f"({coords[0]}, {coords[1]})"
    
    def get_config(self):
        """Get current configuration"""
        return self.config 