1. Activate the virtual environment
cd into the current folder and run
- On Windows
python -m venv venv
venv\Scripts\activate

- On macOS and Linux
python3 -m venv venv
source venv/bin/activate

2. Install all the libraries required that are listed in the requirements.txt
run pip install -r requirements.txt

3. Set the environment and execute the main.py file
run these commands
- On Windows
set FLASK_APP=app.py
set FLASK_ENV=development
flask run

- On macOS and Linux
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
