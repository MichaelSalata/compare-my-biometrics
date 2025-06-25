#!/usr/bin/env python
import cherrypy
import os
import sys
import threading
import traceback
import webbrowser
import json
from dotenv import load_dotenv, set_key

from urllib.parse import urlparse
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError

# This is a forked version of the official gather_keys_oauth2.py
# github link: https://github.com/orcasgit/python-fitbit/blob/master/gather_keys_oauth2.py

class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""

        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )

        self.redirect_uri = redirect_uri

    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()

        # Same with redirect_uri hostname and port.
        urlparams = urlparse(self.redirect_uri)
        cherrypy.config.update({'server.socket_host': urlparams.hostname,
                                'server.socket_port': urlparams.port})

        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()


if __name__ == '__main__':
    DEFAULT_DOTENV_PATH = '../airflow-gcp/.env'
    CONN_NAME = "AIRFLOW_CONN_FITBIT_HTTP"

    if (len(sys.argv) == 3):
        server = OAuth2Server(*sys.argv[1:])
        env_variables = {}
        env_variables["client_id"], env_variables["client_secret"] = sys.argv[1], sys.argv[2]
    else:
        if os.path.exists(DEFAULT_DOTENV_PATH):
            load_dotenv(DEFAULT_DOTENV_PATH)
            env_variables = os.getenv(CONN_NAME)
            if not env_variables:
                print(f"{CONN_NAME} not in {DEFAULT_DOTENV_PATH}")
                sys.exit(1)
            env_variables = json.loads(env_variables)
            if not env_variables.get("login") or not env_variables.get("password"):
                print(f"{CONN_NAME} doesn't have login or password set")
                sys.exit(1)

            env_variables["client_id"], env_variables["client_secret"] = env_variables["login"], env_variables["password"]
            del env_variables["login"]
            del env_variables["password"]

            server = OAuth2Server(client_id=env_variables["client_id"], client_secret=env_variables["client_secret"])
            
        else:
            raise(f"tried and didn't find {DEFAULT_DOTENV_PATH} locally...")


    server.browser_authorize()
    profile = server.fitbit.user_profile_get()
    print(f'You are authorized to access data for the user: {profile["user"]["fullName"]}')

    token_dict = server.fitbit.client.session.token
    print('TOKENS RETRIEVED\n=====\n')
    token_dict["client_id"] = env_variables["client_id"]
    token_dict["client_secret"] = env_variables["client_secret"]

    for key, value in token_dict.items():
        print(key, ' = ', value)

    # Build Airflow connection dict-style variable
    fitbit_airflow_conn = {
        "conn_type": "http",
        "login": token_dict["client_id"],
        "password": token_dict["client_secret"],
        "host": "api.fitbit.com",
    }
    del token_dict["client_id"]
    del token_dict["client_secret"]
    fitbit_airflow_conn["extra"] = token_dict

    
    serialized_conn = json.dumps(fitbit_airflow_conn, indent=4)

    if not os.path.exists(DEFAULT_DOTENV_PATH):
        open(DEFAULT_DOTENV_PATH, 'a').close()

    # Check writable
    if not os.access(DEFAULT_DOTENV_PATH, os.W_OK):
        print(f"Error: The file {DEFAULT_DOTENV_PATH} is not writable.")
        sys.exit(1)

    load_dotenv(DEFAULT_DOTENV_PATH)
    set_key(DEFAULT_DOTENV_PATH, CONN_NAME, serialized_conn)
    print(f'tokens saved to {DEFAULT_DOTENV_PATH} AS {CONN_NAME}')