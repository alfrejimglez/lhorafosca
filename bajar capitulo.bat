@echo off
set /p URL=Introduce la URL que quieres descargar: 
cd C:\Users\alfre\OneDrive\Documentos\Lahorafosca
ffmpeg -i "%URL%" -c copy -bsf:a aac_adtstoasc output.mp4
pause
