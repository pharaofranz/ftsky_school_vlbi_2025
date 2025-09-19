FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget build-essential python3-pip ipython3 emacs curl git gfortran \
    libfuse2 sudo cmake  make g++ gcc ca-certificates \
    python3-sphinx libcasa-tables6 libgomp1 libhdf5-103 \
    casacore-data casacore-dev casacore-tools python3-casacore ffmpeg libgsl-dev libfftw3-dev \
    libhdf5-dev libcfitsio-dev lcov libatlas3-base \
    libblas-dev libboost-date-time-dev libboost-filesystem-dev \
    libboost-program-options-dev libboost-system-dev libboost-test-dev \
    liberfa-dev libexpat1-dev libfontconfig-dev libfreetype-dev \
    liblapack-dev liblua5.3-dev libpng-dev libssl-dev \
    libxml2-dev pkg-config libpython3-dev pkg-config procps tzdata unzip \
    libopenmpi-dev openmpi-bin
RUN add-apt-repository -y ppa:cartavis-team/carta && \
    apt-get update && \
    apt-get install -y carta && \
RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN python3 -m pip install -U astropy numpy matplotlib scipy mpi4py pyyaml \
cython pyuvdata uvtools python-casacor setuptools

#aplpy mpi4py cubical stimela cult-cargo quartical pyrap pyyaml pygdsm aegeantools cycler cython seaborn shapely progressbar pyuvdata uvtools scikit-image healpy python-dateutil scikit-rf python-casacore pyfiglet astroquery pytoml setuptools

# Step 9: Install WSClean
ARG WSCLEAN_BRANCH=v3.4

RUN git clone --depth 1 https://gitlab.com/aroffringa/wsclean.git /wsclean && \
    cd /wsclean && \
    mkdir build && \
    cd build && \
    cmake $CMAKE_ARGS .. && \
    make install -j$(nproc) && \
    cd / && rm -rf /wsclean

# Step 10: Install AOFlagger
#ARG WSCLEAN_BRANCH=v3.0
RUN git clone --depth 1 https://gitlab.com/aroffringa/aoflagger.git /aoflagger && \
    cd /aoflagger && \
    mkdir build && \
    cd build && \
    cmake $CMAKE_ARGS .. && \
    make install -j$(nproc) && \
    cd / && rm -rf /aoflagger

# Download and install CASA (make sure the URL is appropriate for Ubuntu)
RUN wget --no-check-certificate https://casa.nrao.edu/download/distro/casa/release/rhel/casa-6.6.0-20-py3.8.el7.tar.xz && \
    tar xf casa-6.6.0-20-py3.8.el7.tar.xz && \
    rm -rf casa-6.6.0-20-py3.8.el7.tar.xz
# Add CASA to the PATH
ENV PATH="/casa-6.6.0-20-py3.8.el7/bin:$PATH"
ENV LC_ALL=C.UTF-8
