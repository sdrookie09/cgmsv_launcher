# CGMSV Launcher

A powerful Python-based launcher that allows you to run multiple cgs simultaneously with automatic window positioning and management. Perfect for managing multiple applications, games, or development tools.

## Features

- **Multi-CG Management**: Run and manage multiple cgs simultaneously
- **Automatic Window Positioning**: Automatically position windows at predefined locations (6 positions for 1920x1080 resolution)
- **Real-time Process Monitoring**: Track program status and automatically detect when cg close
- **Individual CG Control**: Terminate specific CGs or all CGs at once
- **Position Adjustment**: Change window positions after CGs are running
- **Hidden Execution**: Run CGs without showing batch/console windows
- **Configurable Interface**: Customizable UI text and settings via YAML configuration
- **Cross-Platform**: Works on Windows with Python 3.7+

## Installation

### Prerequisites

- Python 3.7 or higher
- Windows OS
- Visual C++ Redistributable (for some programs)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/[YOUR_USERNAME]/cgmsv_launcher.git
   cd cgmsv_launcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the launcher**
   ```bash
   python launcher_main.py
   ```

### Building Executable

To create a standalone executable:

```bash
python build_exe.py
```

The executable will be created in the `CGMSVLauncher_Package/` directory.

## Usage

### Basic Operation

1. **Add a Program**
   - Click "Select File" to choose an executable
   - Enter any command-line parameters (optional)
   - Select the desired window position
   - Click "Run Program"

2. **Manage Programs**
   - View all running programs in the list
   - Select a program to adjust its position
   - Use "Terminate Program" to close individual programs
   - Use "Terminate All Programs" to close everything

3. **Position Management**
   - 6 predefined positions for 1920x1080 resolution
   - Automatic position adjustment after program launch
   - Manual position adjustment for running programs

### Window Positions

The launcher supports 6 predefined positions:

- **Top Left**: (0, 0)
- **Top Center**: (640, 0)
- **Top Right**: (1280, 0)
- **Bottom Left**: (0, 480)
- **Bottom Center**: (640, 480)
- **Bottom Right**: (1280, 480)

## Configuration

The launcher uses `config.yml` for all settings and text customization:

```yaml
launcher:
  title: "CGMSV Launcher"
  window_size: "900x700"
  log_height: 12

ui:
  add_program:
    title: "Add New Program"
    program_label: "Program:"
    select_file_button: "Select File"
    param_label: "Parameters:"
    position_label: "Position:"
    run_button: "Run Program"

positions:
  top_left:
    name: "Top Left"
    display: "Top Left (0, 0)"
    coords: [0, 0]
  # ... more positions

messages:
  program_selected: "Program selected: {filename}"
  errors:
    no_program_selected: "❌ Please select a program first."
```

## Project Structure

```
multi-program-launcher/
├── launcher_main.py          # Main entry point
├── config_manager.py         # Configuration management
├── program_manager.py        # Program execution and management
├── ui_manager.py            # User interface management
├── monitor_manager.py       # Process monitoring
├── logger.py                # Logging functionality
├── config.yml               # Configuration file
├── requirements.txt         # Python dependencies
├── build_exe.py            # Build script for executable
└── README.md               # This file
```

## Features in Detail

### Hidden Execution
- Programs are launched using hidden batch files
- No console windows appear during execution
- Clean, professional appearance

### Process Tracking
- Real-time monitoring of program status
- Automatic detection of program termination
- PID tracking for precise control

### Position Adjustment
- Uses PowerShell for window positioning
- Windows API integration for reliable positioning
- Automatic retry mechanism for failed adjustments

### Error Handling
- Comprehensive error logging
- User-friendly error messages
- Graceful handling of program failures

## Development

### Running from Source

1. **Set up virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the launcher**
   ```bash
   python launcher_main.py
   ```

### Building

```bash
python build_exe.py
```

This creates a standalone executable with all dependencies included.

## Troubleshooting

### Common Issues

1. **Program doesn't start**
   - Check if the executable path is correct
   - Ensure the program doesn't require admin privileges
   - Verify Visual C++ Redistributable is installed

2. **Window positioning fails**
   - Some programs may not support window positioning
   - Try running the launcher as administrator
   - Check if the program has a main window

3. **PowerShell execution blocked**
   - Check Windows execution policy
   - Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Logs

Check the execution log in the launcher interface for detailed error messages and debugging information.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
테스트
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and Tkinter
- Uses PowerShell for Windows API integration
- Inspired by the need for efficient multi-program management

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/sdrookie09/cgmsv_launcher/issues) page
2. Create a new issue with detailed information
3. Include system information and error logs

---

**Note**: This launcher is designed for Windows systems. For other operating systems, modifications may be required. 
