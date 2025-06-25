# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- Initial release of Multi-Program Launcher
- Multi-program management with simultaneous execution
- Automatic window positioning (6 predefined positions for 1920x1080 resolution)
- Real-time process monitoring and status tracking
- Individual program control (terminate specific programs or all programs)
- Position adjustment for running programs
- Hidden execution (no batch/console windows visible)
- Configurable interface via YAML configuration
- Comprehensive error handling and logging
- Modular architecture with separate managers for different functionalities
- Build system for creating standalone executables
- Cross-platform compatibility (Windows with Python 3.7+)

### Features
- **Program Management**: Run and manage multiple programs simultaneously
- **Window Positioning**: Automatically position windows at predefined locations
- **Process Monitoring**: Track program status and detect program termination
- **Hidden Execution**: Launch programs without showing console windows
- **Configuration System**: Customizable UI text and settings via YAML
- **Error Handling**: Comprehensive error logging and user-friendly messages
- **Build System**: Automated executable creation with PyInstaller

### Technical Details
- Built with Python and Tkinter for the user interface
- Uses PowerShell for Windows API integration and window positioning
- Modular design with separate managers for configuration, programs, UI, monitoring, and logging
- Hidden batch file execution for clean program launching
- Automatic cleanup of temporary files
- PID tracking for precise program control

### Architecture
- `launcher_main.py`: Main entry point and application initialization
- `config_manager.py`: Configuration file management and message handling
- `program_manager.py`: Program execution, positioning, and termination
- `ui_manager.py`: User interface management and event handling
- `monitor_manager.py`: Process monitoring and status updates
- `logger.py`: Logging functionality with thread-safe operations
- `build_exe.py`: Automated build system for creating executables

### Configuration
- YAML-based configuration system
- Customizable UI text and messages
- Configurable window positions and sizes
- Adjustable monitoring intervals and timeouts
- Localization support through message templates

### Dependencies
- Python 3.7+
- tkinter (included with Python)
- psutil (process management)
- PyYAML (configuration parsing)
- PyInstaller (executable building)

### Installation
- Source code installation with pip dependencies
- Standalone executable creation
- Virtual environment support
- Cross-platform compatibility (Windows focus)

### Documentation
- Comprehensive README with installation and usage instructions
- Contributing guidelines for developers
- Troubleshooting guide for common issues
- Configuration documentation
- Build and deployment instructions

---

## Version History

### [1.0.0] - 2024-12-19
- Initial release with all core features
- Multi-program management and window positioning
- Hidden execution and process monitoring
- Modular architecture and configuration system
- Comprehensive documentation and build system

---

## Future Plans

### Planned Features
- Support for custom window sizes
- Additional window positioning options
- Program presets and favorites
- Enhanced error recovery
- Performance optimizations
- Additional platform support

### Potential Enhancements
- Plugin system for extended functionality
- Advanced window management features
- Integration with system tray
- Automated testing framework
- Continuous integration setup

---

## Support

For support and questions:
- Check the [Issues](https://github.com/yourusername/multi-program-launcher/issues) page
- Review the [README](README.md) for documentation
- Consult the [Contributing](CONTRIBUTING.md) guide for development

---

**Note**: This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format and uses [Semantic Versioning](https://semver.org/) for version numbers. 