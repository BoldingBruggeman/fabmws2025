set CMAKE_GENERATOR=Ninja
set FC=gfortran

conda install -y -c conda-forge impi-devel

pip install -v code\fabm

cmake -B build/gotm -S code/gotm -DFABM_BASE=code/fabm -DCMAKE_BUILD_TYPE=Release -G Ninja -DCMAKE_INSTALL_PREFIX=%CONDA_PREFIX%
cmake --build build/gotm --target install

call code\pygetm\install.bat

pip install -v code\fabmos

call code\eat\install.bat
