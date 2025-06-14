import cftime
import os
import datetime

import fabmos
import fabmos.transport.tmm
import fabmos.input.riverlist

import pandas as pd

script_dir = os.path.dirname(__file__)
tm_config_dir = os.path.join(script_dir, "../../setups/global-fabmos")
calendar = "360_day"  # any valid calendar recognized by cftime, see https://cfconventions.org/cf-conventions/cf-conventions.html#calendar

fabm_yaml = os.path.join(
    script_dir, "../../code/fabm/extern/mops/testcases/fabm_with_runoff.yaml"
)

domain = fabmos.transport.tmm.create_domain(tm_config_dir)

sim = fabmos.transport.tmm.Simulator(domain, calendar=calendar, fabm=fabm_yaml)

sim.fabm.get_dependency("mole_fraction_of_carbon_dioxide_in_air").set(280.0)
sim.fabm.get_dependency("surface_air_pressure").set(101325.0)

# Load rivers from https://doi.org/10.1029/96JD00932
rivers = pd.read_fwf(
    os.path.join(script_dir, "../../code/fabmos/examples/tmm/rivrstat.txt"),
    skiprows=7,
    usecols=(1, 2, 3, 4, 6),
    names=("name", "country", "lat", "lon", "flow"),
)

# Exclude Arctic rivers as in https://doi.org/10.5194/bg-10-8401-2013
rivers = rivers.loc[rivers.lat <= 60.0]

# Convert river list to gridded [2D] river inputs (level increase in m s-1)
runoff = fabmos.input.riverlist.map_to_grid(sim.T, rivers.lon, rivers.lat, rivers.flow)

# Reintroduce buried phosphorus, weighted by river runoff
# (https://doi.org/10.5194/bg-10-8401-2013)
sim.request_redistribution(
    "det/burial", "runoff/source", runoff, datetime.timedelta(days=360)
)

out = sim.output_manager.add_netcdf_file(
    "output.nc", interval=1, interval_units=fabmos.TimeUnit.MONTHS, save_initial=False
)
out.request("runoff_source", *sim.fabm.default_outputs, time_average=True)

start = cftime.datetime(2000, 1, 1, calendar=calendar)
stop = cftime.datetime(2000, 2, 1, calendar=calendar)
sim.start(start, timestep=12 * 3600)
while sim.time < stop:
    sim.advance()
sim.finish()
