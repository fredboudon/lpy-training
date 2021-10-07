FROM jupyter/base-notebook:lab-3.1.13

ARG NB_USER=jovyan
ARG NB_UID=1000

COPY ../environment.yml /home/${NB_USER}/environment.yml

USER root
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install --no-upgrade --no-install-recommends -y git libgl1-mesa-dev && \
    mamba env update -n base -f /home/${NB_USER}/environment.yml && \
    jupyter lab build && \
    mamba clean -y --all --force-pkgs-dirs && \
    jupyter lab clean && \
    jlpm cache clean && \
    npm cache clean --force && \
    apt-get remove -y git && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -fr /tmp/*

USER 1000
WORKDIR $HOME
# RUN rm -fr work
ENTRYPOINT []
