# coffea: the columnar analysis stack for the IRIS-HEP Integration Challenge
# and AGC, on top of base's platform clients. The pixi environment "coffea"
# in envs/pixi.toml defines it, sharing one solve-group (so identical
# platform versions) with base.
#
# Built with the repository root as context (see scripts/build-images).
# images/base/Dockerfile is the same file apart from ENV_NAME; keep the two
# in step.
ARG ENV_NAME=coffea

FROM ghcr.io/prefix-dev/pixi:0.81.0-noble@sha256:788ae451641666e2d1f79d3dbe35392dfc7e9b394b16a3acb75c347f3badb2ab AS build
ARG ENV_NAME
# A conda prefix isn't relocatable, so install at the exact path the final
# image uses.
WORKDIR /opt/rp1
COPY envs/pixi.toml envs/pixi.lock ./
RUN pixi install --locked -e "${ENV_NAME}" \
    && pixi shell-hook --locked -e "${ENV_NAME}" > /opt/rp1/activate.sh \
    && rm -rf /root/.cache/rattler

# AlmaLinux 9, the EL9 distribution CERN and Fermilab standardized on (also
# SWAN's and coffea-casa's base). EL9 matters for what lives outside the
# pixi environment: LCG views and experiment software on CVMFS are built for
# el9, and grid tooling ships as EL RPMs.
FROM almalinux:9@sha256:3a3fa7f043b142bc8008c8b308d39b47d2c84008addcd52f9f9a7a82d2a90474
ARG ENV_NAME
ARG BUILD_DATE
LABEL org.opencontainers.image.created=$BUILD_DATE

# tini comes from the pixi environment (conda-forge), not EPEL.
RUN dnf install -y --setopt=install_weak_deps=False git-core >/dev/null \
    && dnf clean all \
    && rm -rf /var/cache/dnf

# jovyan/1000:100 is what z2jh's singleuser defaults (uid 1000, fsGroup 100)
# and docker-stacks images assume. EL's "users" group is gid 100.
RUN useradd --create-home --uid 1000 --gid 100 --shell /bin/bash jovyan

COPY --from=build /opt/rp1/.pixi/envs/${ENV_NAME} /opt/rp1/.pixi/envs/${ENV_NAME}
COPY --from=build /opt/rp1/activate.sh /opt/rp1/activate.sh

# Activated statically rather than through an entrypoint, because
# KubeSpawner and dask-gateway both set the container command. Nothing in
# these environments relies on activate.d scripts. activate.sh is kept for
# interactive shells (`source /opt/rp1/activate.sh`).
ENV CONDA_PREFIX=/opt/rp1/.pixi/envs/${ENV_NAME} \
    PATH=/opt/rp1/.pixi/envs/${ENV_NAME}/bin:${PATH} \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    SHELL=/bin/bash

USER 1000:100
WORKDIR /home/jovyan
EXPOSE 8888
ENTRYPOINT ["tini", "-g", "--"]
CMD ["jupyterhub-singleuser"]
