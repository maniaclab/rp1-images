# Run by CI inside the built image (not copied into it): everything the
# notebook<->worker contract depends on must import from the default Python.
import dask, distributed, dask_gateway, ndcctools.taskvine, taskvine_gateway

print("dask", dask.__version__, "distributed", distributed.__version__, "dask_gateway", dask_gateway.__version__)

# Upstream's own analysis stack must survive the install above. This runs
# in a plain `python` process, as Dask workers do, so it also catches the
# libstdc++ load-order problem LD_PRELOAD in the Dockerfile fixes.
import uproot, awkward, coffea, atlasopenmagic, ROOT
print("uproot", uproot.__version__, "coffea", coffea.__version__)

# The commands dask-gateway's KubeClusterConfig runs on scheduler/worker pods.
import shutil
missing = [c for c in ("dask-scheduler", "dask-worker") if not shutil.which(c)]
assert not missing, f"missing on PATH: {missing}"
