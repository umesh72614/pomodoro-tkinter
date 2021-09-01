# import subprocess, os
import os
from utility import get_base_path, get_path

VENV_PATH = get_path('venv')
PYTHON_PATH = get_path('venv/bin/python3')
PIP_PATH = get_path('venv/bin/pip3')
REQUIREMENTS_PATH = get_path('requirements.txt')
APP_PATH = get_path('app.py')
# print(f'py: {PYTHON_PATH}\npip: {PIP_PATH}\nreq: {REQUIREMENTS_PATH}\napp: {APP_PATH}')
if (not os.path.exists(PYTHON_PATH)):
    os.system(f"python3 -m venv {VENV_PATH}")
    os.system(f"{PIP_PATH} install -r {REQUIREMENTS_PATH}")
else:
    print('venv and requirements are already ready! Starting the App!')

os.chdir(get_base_path())
# subprocess.Popen([PYTHON_PATH, APP_PATH])
os.system(f'{PYTHON_PATH} {APP_PATH}')
