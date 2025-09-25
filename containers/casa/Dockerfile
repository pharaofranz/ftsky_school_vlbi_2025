FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget python3-pip ipython3 emacs curl git gfortran \
    libfuse2 ca-certificates \
    python3-sphinx libcasa-tables6 libgomp1 libhdf5-103 \
    casacore-data casacore-dev casacore-tools python3-casacore \
    pkg-config tzdata unzip \
    software-properties-common gnupg2 kmod \
    wsclean aoflagger
RUN apt-add-repository -y ppa:cartavis-team/carta && \
    apt-get update && \
    apt-get install -y carta

#RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN python3 -m pip install -U astropy numpy matplotlib scipy mpi4py pyyaml \
cython pyuvdata uvtools python-casacore setuptools

# Download and install CASA (make sure the URL is appropriate for Ubuntu)
#RUN wget --no-check-certificate https://casa.nrao.edu/download/distro/casa/release/rhel/casa-6.6.0-20-py3.8.el7.tar.xz && \
ADD casa-6.6.0-20-py3.8.el7.tar.xz ./
#RUN tar xf casa-6.6.0-20-py3.8.el7.tar.xz && \
#    rm -rf casa-6.6.0-20-py3.8.el7.tar.xz
# Add CASA to the PATH
ENV PATH="/casa-6.6.0-20-py3.8.el7/bin:$PATH"
ENV LC_ALL=C.UTF-8

RUN mkdir /data

#RUN apt-add-repository universe && \
#    apt-get update && \
#    apt-get install -y libfuse2
#
RUN apt-get install -y fuse

RUN modprobe fuse