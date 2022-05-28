rmdir ./release /S /Q
pyinstaller --distpath ./release --workpath ./release/build --onedir --nowindowed --icon=../img/logo.png --specpath ./release -n MyBalance main.py
