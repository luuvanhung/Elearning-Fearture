# Enterprise Resource Management

## Requirements

Mysql Client 3.5

Python 3.7 or later

Node 14 for frontend

## Preparing accounts
(Only creates these accounts for your local debuging puporse. On the server side, we already created these accounts for all environments.)
1. Create account for mailing service
    * Register an new [Google Account](https://accounts.google.com/) for mailing service 
    * Turn on [2-Steps Verification](https://support.google.com/accounts/answer/185839) for your account
    * Create an [App Passwords](https://support.google.com/mail/answer/185833) for your mailing service
    * Remember [SMTP setup options](https://support.google.com/a/answer/176600?hl=en#zippy=%2Cuse-the-restricted-gmail-smtp-server%2Cuse-the-gmail-smtp-server) to fill in `src/config.env` later.
2. Create Firebase/Google Cloud Platform accounts for Google's services (authentication, calendar,...)
    * Register an [Firebase](https://firebase.google.com/)
    * Open [Firebase console](https://console.firebase.google.com/), create a project. When you creat a project on Firebase, it also create a project on Google Cloud  Platform. You can also create an [web app](https://firebase.google.com/learn/pathways/firebase-web), but it is not required.
    * Open [Google Cloud Console](https://console.cloud.google.com/), chose your project and [enable](https://cloud.google.com/endpoints/docs/openapi/enable-api) needed APIs/Services. We need Google Calendar API, your can enable more APIs as you want.
    * [Create](https://support.google.com/cloud/answer/6158849) an [OAuth Client ID](https://developers.google.com/identity/protocols/oauth2) for `Login with Google`, and a [Service Account](https://cloud.google.com/iam/docs/service-accounts) for calendar service. Download the `credentials.json` and replace `src/api/credentials.json`.
    * Create new [Google Calendar](https://support.google.com/calendar/answer/37095) and [share](https://support.google.com/calendar/answer/37082) that calendar with the service account.
    * Remember all the keys and ids to fill in `src/config.env` later.
3. Slack
    * Create a [Slack workspace](https://slack.com/help/articles/206845317-Create-a-Slack-workspace) for your self. Then create a [chanel](https://slack.com/help/articles/201402297-Create-a-channel) on that workspace.
    * Create a [Slack app](https://api.slack.com/authentication/basics) and install it to your workspace:
        * Open the [Slack Apps console](https://api.slack.com/apps), chose your app.
        * Take a look on `Basic Information` section. There are some keys, you will use them to fill in `src/config.env` later.
        * Go to `Interactivity & Shortcuts` section, fill the `Request URL` by `<your api host>/api/v1/slack-bot/slack/actions`. If you don't have a domain, you can use [Ngrok](https://ngrok.com/) to register a free domain and forward to you personal computer.
        * Go to `Event Subscriptions` section, fill the `Request URL` by `<your api host>/api/v1/slack-bot/slack/events`
        * Take a look on `OAuth & Permissions` section. There are some other keys, you will use them to fill in `src/config.env` later. Make sure to grand needed `Scopes`, so the app can read message and reply other users.
4. wit.ai
    * Register an [wit.ai](https://wit.ai/) account.
    * [Create an app](https://wit.ai/docs/quickstart) and training your bot
    * Go to [Wit.ai App console](https://wit.ai/apps/), chose your app. Then chose `Settings` section. There are some keys, you will use it to fill in `src/config.env` later.
    * There is [another repository](https://gitlab.damelagi.org/internship/hrm/hr-bot-crawler) for crwaling data and train the bot. You can contact your mentors for the training data and the guidline too.


## Install dependencies and build

### Running in ubuntu

1. Install packages

    ```
        sudo apt-get -y install python-virtualenv mysql-server mysql-client python3 python3-dev python3-pip python-mysqldb libmysqlclient-dev
    ```

2. Create virtualenv
    ```
        virtualenv --python=/usr/bin/python3 env
        source /home/ubuntu/env/bin/activate
        deactivate
    ```

3. Install all dependencies:
    ```
        pip3 install -r requirements.txt
    ```

4. Init config & database
    ```
        ./ci/generate-rsa-key.sh jwt
        cp src/core/config.env.sample src/config.env
        cd src
        python3 manage.py migrate
    ```

5. Get Google Calendar API credentials
    ```
        https://developers.google.com/calendar/quickstart/go
    ```
6. Build frontend

   Copy *src/frontend/sample.env* to *src/frontend/.env*, and change the config if you want. By default, we don't need
   to change.

   Build the frontend (call these command from the *src/frontend* folder):

   Install dependencies
    ```
    npm install
    ```

   Build for release
    ```
    npm run build
    ```

   Or build for debug
    ```
    npm run watch
    ```

   Collect static files (only need for `production`):
    ```
    python manage.py collectstatic --settings=core.settings.production
    ```

7. Start Server Its recommended running the `development` mode only on your local PC. If you would like to run
   the `production` mode, you should use docker / use proxy server to host static resource / or add `--insecure`
   parameter to force serving of static files with the staticfiles app (More
   detail [here](https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/)).
    ```
        cd src
        python3 manage.py runserver --settings=core.settings.development
    ```

8. For Mac: 
    run before pip install
    ```
        export CFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -I/usr/local/include/ ${CFLAGS}"
        export LDFLAGS="-isysroot $(xcrun --show-sdk-path) -L/usr/local/lib -L/usr/lib"
        export CPPFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -L/usr/lib"
    ```
    run before npm install
    ```
        export LDFLAGS="-L/usr/local/opt/node@14/lib"
        export CPPFLAGS="-I/usr/local/opt/node@14/include"
    ```

### Running in windows

1. Install environment and activate :
   ```
      python -m venv venv
      venv\Scripts\activate
   ```

2. Install requirement libraries :

- First you have to comment libraries uWSGI (this only run in Ubuntu)
   ```
      pip install -r requirements.txt
   ```

3. Follow from step 3 to the end in Running with Ubuntu

## Using docker

If you would like to use docker, you can skip the `Install dependencies and build` section. Just follow these steps:

1. Copy and rename these files. Then change the values for `__ERP_PORT__`, `__DJANGO_SETTINGS_MODULE__`, and other environment variables (if needed).
    * `ci/Dockerfile.template` -> `Dockerfile`
    * `ci/docker-compose.yml.local` -> `docker-compose.yml`
    * `ci/docker.env.template` -> `docker.env`
    * `src/core/config.env.sample` -> `src/config.env`
2. From the root folder (where the docker-compose.yml located), run the command:
    ```
    docker-compose up -d --build
    ```

## Adding libraries

1. Adding python libraries:

   If your need add more libraries while developing new feature. Make sure to follow these steps:

   a. First, install the library:
    ```
    pip install <library name>
    ```

   b. Use the library as you want

   c. List the libraries to the requirements.txt
    ```
    pip freeze > requirements.txt
    ```

   d. Commit the requirements.txt within your other codes

2. Adding JavaScript libraries:
   If your need add more JavaScript libraries for frontend. Make sure to follow these steps:

   a. First, install the library (from `src/frontend` folder):
    ```
    npm install <library name>
    ```

   b. Use the library as you want

   d. Commit these files within other changes to gitlab:
    * src/frontend/package.json
    * src/frontend/package-lock.json

### Reset database, run file:
   src/resetBD.sh

### Set up precommit:
   ```
   pre-commit install
   pre-commit install --hook-type commit-msg
   # install latest npm version by using nvm https://github.com/nvm-sh/nvm (Recommended)
   npm install --save-dev @commitlint/{cli,config-conventional}
   ```

### Create api key
   ```
   python3 manage.py create_api_key {name} {scope} {application_id}
   ```
