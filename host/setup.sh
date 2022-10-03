#setup python and pip
sudo apt-get update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.9
sudo apt-get install -y python3-pip

#setup docker repository
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p -y /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

#setup docker engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
#setup bazel
sudo apt install apt-transport-https curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

sudo apt update && sudo apt install bazel
sudo apt update && sudo apt full-upgrade
#setup gvisor
sudo apt-get update
sudo apt-get install unzip
wget https://github.com/google/gvisor/archive/refs/heads/master.zip
unzip master.zip
cd gvisor-master
mkdir -p bin
make copy TARGETS=runsc DESTINATION=bin/
sudo cp ./bin/runsc /usr/local/bin

sudo /usr/local/bin/runsc install
sudo systemctl reload docker

#setup sandbox- and trace-specific runtimes
sudo runsc install --runtime=runsc-trace-infected -- --pod-init-config=$PWD/infected/session.json
sudo runsc install --runtime=runsc-trace-healthy -- --pod-init-config=$PWD/healthy/session.json
sudo systemctl restart docker

#install dependencies
pip3 install -r requirements.txt