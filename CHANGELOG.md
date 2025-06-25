# Changelog

All notable changes to CGMSV Launcher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-25

### Added
- Initial release of CGMSV Launcher
- Multi-CGMSV instance management
- Automatic window positioning (6 predefined positions for 1920x1080 resolution)
- Real-time process monitoring and status tracking
- Individual CGMSV instance control (terminate specific instances)
- Bulk termination (terminate all instances at once)
- Hidden execution (no console windows during launch)
- Configurable UI text and settings via YAML configuration
- Position adjustment for running instances
- Comprehensive error handling and logging
- PowerShell-based window positioning using Windows API
- Automatic retry mechanism for failed position adjustments
- PID tracking for precise process control
- Batch file cleanup on instance termination
- Thread-safe UI updates
- Cross-platform compatibility (Windows focus)

### Features
- **UI Components**:
  - File selection dialog for CGMSV executables
  - Parameter input for command-line arguments
  - Position selection radio buttons
  - Real-time CGMSV instance list with status
  - Control buttons for position adjustment and termination
  - Execution log display

- **Configuration**:
  - YAML-based configuration system
  - Customizable UI text and messages
  - Configurable window positions
  - Default parameter settings
  - Monitoring interval settings

- **Process Management**:
  - Hidden batch file execution
  - Process monitoring with automatic cleanup
  - Window handle detection and positioning
  - Graceful termination handling

### Technical Details
- Built with Python 3.7+
- Uses Tkinter for GUI
- PowerShell integration for Windows API calls
- psutil for process management
- PyYAML for configuration parsing
- PyInstaller for executable building

### System Requirements
- Windows 10/11
- Python 3.7 or higher
- Visual C++ Redistributable (for some programs)
- .NET Framework 4.5 or higher

### Known Issues
- Window positioning may not work with some CGMSV instances
- Requires administrator privileges for certain window operations
- Limited to Windows platform

### Future Enhancements
- Support for custom window positions
- Enhanced error recovery mechanisms
- Additional UI themes and customization options
- Cross-platform support (Linux/macOS)
- Plugin system for extended functionality

---

## Version History

### [1.0.0] - 2024-12-25
- Initial release with all core features
- Multi-CGMSV instance management and window positioning
- Hidden execution and process monitoring
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