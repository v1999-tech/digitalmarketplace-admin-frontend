# digitalmarketplace-admin-frontend

Frontend administration application for the digital marketplace.

- Python app, based on the [Flask framework](http://flask.pocoo.org/)

## Setup

Install [Virtualenv](https://virtualenv.pypa.io/en/latest/)

```
sudo easy_install virtualenv
```

Create a virtual environment
 
 ```
 virtualenv ./venv
 ```

Set the required environment variables (for dev use local API instance if you 
have it running):
```
export DM_API_URL=https://api.digitalmarketplace.service.gov.uk
export DM_API_BEARER=<bearer_token>
```

### Activate the virtual environment

```
source ./venv/bin/activate
```

### Upgrade dependencies

Install new Python dependencies with pip

```pip install -r requirements.txt```

Install frontend dependencies with npm and gulp

```
npm install
```

### Run the tests

```
./scripts/run_tests.sh
```


### Run the server

```
python application.py runserver
```

Use the app at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Frontend tasks

[NPM](https://www.npmjs.org/) is used for all frontend build tasks. The commands available are:

- `npm run frontend-build:development` (compile the frontend files for development)
- `npm run frontend-build:production` (compile the frontend files for production)
- `npm run frontend-build:watch` (watch all frontend files & rebuild when anything changes)
- `npm run frontend-install` (install all non-NPM dependancies)

Note: `npm run frontend-install` is run as a post-install task after you run `npm install`.
