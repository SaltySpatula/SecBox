# SecBox
SecBox tool; a lightweight, container based malware analysis sandbox.
Requires Python version 3.9.

## Frontend Setup


## Backend Setup
All dependencies required for the backend can be installed by running:
```
pip install -r requirements.txt
```

The backend can be run the following way, from the api directory:
```
python3 webapp_api.py
```

## Host Setup
In order to set up the host on a machine, run:

```
sudo ./setup.sh
sudo ./setup_bazel_gvisor.sh
```

The host can then be run from the host directory by running:

```
sudo python3 ./host.py
```


## Configuration
Configuration happens through the respective .env files for the respective system components.
