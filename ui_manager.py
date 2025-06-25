import tkinter as tk
from tkinter import ttk, filedialog
import time
import os

class UIManager:
    def __init__(self, root, config_manager, program_manager, logger):
        self.root = root
        self.config_manager = config_manager
        self.program_manager = program_manager
        self.logger = logger
        self.config = config_manager.get_config()
        
        # UI components
        self.path_display = None
        self.param_input = None
        self.default_position = None
        self.new_position = None
        self.program_tree = None
        self.log_text = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top: Add program section
        self.create_add_program_section(main_frame)
        
        # Middle: Program list
        self.create_program_list_section(main_frame)
        
        # Bottom: Control buttons
        self.create_control_section(main_frame)
        
        # Log display
        self.create_log_section(main_frame)
    
    def create_add_program_section(self, parent):
        """Create add program section"""
        add_frame = ttk.LabelFrame(parent, text=self.config['ui']['add_program']['title'], padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        file_frame = ttk.Frame(add_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text=self.config['ui']['add_program']['program_label']).pack(side=tk.LEFT)
        self.path_display = ttk.Label(file_frame, text=self.config['ui']['add_program']['program_placeholder'], foreground="gray")
        self.path_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        select_file_button = ttk.Button(file_frame, text=self.config['ui']['add_program']['select_file_button'], command=self.select_program_file)
        select_file_button.pack(side=tk.RIGHT)
        
        # Parameter input
        param_frame = ttk.Frame(add_frame)
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(param_frame, text=self.config['ui']['add_program']['param_label']).pack(side=tk.LEFT)
        self.param_input = ttk.Entry(param_frame)
        self.param_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        self.param_input.insert(0, self.config.get('default_params', ''))
        
        # Position selection
        pos_frame = ttk.Frame(add_frame)
        pos_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(pos_frame, text=self.config['ui']['add_program']['position_label']).pack(side=tk.LEFT)
        
        # Position variable
        self.default_position = tk.StringVar(value=self.config['defaults']['position'])
        
        # Create position radio buttons
        for i, (pos_key, pos_info) in enumerate(self.config['positions'].items()):
            ttk.Radiobutton(pos_frame, text=pos_info['display'], variable=self.default_position, 
                           value=pos_key).pack(side=tk.LEFT, padx=(10 if i == 0 else 0, 10))
        
        # Run button
        run_button = ttk.Button(add_frame, text=self.config['ui']['add_program']['run_button'], command=self.run_program_threaded)
        run_button.pack()
    
    def create_program_list_section(self, parent):
        """Create program list section"""
        list_frame = ttk.LabelFrame(parent, text=self.config['ui']['program_list']['title'], padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Program list treeview
        columns = ('ID', '이름', '상태', '위치', 'PID')
        self.program_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Column configuration
        column_config = self.config['ui']['program_list']['columns']
        column_widths = self.config['ui']['program_list']['column_widths']
        
        # Column mapping (map Korean keys to English column names)
        column_mapping = {
            'id': 'ID',
            'name': '이름', 
            'status': '상태',
            'position': '위치',
            'pid': 'PID'
        }
        
        for col, text in column_config.items():
            if col in column_mapping:
                column_id = column_mapping[col]
                self.program_tree.heading(column_id, text=text)
                self.program_tree.column(column_id, width=column_widths.get(col, 100))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.program_tree.yview)
        self.program_tree.configure(yscrollcommand=scrollbar.set)
        
        self.program_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Program selection event
        self.program_tree.bind('<<TreeviewSelect>>', self.on_program_select)
    
    def create_control_section(self, parent):
        """Create control section"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        controls = self.config['ui']['controls']
        ttk.Button(control_frame, text=controls['position_adjust'], command=self.adjust_selected_position).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text=controls['terminate_program'], command=self.terminate_selected_program).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text=controls['terminate_all'], command=self.terminate_all_programs).pack(side=tk.LEFT)
        
        # Position change frame
        pos_change_frame = ttk.LabelFrame(control_frame, text=self.config['ui']['position_change']['title'], padding="5")
        pos_change_frame.pack(side=tk.RIGHT)
        
        self.new_position = tk.StringVar(value=self.config['defaults']['position'])
        for i, (pos_key, pos_info) in enumerate(self.config['positions'].items()):
            ttk.Radiobutton(pos_change_frame, text=pos_info['name'], variable=self.new_position, 
                           value=pos_key).pack(side=tk.LEFT, padx=(0, 5))
    
    def create_log_section(self, parent):
        """Create log section"""
        log_frame = ttk.LabelFrame(parent, text=self.config['ui']['log']['title'], padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=self.config['launcher']['log_height'], wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def select_program_file(self):
        """Select program file"""
        file_dialog_config = self.config.get('file_dialog', {})
        file_path = filedialog.askopenfilename(
            title=file_dialog_config.get('title', 'Select Program to Execute'),
            filetypes=file_dialog_config.get('file_types', [("Executable Files", "*.exe"), ("All Files", "*.*")])
        )
        
        if file_path:
            self.path_display.config(text=file_path, foreground="black")
            self.logger.log(self.config_manager.get_message('program_selected', filename=os.path.basename(file_path)))
    
    def run_program_threaded(self):
        """Run program in thread"""
        import threading
        
        def run_in_thread():
            self.run_program()
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
    
    def run_program(self):
        """Run program"""
        program_path = self.path_display.cget("text")
        if program_path == self.config['ui']['add_program']['program_placeholder']:
            self.logger.log(self.config_manager.get_message('errors.no_program_selected'))
            return
        
        params = self.param_input.get().strip()
        position_name = self.default_position.get()
        
        program_id = self.program_manager.run_program(program_path, params, position_name)
        if program_id:
            self.update_program_list()
    
    def update_program_list(self):
        """Update program list UI"""
        def update():
            # Delete existing items
            for item in self.program_tree.get_children():
                self.program_tree.delete(item)
            
            # Add new items
            for program_id, info in self.program_manager.get_programs().items():
                position_name = self.config_manager.get_position_name(info['position'])
                pid = info.get('pid', 'N/A')
                
                self.program_tree.insert('', 'end', values=(
                    program_id,
                    info['name'],
                    info['status'],
                    position_name,
                    pid
                ))
        
        self.root.after(0, update)
    
    def on_program_select(self, event):
        """Program selection event"""
        selection = self.program_tree.selection()
        if selection:
            item = self.program_tree.item(selection[0])
            program_id = item['values'][0]
            self.logger.log(self.config_manager.get_message('progress.program_selected_ui', id=program_id))
    
    def adjust_selected_position(self):
        """Adjust position of selected program"""
        selection = self.program_tree.selection()
        if not selection:
            self.logger.log(self.config_manager.get_message('errors.no_program_to_adjust'))
            return
        
        item = self.program_tree.item(selection[0])
        program_id = item['values'][0]
        
        position_name = self.new_position.get()
        x, y = self.config_manager.get_position_coords(position_name)
        
        self.logger.log(self.config_manager.get_message('progress.position_adjusting', id=program_id, position=self.config_manager.get_position_name((x, y))))
        
        # Update position information
        if self.program_manager.update_program_position(program_id, position_name):
            self.update_program_list()
            # Actually adjust position
            self.program_manager.adjust_program_position(program_id, x, y)
        else:
            self.logger.log(self.config_manager.get_message('errors.program_info_not_found', id=program_id))
    
    def terminate_selected_program(self):
        """Terminate selected program"""
        selection = self.program_tree.selection()
        if not selection:
            self.logger.log(self.config_manager.get_message('errors.no_program_to_terminate'))
            return
        
        item = self.program_tree.item(selection[0])
        program_id = item['values'][0]
        
        self.program_manager.terminate_program(program_id)
        self.update_program_list()
    
    def terminate_all_programs(self):
        """Terminate all programs"""
        self.program_manager.terminate_all_programs()
        self.update_program_list()
    
    def log(self, message):
        """Add log message (thread-safe)"""
        def update_log():
            self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
            self.log_text.see(tk.END)
        self.root.after(0, update_log) 