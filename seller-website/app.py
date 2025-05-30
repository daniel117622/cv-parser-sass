import os
import traceback
from flask import Flask, render_template, redirect, url_for, session
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from authlib.integrations.flask_client import OAuth 
except Exception as e:
    OAuth = None  # Authlib not installed or import failed
    logger.warning("Error importing flask_client for OAUTH")
    logger.warning(f"Exception: {e}")
    logger.warning(traceback.format_exc())


from dotenv import load_dotenv # type: ignore

load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-secret-key")

# Check for Auth0 config
AUTH0_CLIENT_ID     = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN        = os.environ.get("AUTH0_DOMAIN")
AUTH0_CALLBACK_URL  = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")

AUTH0_AVAILABLE = all([
    OAuth,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_DOMAIN,
    AUTH0_CALLBACK_URL
])

if AUTH0_AVAILABLE:
    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id        = AUTH0_CLIENT_ID,
        client_secret    = AUTH0_CLIENT_SECRET,
        api_base_url     = f'https://{AUTH0_DOMAIN}',
        access_token_url = f'https://{AUTH0_DOMAIN}/oauth/token',
        authorize_url    = f'https://{AUTH0_DOMAIN}/authorize',
        client_kwargs    = {
            'scope': 'openid profile email',
        },
    )
else:
    oauth = None
    auth0 = None

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/auth')
def auth():
    return render_template('auth.html', auth0_available=AUTH0_AVAILABLE)

@app.route('/login')
def login():
    if not AUTH0_AVAILABLE:
        return redirect(url_for('auth'))
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)

@app.route('/callback')
def callback():
    if not AUTH0_AVAILABLE:
        return redirect(url_for('auth'))
    token = auth0.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    if not AUTH0_AVAILABLE:
        return redirect(url_for('index'))
    return redirect(
        f'https://{AUTH0_DOMAIN}/v2/logout?returnTo={url_for("index", _external=True)}'
    )

logger.info("--- Loaded Environment Variables ---")
logger.info(f"FLASK_SECRET_KEY: {os.environ.get('FLASK_SECRET_KEY')}")
logger.info(f"AUTH0_CLIENT_ID: {AUTH0_CLIENT_ID}")
logger.info(f"AUTH0_CLIENT_SECRET: {AUTH0_CLIENT_SECRET}")  # Consider masking in production!
logger.info(f"AUTH0_DOMAIN: {AUTH0_DOMAIN}")
logger.info(f"AUTH0_CALLBACK_URL: {AUTH0_CALLBACK_URL}")
logger.info(f"Authlib Installed: {'YES' if OAuth else 'NO'}")
logger.info(f"Auth0 Setup: {'ENABLED' if AUTH0_AVAILABLE else 'DISABLED'}")

if __name__ == "__main__":
    app.run(debug=True)
