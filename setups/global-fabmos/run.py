import cftime
import os

import numpy as np
import fabmos.transport.tmm
import fabmos

calendar = "360_day"  # any valid calendar recognized by cftime, see https://cfconventions.org/cf-conventions/cf-conventions.html#calendar

domain = fabmos.transport.tmm.create_domain(".")

sim = fabmos.transport.tmm.Simulator(domain, calendar=calendar, fabm="fabm.yaml")

def estimate_diffusivity():
    # Crude estimate of turbulent diffusivity from temperature-only MLD
    # PISCES and iHAMOCC use this to determine turbocline depth
    temp = fabmos.transport.tmm.get_mat_array(
        "GCM/Theta_gcm.mat",
        "Tgcm",
        domain._grid_file,
        times=fabmos.transport.tmm.climatology_times(calendar),
    )
    Kzval = np.where(temp.values < temp.values[:, :1, :, :] - 0.5, 1e-5, 1e-3)
    return fabmos.transport.tmm._wrap_ongrid_array(
        Kzval, domain._grid_file, times=fabmos.transport.tmm.climatology_times(calendar)
    )

# Here we can add dependencies for FABM as needed.
# For example:
# sim.fabm.get_dependency("surface_air_pressure").set(101325.0)
# sim.fabm.get_dependency("mole_fraction_of_carbon_dioxide_in_air").set(280.0)
# sim.fabm.get_dependency("absorption_of_silt").set(0.02)
# sim.fabm.get_dependency("bottom_stress").set(0.0)

# Non-constant dependencies can be used too, e.g., for diffusivity in PISCES and iHAMOCC:
# sim.fabm.get_dependency("vertical_tracer_diffusivity").set(
#     estimate_diffusivity(), on_grid=fabmos.input.OnGrid.ALL, climatology=True
# )

out = sim.output_manager.add_netcdf_file(
    "output.nc", interval=5, interval_units=fabmos.TimeUnit.DAYS, save_initial=False
)
out.request(*sim.fabm.state_variables, time_average=True)

start = cftime.datetime(2000, 1, 1, calendar=calendar)
stop = cftime.datetime(2001, 1, 1, calendar=calendar)
sim.start(start, timestep=3600, transport_timestep=12 * 3600)
while sim.time < stop:
    sim.advance()
sim.finish()
