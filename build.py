import PyInstaller.__main__
import os
import platform
import shutil

def build_windows_exe():
    """
    Build the Windows executable using PyInstaller.
    """
    # Clean up previous build
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    # PyInstaller arguments
    args = [
        'recipe_manager.py',  # Main script
        '--name=LunarBatch',  # Name of the executable
        '--windowed',  # Don't show console window
        '--onefile',  # Create a single executable
        '--icon=icon.ico',  # Application icon
        '--add-data=README.md;.',  # Include README
        '--add-data=LICENSE;.',  # Include license
        '--version-file=version_info.txt',  # Version information
        '--noconfirm',  # Don't ask for confirmation
    ]

    # Run PyInstaller
    try:
        PyInstaller.__main__.run(args)
        print("Build complete! The executable is in the 'dist' directory.")
    except Exception as e:
        print(f"Error during build: {str(e)}")
        print("Make sure all dependencies are installed correctly:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    if platform.system() == "Windows":
        build_windows_exe()
    else:
        print("This build script is for Windows only.") 