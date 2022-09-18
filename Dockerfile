# use the ROOT 6.22 tag as base
FROM rootproject/root:6.22.00-ubuntu20.04 as base
SHELL ["/bin/bash", "-c"]
# pre-emptively set environment variables needed for TIMBER
ENV BOOSTPATH /usr/lib/x86_64-linux-gnu
ENV LD_LIBRARY_PATH $BOOSTPATH
# update package manager, install packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    graphviz \
    libgraphviz-dev \
    libboost-all-dev \
    vim \
    git && \
    # set up TIMBER (python3, courtesy of Matej)
    # kind of redundant to set up a virtual env in a container, but TIMBER requires this step..
    python3 -m pip install virtualenv && \
    python3 -m virtualenv timber-env && \
    git clone --branch Zbb_branch_py3 https://github.com/mroguljic/TIMBER.git && \
    cd TIMBER && mkdir bin && cd bin && \
    git clone https://github.com/fmtlib/fmt.git && \
    cd ../../ && \
    . ./timber-env/bin/activate && \
    cd /opt/TIMBER && \
    echo $VIRTUAL_ENV && \
    . ./setup.sh

# create app layer
FROM base as app
# Run the following commands as super user (root):
USER root
# Create a user that does not have root privileges
ARG username=physicist
RUN useradd --create-home --home-dir /home/${username} ${username}
ENV HOME /home/${username}
ENV TIMBERPATH /opt/TIMBER
# Switch to our newly created user
USER ${username}
# Our working directory will be in our home directory where we have permissions
WORKDIR /home/${username}
COPY setup.sh setup.sh
ENTRYPOINT ["/bin/bash"]
