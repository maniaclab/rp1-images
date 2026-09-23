# rp1-images

Container images for the Research Platform 1 (RP1) JupyterHubs, including the Open Data
Facility (ODF) at `jupyterhub.odf.uchicago.edu`, deployed from
[maniaclab/rp1-core](https://github.com/maniaclab/rp1-core). There are two kinds:

- **Notebook images** (`base`, `coffea`, `opendata`): user environments.
- **Platform images** (`hub`): components of the hub itself.

## The notebook-image contract

Every notebook image here can run **both** a user's notebook **and** that notebook's scale-out
workers. On ODF, Dask Gateway clusters default to the image the notebook was spawned with
(`JUPYTER_IMAGE_SPEC`), so client and worker package versions match by construction. There's
no second worker image to keep in sync, and no `PipInstall` onto workers at runtime. So every
notebook image includes:

| Package | Why |
|---|---|
| `dask-gateway`, `distributed` | Dask Gateway client in the notebook; `dask-scheduler`/`dask-worker` on cluster pods |
| `ndcctools` | TaskVine manager in the notebook |
| `taskvine-gateway` (client) | `TaskVineCluster`: self-service TaskVine worker pools |

## Images

| Image | Built on | For |
|---|---|---|
| `ghcr.io/maniaclab/rp1-images/hub` | z2jh `k8s-hub` 4.4.2 | Hub image with [jupyterhub-fancy-profiles](https://github.com/2i2c-org/jupyterhub-fancy-profiles) (profile picker + BinderHub builds), for every RP1 cluster |
| `ghcr.io/maniaclab/rp1-images/base` | AlmaLinux 9 + pixi env `base` (Python 3.12) | Minimal starting point; ODF's fallback Dask image |
| `ghcr.io/maniaclab/rp1-images/coffea` | AlmaLinux 9 + pixi env `coffea` | coffea 2025.12 columnar stack: [integration-challenge](https://github.com/iris-hep/integration-challenge) (ATLAS + CMS) and [AGC](https://github.com/iris-hep/analysis-grand-challenge) `latest` |
| `ghcr.io/maniaclab/rp1-images/opendata` | [ATLAS Open Data notebooks](https://github.com/atlas-outreach-data-tools/notebooks-collection-opendata) image | ATLAS Open Data tutorials (ROOT, coffea 0.7, atlasopenmagic) |

## Environments (pixi)

`base` and `coffea` are pixi environments in one workspace, `envs/pixi.toml`, with one
lock, `envs/pixi.lock`. Each image installs its environment with `pixi install --locked`,
so an image contains exactly what the lock says. The workspace is built from features:

| Feature | What | Who changes it |
|---|---|---|
| `platform` | `dask-gateway`, `ndcctools`, `jupyterhub-singleuser`, `xrootd`, `taskvine-gateway` client: versions coupled to services rp1-core runs | Only together with the matching rp1-core change |
| `notebook` | JupyterLab, ipykernel, Dask runtime | Freely |
| `coffea` | The analysis stack | Freely; exact pins follow `integration-challenge/cms/pixi.lock` |

All environments share one `solve-group`, so a package two images both carry has the same
version in both. To change an environment, edit `envs/pixi.toml` and run `pixi lock` in
`envs/`. You can also use it outside Docker: `pixi shell -e coffea` gives the same environment
the image has.

`coffea`'s `histserv` client matches ODF's histserv server.

Not covered: AGC's legacy `cms-open-data-ttbar` environment (coffea 0.7 on Python 3.9).

## Tags

Images are tagged `tree-<hash>`, where the hash is the git tree hash of `images/<name>/`
(`scripts/image-tag <name>`). It depends only on that directory's contents, so an image whose
tag is already in the registry is unchanged and CI skips it. There's no changed-files action to
maintain or trust. `latest` follows `main`, but nothing should deploy from it.

For `base` and `coffea`, the hash also covers `envs/`, so changing the lock gives both new
tags. If an image is ever built `FROM` another image here, it must pin that parent's current
tag. CI builds parents first, and fails if the `FROM` is stale.

## Workflow

Modelled on [vre-hub/environments](https://github.com/vre-hub/environments): images publish
from `main` only.

1. Open a PR editing `envs/` or `images/<name>/`. Keep the `platform` pins in step with
   `opendata/Dockerfile` (which can't use the pixi workspace) and with their upstreams
   (noted inline).
2. CI runs `scripts/build-images` on the PR. It builds every changed image and runs its
   `smoke-test.py` inside it, **without pushing**. Run the same script locally if you have
   Docker.
3. Merge. CI builds again on `main` and pushes `tree-<hash>`.
4. In rp1-core, pin the new tag (`scripts/image-tag <name>` on `main`):
   - notebook images: the cluster's `patch-singleuser-image.yaml` profile choices, plus
     `gateway.backend.image` in the dask-gateway patch for `base`
   - `hub`: `hub.image`, next to a jupyterhub chart version equal to the image's `Z2JH_VERSION`

Packages are private (org policy). ODF pulls them with an image pull secret.
