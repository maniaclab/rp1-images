# base

AlmaLinux 9 plus the pixi environment `base` (`envs/pixi.toml`): the `platform` feature
(`dask-gateway`, `ndcctools` for TaskVine, the `taskvine-gateway` client, XRootD) and the
`notebook` feature (JupyterLab, the Dask runtime). It runs as `jovyan` (1000:100). Start from
this image when you're building a new environment. ODF also uses it as the fallback Dask
scheduler/worker image.
