# final_project_fall_2025
This is a movie web application.


## Setup
Clone the Repo to download it from GitHub. Perhaps onto the Desktop.



Create a virtual environment
```sh
conda create -n final-project-env-fall-2025 python=3.11
```
Activate the virtual environment
```sh
conda activate final-project-env-fall-2025
```

Navigate to project
```sh
cd ~Desktop\final_project_fall_2025
OR
cd C:"\Users\username\Desktop\final_project_fall_2025"
```
In second line, replace "username" with your username

Install dependences:

```sh
pip install -r requirements.txt
```

Navigate to the repo using the command line.

## Usage
Example script:

```sh
python apps/movies.py

```
## Secret Credentials
this is the ".env" file...

replace "demo" with your premium key:
```sh
TMDB_API_KEY="demo"

```
also tell flask where web app is located
```sh
FLASK_APP=web_app
```

## Web App

if we have the FLASK_APP=web_app env var in the ".env" file:
```sh
flask run
```

Mac OS:
```sh
FLASK_APP=web_app flask run
```
 Windows OS:
... if `export` doesn't work for you, try `set` instead
... or set FLASK_APP variable via ".env" file
```sh
export FLASK_APP=web_app
flask run
```

## Testing

Run tests:

```sh
pytest
```