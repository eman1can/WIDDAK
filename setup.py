from os import mkdir
from os.path import exists, join

import requests
import zipfile
import shutil

total, used, free = shutil.disk_usage(__file__)

kb = 1024
mb = kb * 1024
gb = mb * 1024
tb = gb * 1024

if free / gb < 10:
    print('Sorry, I don\'t want to clog your machine. Override me.')
    exit(1)

print(total / gb, used / gb, free / gb)


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download&confirm=1"

    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)

    save_response_content(response, destination)


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if not exists('local.zip'):
    print('Download file')
    download_file_from_google_drive('1r9jhGRxyiTOcOrTvP47C6Rf-RSfXPmNl', 'local.zip')

root_path = 'local'
if not exists(root_path):
    mkdir(root_path)
with zipfile.ZipFile('local.zip', 'r') as zfile:
    for name in zfile.namelist():
        file_path = join(root_path, name)
        if not exists(file_path):
            print(name)
        if name[-1] == '/':
            if not exists(file_path):
                mkdir(file_path)
        elif not exists(file_path):
            with zfile.open(name, 'r') as ifile:
                with open(file_path, 'wb') as file:
                    file.write(ifile.read())
