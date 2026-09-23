# Run by CI inside the built image (not copied into it).
import dask, distributed, dask_gateway, ndcctools.taskvine, taskvine_gateway, fsspec_xrootd, XRootD
import coffea, awkward, dask_awkward, dask_histogram, uproot, vector, numba, correctionlib, hist, mplhep
import cabinetry, pyhf, iminuit, servicex, servicex_analysis_utils, atlas_schema, atlasopenmagic
import histserv, roastcoffea, sklearn, xgboost, omegaconf, pydantic
from coffea.nanoevents import NanoEventsFactory

for m in (dask, distributed, coffea, awkward, dask_awkward, uproot, vector, numba, histserv):
    print(m.__name__, m.__version__)

# The commands dask-gateway's KubeClusterConfig runs on scheduler/worker pods.
import shutil
missing = [c for c in ("dask-scheduler", "dask-worker") if not shutil.which(c)]
assert not missing, f"missing on PATH: {missing}"
