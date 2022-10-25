## Installation

It's recommended to set up a [venv](https://docs.python.org/3/library/venv.html). Then install the dependencies from the `requirements.txt`

### Bash (Linux)
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Powershell (Windows)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Just execute the `main.py`

### Configuration [Optional]
The configuration can be passed in via environment variables.

```sh
JIRA_HOST=jira.example.com JIRA_USER=username python main.py
```

## Inspiration

This project was inspired by
[github.com/ussserrr/jira-worklogs](https://github.com/ussserrr/jira-worklogs).