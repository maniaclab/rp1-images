# odf-opendata: the ATLAS Open Data notebooks image plus odf-base's
# scale-out clients (upstream ships none of distributed, dask-gateway or
# ndcctools). It can't share odf-base's FROM, so it repeats that install here.
# Keep the pins in step with the platform feature in envs/pixi.toml.
#
# Base pinned by digest (upstream's :latest as of 2026-07-23). Bump it
# deliberately, not whenever upstream pushes.
FROM ghcr.io/atlas-outreach-data-tools/notebooks-collection-opendata@sha256:32bd27ecf61f28a7301103da4b1d7463809e82b68a32fe66892a6ded9ca34f4f

# Upstream leaves the image as root. /opt/conda is owned by jovyan (NB_UID),
# as in the docker-stacks image it derives from, and Dask workers running as
# root would write root-owned files into users' volumes.
USER ${NB_UID}

# --freeze-installed keeps the solver from rewriting the upstream env (much
# of which is pip-installed and invisible to it) just to satisfy these.
RUN mamba install -y -n base -c conda-forge --freeze-installed \
        "dask-gateway==2026.3.0" \
        "distributed" \
        "ndcctools==7.17.1" \
    && mamba clean -afy

RUN pip install --no-cache-dir \
        "taskvine-gateway @ git+https://github.com/maniaclab/taskvine-gateway@4ad5d3d7ccdff3b5146f2afceb5fd9f084877343"

# Upstream mixes conda packages with pip wheels in one env. Wheels (numpy,
# pandas, ...) link the system libstdc++ (Ubuntu 22.04: GCC 12), while conda's
# libarrow/pyarrow need conda's newer one (CXXABI_1.3.15). Whichever loads
# first wins for the whole process. Jupyter kernels happen to load conda's
# first (via pyzmq), but a plain `python` or `dask-worker` imports a numpy
# wheel first, and `import pyarrow` (awkward, uproot) then fails. Preloading
# conda's libstdc++ fixes every process; it's a superset of the system one,
# so wheels and system tools keep working.
ENV LD_PRELOAD=/opt/conda/lib/libstdc++.so.6
