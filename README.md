# magistracy-invest-service

Magistracy project KubSU
## installation

1. Create virtual environment `python3.8 -m venv venv`
2. Activate virtual environment `source venv/bin/activate`
3. Install all dependencies `pip install -r requirements.txt`
4. Copy and edit config file `cp example.config.py conf.py`

## Launch app
* Launch API `python run.py`
* Launch worker to update rates`python worker.py`

## Other
* URL for API in GUI http://127.0.0.1:5000/api/v1/ui ;