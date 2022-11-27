# syntax=docker/dockerfile:1
# setup ubuntu version
ARG os_image
ARG malware_hash=""
FROM $os_image

#setup wget and 
RUN apt-get update 
RUN apt-get install -y wget 
RUN apt-get install -y p7zip-full p7zip-rar
RUN apt update && apt install -y wget