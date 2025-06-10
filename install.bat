set CMAKE_GENERATOR=Ninja
set FC=x86_64-w64-mingw32-gfortran.exe

REM call conda install -y -c conda-forge impi-devel

echo [build_ext] > code\fabm\setup.cfg
echo build_temp=../../build/pyfabm >> code\fabm\setup.cfg
pip install -v code\fabm
if errorlevel 1 exit /b 1

cmake -B build/gotm -S code/gotm -DFABM_BASE=code/fabm -DCMAKE_BUILD_TYPE=Release -G Ninja -DCMAKE_INSTALL_PREFIX=%CONDA_PREFIX%
if errorlevel 1 exit /b 1
cmake --build build/gotm --target install
if errorlevel 1 exit /b 1

echo [build_ext] > code\pygetm\python\setup.cfg
echo build_temp=../../../build/pygetm >> code\pygetm\python\setup.cfg
echo cmake_opts=-DFABM_BASE=../../fabm >> code\pygetm\python\setup.cfg
call code\pygetm\install.bat
if errorlevel 1 exit /b 1

echo [build_ext] > code\fabmos\setup.cfg
echo build_temp=../../build/fabmos >> code\fabmos\setup.cfg
echo cmake_opts=-DFABM_BASE=../fabm >> code\fabmos\setup.cfg
pip install -v code\fabmos
if errorlevel 1 exit /b 1

REM call code\eat\install.bat
