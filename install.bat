set CMAKE_GENERATOR=Ninja
set FC=gfortran

call conda install -y -c conda-forge impi-devel

echo [build_ext] > code\fabm\setup.cfg
echo build_temp=../../build/pyfabm >> code\fabm\setup.cfg
pip install -v code\fabm

cmake -B build/gotm -S code/gotm -DFABM_BASE=code/fabm -DCMAKE_BUILD_TYPE=Release -G Ninja -DCMAKE_INSTALL_PREFIX=%CONDA_PREFIX%
cmake --build build/gotm --target install

echo build_temp=../../../build/pygetm >> code\pygetm\python\setup.cfg
echo cmake_opts=-DFABM_BASE=../../fabm >> code\pygetm\python\setup.cfg
call code\pygetm\install.bat

echo [build_ext] > code\fabmos\setup.cfg
echo build_temp=../../build/fabmos >> code\fabmos\setup.cfg
echo cmake_opts=-DFABM_BASE=../fabm >> code\fabmos\setup.cfg
pip install -v code\fabmos

REM call code\eat\install.bat
