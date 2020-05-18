# Nocode Backend

The project belongs to BUAA SCSE 2019 Spring SE course. This repo is the backend part.

Visit [our blog](https://www.cnblogs.com/no-code-2020) for more infomation.

## Run

### Prerequisite

The backend is driven by python3, Django 3.0 and Postgresql.

Therefore, it's necessary to set up a Postgresql database before running the backend. Docker is recommended.

Required python packages are listed in [requirements.txt](./requirements.txt). You can install the packages with

```bash
# pip
pip install -r requirements.txt
# conda
conda install --file requirements.txt
```

### Enviornment Variable

With the consideration of security, we use the environment variable as our config. For example, database info.

You can check [here](./nocode_backend/settings.py) to find out the required variables.

### Database Migration

Convert the models into database tables. The script is as below

```bash
# generate migrations files before migrate to database
python manage.py makemigrations
# migrate to database
python manage.py migrate
```

### Run Server

Run server and listening to 8000 port as default.

```bash
python manage.py runserver
```

## API Docs

[user management](./docs/api/auth.md)

[OCR module](./docs/api/ocr.md)

[HTTP Status](./docs/api/status.md)
