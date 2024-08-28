import os
import PyInstaller.__main__

project_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(project_dir, 'output')
icon_path = os.path.join(project_dir, 'assets', 'icons', 'logo.ico')
main_script = os.path.join(project_dir, 'College Event Score System.py')

PyInstaller.__main__.run([
    '--noconfirm',
    '--onedir',
    '--windowed',
    f'--icon={icon_path}',
    f'--name=College Event Score System',
    f'--distpath={output_dir}',
    '--add-data=' + os.path.join(project_dir, 'assets') + os.pathsep + 'assets/',
    '--add-data=' + os.path.join(project_dir, 'backups') + os.pathsep + 'backups/',
    '--add-data=' + os.path.join(project_dir, 'data') + os.pathsep + 'data/',
    '--add-data=' + os.path.join(project_dir, 'gui') + os.pathsep + 'gui/',
    '--add-data=' + os.path.join(project_dir, 'logs') + os.pathsep + 'logs/',
    '--add-data=' + os.path.join(project_dir, 'reports') + os.pathsep + 'reports/',
    '--add-data=' + os.path.join(project_dir, 'themes') + os.pathsep + 'themes/',
    '--add-data=' + os.path.join(project_dir, 'utils') + os.pathsep + 'utils/',
    '--hidden-import=html.parser',
    main_script
])
