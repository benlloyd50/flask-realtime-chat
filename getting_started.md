# Getting Started for developers
*Depending on your setup you may have to use `python3` rather than `python`*

## First time setup
```
git clone https://github.com/benlloyd50/flask-realtime-chat.git

python -m venv venv

# For Mac/Unix
. venv/bin/activate
# For Windows
venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

flask init-db
flask run
```

## Everytime after
```
# Everytime terminal is restarted you must start the virtual environment
# (venv) means it is active and will appear on the command line
# For Mac/Unix
. venv/bin/activate
# For Windows
venv\Scripts\Activate.ps1

# if you made changes to the schema rebuild the db, this will wipe old data
flask init-db

flask run
# or with debug and lan network accessibility
flask --debug run --host=0.0.0.0
```

## Common Faults
- If you need to deactivate the venv then run `deactivate`
- Check if your venv is running, you will see `(venv)` in your terminal
- Make sure you have an instance folder with a vox.sqlite file, or else you didn't make the database correctly