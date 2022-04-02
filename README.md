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

## Setting environmental variables

A file called `.env` should be created with environmental variables.

```text
OPEN_WEATHER_API_KEY=<API KEY>
DEFAULT_MAX_NUMBER=<time interval>
```

### Running our API

```bash
python run.py
```
