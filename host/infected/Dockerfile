# syntax=docker/dockerfile:1
# setup ubuntu version
ARG os_image
ARG malware_hash=""
FROM $os_image

#setup wget and 
# RUN sudo apt-get update && sudo apt-get install -y wget && sudo apt-get install -y p7zip-full p7zip-rar
RUN apt update && apt install -y wget
RUN wget -O malware.html --post-data query="get_file&sha256_hash=$malware_hash" https://mb-api.abuse.ch/api/v1/
# RUN 7z e -pinfected malware.html
# RUN apt-get uninstall -y unzip && apt-get uninstall -y wget