@echo off
REM Package project into a portable zip (Windows)
setlocal
set ZIPNAME=diabetic_retinopathy_system_release.zip





pauseendlocalecho Created ..\%ZIPNAME%powershell -Command "Compress-Archive -Path * -DestinationPath ..\%ZIPNAME% -Force -CompressionLevel Optimal -Exclude 'venv','venv\\*','.git','staticfiles','staticfiles\\*','media','media\\*','__pycache__','__pycache__\\*','*.pyc','.env'"necho Creating %ZIPNAME% in parent directory...