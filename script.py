import PyInstaller.__main__
import os
import sys

def build_app():
    # Get the absolute path to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to your source files
    main_script = os.path.join(script_dir, 'src', 'image_pdf_converter.py')
    icon_file = os.path.join(script_dir, 'src', 'icon.png')
    
    # Convert PNG to ICO if on Windows
    if sys.platform.startswith('win'):
        from PIL import Image
        ico_file = os.path.join(script_dir, 'src', 'icon.ico')
        if not os.path.exists(ico_file):
            img = Image.open(icon_file)
            img.save(ico_file, format='ICO')
        icon_file = ico_file

    # PyInstaller arguments
    args = [
        main_script,
        '--name=ImagePDFConverter',
        '--onefile',
        f'--icon={icon_file}',
        '--noconsole',
        '--add-data=src/icon.png;src',  
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=ttkthemes',
    ]

    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build_app()