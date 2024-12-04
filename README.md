# OPAN 3244 Final
## Made by Brooke O'Donnell, Colin McKenna, and Elliot Landolt

## Setup (running on your local PC)

Create a virtual environment (first-time only):
```sh
conda create -n reports-env python=3.10
```

Activate the environment (whenever you come back):
```sh
conda activate reports-env
```

To install the required packages for local testing:
```sh
pip install -r requirements.txt
```

## Usage (local)

To run individual python scripts use
```sh
python -m app.[insertscriptname]
```

To run our web-app
```sh
flask run
```

## Testing