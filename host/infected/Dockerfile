# syntax=docker/dockerfile:1
# setup ubuntu version
ARG os_image
ARG malware_hash=""
FROM $os_image

#setup python and pip
#RUN  apt-get update && apt-get install -y wget && apt-get install -y unzip
#RUN wget -O malware.html --post-data query="get_file&sha256_hash=$malware_hash" https://mb-api.abuse.ch/api/v1/
#RUN unzip -P infected malware.html