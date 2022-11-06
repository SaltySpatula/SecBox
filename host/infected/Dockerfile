# syntax=docker/dockerfile:1
# setup ubuntu version
ARG os_image
FROM $os_image

#setup python and pip
RUN apt-get update
RUN apt-get upgrade
#ARG malware_hash
#RUN malware_hash_var=malware_hash
#RUN wget --post-data "query=get_file&sha256_hash=${malware_hash_var}" +malware_hash https://mb-api.abuse.ch/api/v1/