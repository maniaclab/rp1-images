# hub

The z2jh hub image (`quay.io/jupyterhub/k8s-hub`) plus [jupyterhub-fancy-profiles](https://github.com/2i2c-org/jupyterhub-fancy-profiles),
2i2c's profile picker with BinderHub image building. Used by every RP1 cluster's JupyterHub.
It replaces 2i2c's prebuilt image, which only ships for z2jh 4.3.1. `Z2JH_VERSION` here must
match the jupyterhub chart version deployed in rp1-core.
