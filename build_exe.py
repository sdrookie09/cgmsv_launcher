#!/usr/bin/env python3
"""
CGMSV Launcher Build Script
This script builds the launcher into an executable file.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from version import __version__

def check_dependencies():
    """Check required dependencies"""
    print("🔍 Checking dependencies...")
    
    required_packages = ['psutil', 'yaml', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'yaml':
                import yaml
            elif package == 'tkinter':
                import tkinter
            else:
                __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are available")
    return True

def install_pyinstaller():
    """Install PyInstaller"""
    print("\n🔧 Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                      check=True, capture_output=True, text=True)
        print("✅ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyInstaller: {e}")
        return False

def build_executable():
    """Build executable file"""
    print(f"\n🏗️ Building CGMSV Launcher v{__version__}...")
    
    # PyInstaller command configuration
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single file
        "--windowed",                   # Hide console window
        f"--name=CGMSVLauncher-v{__version__}",  # Executable name with version
        "--icon=icon6.0.ico",           # Icon (if available)
        "--add-data=config.yml;.",      # Include config file
        "--add-data=version.py;.",      # Include version file
        "--hidden-import=tkinter",      # Explicitly include tkinter
        "--hidden-import=tkinter.ttk",  # Explicitly include ttk
        "--hidden-import=tkinter.filedialog",  # Explicitly include filedialog
        "launcher_main.py"
    ]
    
    # Remove icon if not available
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_distribution():
    """Create distribution package"""
    print("\n📦 Creating distribution package...")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist directory not found. Build may have failed.")
        return False
    
    # Create distribution folder
    package_dir = Path(f"CGMSVLauncher-v{__version__}_Package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy executable
    exe_file = dist_dir / f"CGMSVLauncher-v{__version__}.exe"
    if exe_file.exists():
        shutil.copy2(exe_file, package_dir)
        print(f"✅ Copied {exe_file.name}")
    else:
        print(f"❌ Executable not found: {exe_file}")
        return False
    
    # Copy config file
    if os.path.exists("config.yml"):
        shutil.copy2("config.yml", package_dir)
        print("✅ Copied config.yml")
    
    # Copy README file
    if os.path.exists("README.md"):
        shutil.copy2("README.md", package_dir)
        print("✅ Copied README.md")
    
    # Copy version file
    if os.path.exists("version.py"):
        shutil.copy2("version.py", package_dir)
        print("✅ Copied version.py")
    
    # Create usage file
    create_usage_file(package_dir)
    
    # Create version info file
    create_version_info(package_dir)
    
    print(f"✅ Distribution package created: {package_dir}")
    return True

def create_usage_file(package_dir):
    """Create usage file"""
    usage_content = f"""# CGMSV Launcher v{__version__} Usage Guide

## How to Run
1. Double-click CGMSVLauncher-v{__version__}.exe to run
2. Or run `CGMSVLauncher-v{__version__}.exe` from command prompt

## Main Features
- Run multiple CGs simultaneously
- Automatically move each CG window to specified position
- Real-time CG status monitoring
- Individual CG position adjustment and termination

## Configuration File
- Modify config.yml file to customize UI text, position settings, etc.
- If config file is missing, runs with default settings

## System Requirements
- Windows 10/11
- .NET Framework 4.5 or higher (installed by default on most Windows)

## Troubleshooting
- If execution fails: Visual C++ Redistributable installation required
- If window positioning doesn't work: Try running as administrator

## Support
If problems occur, refer to README.md file.
"""
    
    with open(package_dir / "Usage.txt", "w", encoding="utf-8") as f:
        f.write(usage_content)
    print("✅ Created Usage.txt")

def create_version_info(package_dir):
    """Create version info file"""
    version_info = f"""CGMSV Launcher v{__version__}

Build Information:
- Version: {__version__}
- Author: sdrookie09
- License: MIT
- Description: Multi-CGMSV Instance Manager

Release Notes:
- Initial release
- Multi-CGMSV instance management
- Automatic window positioning
- Real-time process monitoring
- Configurable UI and settings
"""
    
    with open(package_dir / "VERSION.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    print("✅ Created VERSION.txt")

def main():
    """Main build process"""
    print(f"🚀 CGMSV Launcher v{__version__} Build Process")
    print("=" * 50)
    
    # 1. Check dependencies
    if not check_dependencies():
        return False
    
    # 2. Check PyInstaller installation
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        if not install_pyinstaller():
            return False
    
    # 3. Execute build
    if not build_executable():
        return False
    
    # 4. Create distribution package
    if not create_distribution():
        return False
    
    print(f"\n🎉 CGMSV Launcher v{__version__} build process completed successfully!")
    print(f"\n📁 Distribution package: CGMSVLauncher-v{__version__}_Package/")
    print(f"📄 Executable: CGMSVLauncher-v{__version__}_Package/CGMSVLauncher-v{__version__}.exe")
    print(f"\n💡 Tip: Deploy the entire CGMSVLauncher-v{__version__}_Package folder.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Build process failed!")
        sys.exit(1) 