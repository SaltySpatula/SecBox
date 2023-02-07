# SecBox
SecBox tool; a lightweight, container based malware analysis sandbox.
Requires Python version 3.9.

## Frontend Setup
The frontend requires [Node 16.X](https://www.stewright.me/2022/01/tutorial-install-nodejs-16-on-ubuntu-20-04/) and
 [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/#debian-stable). To install the dependencies go to 
```
├── SecBox
│   ├── app
```           
and run `npm install`. Create a .env file with the value VUE_APP_ROOT with the desired backend IP, e.g. `VUE_APP_ROOT="localhost:5000"` for if you are running it locally.

## Backend Setup
The backend requires [python 3.9](https://www.python.org/downloads/release/python-390/) and [pip](https://pip.pypa.io/en/stable/installation/).
All dependencies required for the backend can be installed in
```
├── SecBox
│   ├── api
``` 
with `pip install -r requirements.txt`.

To add a [mongo DB](https://www.mongodb.com/), a .env file in this directory must be configured:
```
DB_PORT= "27017"
HOST_BITNESS= 64
HOST="mongodb+srv://"
DB= "DB?"
```




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


## Demo Video
A demo is available on YouTube:
https://www.youtube.com/watch?v=lkEE3iQvFtk
