git pull
if errorlevel 1 exit /b 1

git submodule update --init --recursive
if errorlevel 1 exit /b 1

conda env update -f environment.yml
if errorlevel 1 exit /b 1

call install.bat
