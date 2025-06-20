import eatpy
import numpy as np
rng = np.random.default_rng()

N = 20

# Vary physical model configuration (gotm.yaml) across the ensemble by
# applying log-normally distributed scale factors to
# * wind speeds (x and y components)
# * background mixing (minimum turbulent kinetic energy)
gotm = eatpy.models.gotm.YAMLEnsemble("gotm.yaml", N)
with gotm:
    gotm["surface/u10/scale_factor"] = rng.lognormal(mean=0.0, sigma=0.2, size=N)
    gotm["surface/v10/scale_factor"] = rng.lognormal(mean=0.0, sigma=0.2, size=N)
    gotm["turbulence/turb_param/k_min"] = 1e-6 * rng.lognormal(mean=0.0, sigma=0.2, size=N)
