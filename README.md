# Open-Weather-API-Wrapper

This project is a wrapper of Open Weather API.

## Install requirements

Create a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install all requirements.

```bash
pip install -r requirements.txt
```

### Setting environmental variables

Create a file called `.env` with environmental variables.

```text
OPEN_WEATHER_API_KEY=<API KEY>
DEFAULT_MAX_NUMBER=<time interval>
```

### Running our API

```bash
python run.py
```

## Running our unit tests

Install requirements for development.

```bash
pip install -r requirements-dev.txt
```

Then run next command inside the project path.

```bash
py.test
```