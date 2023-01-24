#setup bazel
sudo apt install apt-transport-https curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

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
cd ../
sudo /usr/local/bin/runsc install
sudo systemctl reload docker

#setup sandbox- and trace-specific runtimes
sudo runsc install --runtime=runsc-trace-infected -- --pod-init-config=$PWD/infected/session.json
sudo runsc install --runtime=runsc-trace-healthy -- --pod-init-config=$PWD/healthy/session.json
sudo systemctl restart docker

#install dependencies
sudo pip3 install -r requirements.txt