# AI-coin-detector
 
## Installation

### NOTICE
Use `python` or `python3.11` as an alternative to `py` command if not working correctly and for python version conflicts. Same goes for `pip` and `pip3.11`.

1. Clone the repository
```cmd
git clone https://github.com/Seanneskie/AI-coin-detector-django
```

2. Navigate to the project directory

3. Create an Virtual Environment named "env" folder
```py
py -m venv env
```

4.  Activate the virtual environment (if applicable)
```cmd
env\Scripts\activate.bat
```
or
```ps1
env\Scripts\activate.ps1
```

5. Install dependencies
```py
pip install -r requirements.txt
```

6. Go to project directory
```cmd
cd myproject
```

7. Migrate
```py
py manage.py migrate
```

8. Run webserver
```py
py manage.py runserver
```

9. Go to 127.0.0.1:8000


## Running on Mobile

6. Repeat Step 1 - 7

7. Run Webserver
```py
py manage.py runserver 0.0.0.0:8000
```

8. Get your IPv4 Address in Command Prompt using `ipconfig`

9. Add your IPv4 Address in Allowed Connection in myproject/settings.py. 
```py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.56.1', '192.168.1.7', '192.168.80.160']
```

11. Go to your Mobile Browser and run `IPv4 Address:8000` For Example: `192.168.1.7:8000`