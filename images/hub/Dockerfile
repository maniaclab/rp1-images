# hub: z2jh's hub image plus 2i2c's jupyterhub-fancy-profiles (the profile
# picker UI with BinderHub image building), for all RP1 clusters.
#
# 2i2c's own prebuilt image (quay.io/yuvipanda/z2jh-hub-with-fancy-profiles)
# only ships for z2jh 4.3.1. Their Dockerfile just layers the wheel onto
# k8s-hub, so we do the same here and choose the z2jh version ourselves.
# fancy-profiles pins no jupyterhub/kubespawner version; it hooks in only via
# KubeSpawner.additional_profile_form_template_paths and a static handler.
#
# Keep Z2JH_VERSION equal to the jupyterhub chart version in rp1-core
# (infrastructure/jupyterhub/helmrelease.yaml, or a cluster's overlay patch).
ARG Z2JH_VERSION=4.4.2
ARG HUB_DIGEST=sha256:108fbb01c3fe23e4a81efc8899aa73b4c15413615c73dfcdc44248eb63096e41

# Needs node/npm to build the frontend, which the final image doesn't carry.
FROM quay.io/jupyterhub/k8s-hub:${Z2JH_VERSION}@${HUB_DIGEST} AS builder
USER root
RUN apt-get update >/dev/null \
    && apt-get install --yes --no-install-recommends git nodejs npm >/dev/null

# Pinned to a main commit rather than the v0.6.0 release, which predates
# build-then-autostart and permalinks for BinderHub builds.
ARG FANCY_PROFILES_REF=6e67df8566185594c9c186ce4e20d8c70b7c9cff
RUN git clone https://github.com/2i2c-org/jupyterhub-fancy-profiles /srv/repo \
    && git -C /srv/repo checkout "${FANCY_PROFILES_REF}" \
    && pip install --no-cache-dir build \
    && python -m build /srv/repo --wheel --outdir /srv/wheels/

FROM quay.io/jupyterhub/k8s-hub:${Z2JH_VERSION}@${HUB_DIGEST}
USER root
COPY --from=builder /srv/wheels/*.whl /srv/wheels/
RUN pip install --no-cache-dir /srv/wheels/*.whl && rm -rf /srv/wheels
USER ${NB_USER}
