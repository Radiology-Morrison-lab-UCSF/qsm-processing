FROM vnmd/qsmxt_8.2.2:20260105
LABEL maintainer="UCSF Morrison Lab: Eric.Cito@ucsf.edu"
LABEL version=2.0
LABEL description="QSMxT version 8.2.2, with an additional skull stripping step and real/imaginary dicom conversion"


RUN ls /dev
RUN apt-get update && apt-get install -y bash
SHELL ["/bin/bash", "-c"]

RUN apt install -y software-properties-common && add-apt-repository -y 'ppa:deadsnakes/ppa' && apt-get update -y && apt-get upgrade -y && apt-get install dcm2niix wget git -y 
COPY . /opt/
WORKDIR /opt

RUN /opt/install.sh


ENTRYPOINT [ "/opt/process-qsm.sh" ]

