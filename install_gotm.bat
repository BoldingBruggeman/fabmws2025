set CMAKE_GENERATOR=Ninja
set FC=x86_64-w64-mingw32-gfortran.exe

cmake -B build/gotm -S code/gotm -DFABM_BASE=code/fabm -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%CONDA_PREFIX%
if errorlevel 1 exit /b 1
cmake --build build/gotm --target install
