# Getting Started for developers
*Depending on your setup you may have to use `python3` rather than `python`*

## 0. Clone the repo
`git clone https://github.com/benlloyd50/flask-realtime-chat.git`

## 1. Setup Virtual Environment
It is good python practice to use them, the `requirements.txt` file tells you what libraries this project uses

#### Mac/Unix/Windows
```
python -m venv venv 
python -m pip install -r requirements.txt
```

## 2. Activate the Virtual Environment
Note this must be ran in your terminal everytime you start a new one. For most flavors of terminal you should see a tag that says `(venv)` which means you are running this venv
#### Mac/Unix
`. venv/bin/activate`
#### Windows
`source venv/bin/activate.bat`

*If you need to deactivate the venv then run `deactivate`*

## 3. Run the app
`python run.py` 

## 4. Complete
You should be up and running, if not please submit an issue