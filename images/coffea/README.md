# coffea

AlmaLinux 9 plus the pixi environment `coffea` (`envs/pixi.toml`): `base`'s features plus
the coffea 2025.12 columnar stack (dask-awkward, uproot, hist, correctionlib, cabinetry/pyhf,
ServiceX, atlas-schema, atlasopenmagic, histserv, roastcoffea). It targets:

- [iris-hep/integration-challenge](https://github.com/iris-hep/integration-challenge) `atlas/` and `cms/`
- [iris-hep/analysis-grand-challenge](https://github.com/iris-hep/analysis-grand-challenge) `latest` environment

Pins follow `integration-challenge/cms/pixi.lock`. Because notebook and workers share this
image, the integration-challenge notebooks' `WORKER_DEPENDENCIES` / `PipInstall` step isn't
needed on ODF.
