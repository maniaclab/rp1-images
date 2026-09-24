# Run by CI inside the built image (not copied into it): everything the
# notebook<->worker contract depends on must import from the default Python.
import dask, distributed, dask_gateway, ndcctools.taskvine, taskvine_gateway, fsspec_xrootd, XRootD

print("dask", dask.__version__, "distributed", distributed.__version__, "dask_gateway", dask_gateway.__version__)

# The commands dask-gateway's KubeClusterConfig runs on scheduler/worker pods.
import shutil
missing = [c for c in ("dask-scheduler", "dask-worker") if not shutil.which(c)]
assert not missing, f"missing on PATH: {missing}"

# The Dask JupyterLab extension (sidebar, dashboard panes) must be installed
# and enabled in the image's JupyterLab.
import subprocess
out = subprocess.run(["jupyter", "labextension", "list"], capture_output=True, text=True)
listing = out.stdout + out.stderr
line = next((l for l in listing.splitlines() if "dask-labextension" in l), "")
assert "enabled" in line and "OK" in line, f"dask-labextension not enabled:\n{listing}"
print(line.strip())
