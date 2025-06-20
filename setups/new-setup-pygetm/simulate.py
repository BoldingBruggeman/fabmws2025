"""
This script performs a full 3D simulation of a 1 x 1 km domain
centered at the longitude and latitude specified by LON and LAT.
The horizontal resolution is currently set to 50 m, with 20 vertical
layers (sigma coordinates).

The bottom topography is obtained from the EMODnet database.
The simulation is forced by a single timeseries of ERA5 meteorology
obtained for the center coordinate.

Open boundaries currently use a Flather condition for elevation,
which requires prescribed elevation and depth-averaged currents (currently 0)
For tracers (currently T & S only) a zero-gradient condition is used.
We are still need to source decent open boundary conditions for
elevation, velocity and tracers (CMEMS?)

To run, you need pygetm:

conda install -c conda-forge pygetm

All necessary forcing is downloaded from the internet,
so this run script does not require any additional files.
"""

import datetime
import numpy as np
import pygetm
import pygetm.input.emodnet
import pygetm.input.igotm

LON, LAT = (22.87385000000006, 70.24538300000006)

# Set up the domain (x, y, lon, lat)
x = np.linspace(0.0, 1000.0, 21)
y = np.linspace(0.0, 1000.0, 21)
domain = pygetm.domain.create_cartesian(
    x, y, central_lon=LON, central_lat=LAT, interfaces=True
)

# Source bathymetry from EMODnet
elev_src = pygetm.input.emodnet.get(
    domain.lon.min(), domain.lon.max(), domain.lat.min(), domain.lat.max()
)

# Adjust bathymetry, mask, bottom roughness
domain.H = -pygetm.input.horizontal_interpolation(elev_src, domain.lon, domain.lat)
domain.mask = np.where(domain.H > 0.1, 1, 0)
domain.z0 = 0.001

# Filter out any isolated points/subbasins
domain.mask_subbasins()

# Smooth the bathymetry by limiting slope factor rx0
domain.smooth()

# Set up open boundaries along the entire outer edge;
# land points will be ignored at runtime
uvz_bc = pygetm.FLATHER_ELEV
domain.open_boundaries.allow_on_land = True
domain.open_boundaries.add_left_boundary("left", 0, 0, domain.ny, uvz_bc, None)
domain.open_boundaries.add_top_boundary(
    "top", domain.ny - 1, 1, domain.nx, uvz_bc, None
)
domain.open_boundaries.add_right_boundary(
    "right", domain.nx - 1, 0, domain.ny - 1, uvz_bc, None
)
domain.open_boundaries.add_bottom_boundary("bottom", 0, 1, domain.nx - 1, uvz_bc, None)

# Set up the simulation
sim = pygetm.Simulation(
    domain, vertical_coordinates=pygetm.vertical_coordinates.Sigma(20)
)

# Meteo from ERA5 (single time series for entire domain)
# Note: the default air-sea formulation ignores precipitation and evaporation.
# These can be added in the future, but if we care about freshwater fluxes,
# river runoff may be a bigger concern.
era5 = pygetm.input.igotm.download_era5(LON, LAT, 2020, logger=sim.logger)
sim.airsea.t2m.set(era5["t2m"])
sim.airsea.d2m.set(era5["d2m"])
sim.airsea.u10.set(era5["u10"])
sim.airsea.v10.set(era5["v10"])
sim.airsea.sp.set(era5["sp"])
sim.airsea.tcc.set(era5["tcc"])

# Initial conditions for temperature and salinity
# Here constant, in the future ideally sourced from simulations
# with larger domains (e.g., CMEMS) or observations
sim.temp.set(12.0)
sim.salt.set(35.0)

# Light attenuation
# In the future ideally based on local water type or
# in-situ or remotely sensed (e.g., OceanColour-CCI) observations
sim.radiation.jerlov_type = pygetm.radiation.Jerlov.Type_I

# Values at the open boundaries
# Here constant, in the future ideally sourced from simulations
# with larger domains (e.g., CMEMS) or observations
sim.temp.open_boundaries.values.set(12.0)
sim.salt.open_boundaries.values.set(35.0)
sim.T.z.open_boundaries.values.set(0.0)
sim.open_boundaries.u.set(0.0)
sim.open_boundaries.v.set(0.0)

# Output
out = sim.output_manager.add_netcdf_file(
    "test.nc", interval=datetime.timedelta(hours=1)
)
out.request("uk", "vk", "sst", "temp", "salt", "zt")

# Run the simulation
start = datetime.datetime(2020, 1, 1)
stop = datetime.datetime(2020, 1, 3)
timestep = domain.maxdt * 0.8
sim.start(start, timestep=timestep, split_factor=30, report=int(3600 / timestep))
while sim.time < stop:
    sim.advance()
sim.finish()
