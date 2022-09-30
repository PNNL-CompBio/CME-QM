FROM continuumio/anaconda3:latest
ARG BUILD_DATE
#ARG VCS_REF
ARG BUILD_VERSION

# Labels:
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="DarpaCME"
LABEL org.label-schema.description=""
LABEL org.label-schema.url=""
LABEL org.label-schema.vcs-url="https://gitlab.pnnl.gov/computational_data_science/darpacme"
#LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="Pacific Northwest National Laboratory"
LABEL org.label-schema.version=$BUILD_VERSION
LABEL maintainer="Anubhav <anubhav@pnnl.gov>"
LABEL tags="ComputationalChemistry"

# Install necessary tools
RUN apt-get update \
    && apt-get install --no-install-recommends --yes  wget bzip2 ssh python-dev gfortran libopenblas-dev libopenmpi-dev bc \
    openmpi-bin tcsh make openbabel \
    && apt-get clean

#get OpenBLAS and compile with 64-bit integers

ENV         NWCHEM_TOP="/opt/nwchem-6.8.1" \
            NWCHEM_TARGET=LINUX64 \
            BLASOPT="-lopenblas -lpthread -lrt" \
            BLAS_SIZE=4 \
            USE_64TO32=y \
            NWCHEM_MODULES="smallqm" \
            USE_MPI=y \
            USE_MPIF=y \
            USE_MPIF4=y

#Build NWChem source.
RUN cd opt \
    && wget https://github.com/nwchemgit/nwchem/releases/download/6.8.1-release/nwchem-6.8.1-release.revision-v6.8-133-ge032219-srconly.2018-06-14.tar.bz2 \
    && tar -vxjf nwchem-6.8.1-release.revision-v6.8-133-ge032219-srconly.2018-06-14.tar.bz2 \
    && rm nwchem-6.8.1-release.revision-v6.8-133-ge032219-srconly.2018-06-14.tar.bz2 \
    && cd ${NWCHEM_TOP}/src \
    && make nwchem_config \
    && make 64_to_32 \
    && make -j3

# Install python dependencies
COPY cme_environment.yml ./
RUN conda create --name cme_env python=3.7
SHELL ["conda", "run", "-n", "cme_env", "/bin/bash", "-c"]
RUN conda env update -n cme_env -f cme_environment.yml && \
    echo "conda activate cme_env" >> ~/.bashrc && \
    conda clean --all

#clean unnecessary packages
RUN  apt-get -y remove  make \
                        curl \
                        subversion \
                        unzip \
                        cmake \
                        perl \
                        tcsh ssh gfortran  python-dev libopenmpi-dev  \
     &&  apt-get -y autoremove && apt-get clean

# Setting up NWchem path!
# No need to specify path explicitly for :
# nwchem
ENV         NWCHEM_EXECUTABLE=${NWCHEM_TOP}/bin/LINUX64/nwchem \
            NWCHEM_BASIS_LIBRARY=${NWCHEM_TOP}/src/basis/libraries/ \
            NWCHEM_NWPW_LIBRARY=${NWCHEM_TOP}/src/nwpw/libraryps/  \
            FFIELD=amber \
            AMBER_1=${NWCHEM_TOP}/src/data/amber_s/ \
            AMBER_2=${NWCHEM_TOP}/src/data/amber_q/ \
            AMBER_3=${NWCHEM_TOP}/src/data/amber_x/ \
            AMBER_4=${NWCHEM_TOP}/src/data/amber_u/ \
            SPCE=${NWCHEM_TOP}/src/data/solvents/spce.rst \
            CHARMM_S=${NWCHEM_TOP}/src/data/charmm_s/ \
            CHARMM_X=${NWCHEM_TOP}/src/data/charmm_x/ \
            PATH=$PATH:${NWCHEM_TOP}/bin/LINUX64

# Setting up Conda Path
# No need to specify path explicitly for :
#   conda packages: snakemake,
#   Amber20 tools : tleap antechamber parmchk2 sander
ENV         CONDA_PATH="/opt/conda/envs/cme_env"
ENV         LEAPRC_GAFF=$CONDA_PATH/dat/leap/cmd/leaprc.gaff \
            LEAPRC_FF14SB=$CONDA_PATH/dat/leap/cmd/oldff/leaprc.ff14SB \
            PATH=$CONDA_PATH/bin:$PATH

WORKDIR /