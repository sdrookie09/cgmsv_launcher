#!/usr/bin/env python3
"""
Multi-Program Launcher Build Script
이 스크립트는 런처를 실행 파일로 빌드합니다.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """필요한 의존성 확인"""
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
    """PyInstaller 설치"""
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
    """실행 파일 빌드"""
    print("\n🏗️ Building executable...")
    
    # PyInstaller 명령어 구성
    cmd = [
        "pyinstaller",
        "--onefile",                    # 단일 파일로 생성
        "--windowed",                   # 콘솔 창 숨김
        "--name=MultiProgramLauncher",  # 실행 파일 이름
        "--icon=icon6.0.ico",              # 아이콘 (있는 경우)
        "--add-data=config.yml;.",      # 설정 파일 포함
        "--hidden-import=tkinter",      # tkinter 명시적 포함
        "--hidden-import=tkinter.ttk",  # ttk 명시적 포함
        "--hidden-import=tkinter.filedialog",  # filedialog 명시적 포함
        "launcher_main.py"
    ]
    
    # 아이콘이 없으면 제거
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
    """배포 패키지 생성"""
    print("\n📦 Creating distribution package...")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist directory not found. Build may have failed.")
        return False
    
    # 배포 폴더 생성
    package_dir = Path("MultiProgramLauncher_Package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # 실행 파일 복사
    exe_file = dist_dir / "MultiProgramLauncher.exe"
    if exe_file.exists():
        shutil.copy2(exe_file, package_dir)
        print(f"✅ Copied {exe_file.name}")
    else:
        print(f"❌ Executable not found: {exe_file}")
        return False
    
    # 설정 파일 복사
    if os.path.exists("config.yml"):
        shutil.copy2("config.yml", package_dir)
        print("✅ Copied config.yml")
    
    # README 파일 복사
    if os.path.exists("README_MODULAR.md"):
        shutil.copy2("README_MODULAR.md", package_dir)
        print("✅ Copied README_MODULAR.md")
    
    # 사용법 파일 생성
    create_usage_file(package_dir)
    
    print(f"✅ Distribution package created: {package_dir}")
    return True

def create_usage_file(package_dir):
    """사용법 파일 생성"""
    usage_content = """# Multi-Program Launcher 사용법

## 실행 방법
1. MultiProgramLauncher.exe를 더블클릭하여 실행
2. 또는 명령 프롬프트에서 `MultiProgramLauncher.exe` 실행

## 주요 기능
- 여러 프로그램을 동시에 실행
- 각 프로그램 창을 지정된 위치로 자동 이동
- 실시간 프로그램 상태 모니터링
- 개별 프로그램 위치 조정 및 종료

## 설정 파일
- config.yml 파일을 수정하여 UI 텍스트, 위치 설정 등을 커스터마이징 가능
- 설정 파일이 없으면 기본 설정으로 실행

## 시스템 요구사항
- Windows 10/11
- .NET Framework 4.5 이상 (대부분의 Windows에 기본 설치됨)

## 문제 해결
- 실행이 안 되는 경우: Visual C++ Redistributable 설치 필요
- 창 위치 조정이 안 되는 경우: 관리자 권한으로 실행해보세요

## 지원
문제가 발생하면 README_MODular.md 파일을 참조하세요.
"""
    
    with open(package_dir / "사용법.txt", "w", encoding="utf-8") as f:
        f.write(usage_content)
    print("✅ Created usage.txt")

def main():
    """메인 빌드 프로세스"""
    print("🚀 Multi-Program Launcher Build Process")
    print("=" * 50)
    
    # 1. 의존성 확인
    if not check_dependencies():
        return False
    
    # 2. PyInstaller 설치 확인
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        if not install_pyinstaller():
            return False
    
    # 3. 빌드 실행
    if not build_executable():
        return False
    
    # 4. 배포 패키지 생성
    if not create_distribution():
        return False
    
    print("\n🎉 Build process completed successfully!")
    print("\n📁 Distribution package: MultiProgramLauncher_Package/")
    print("📄 Executable: MultiProgramLauncher_Package/MultiProgramLauncher.exe")
    print("\n💡 Tip: MultiProgramLauncher_Package 폴더 전체를 배포하세요.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Build process failed!")
        sys.exit(1) 