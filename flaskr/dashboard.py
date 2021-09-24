import requests
import secrets

from flask import Blueprint, session, request, render_template

bp = Blueprint('dashboard', __name__, url_prefix="/dashboard")

STATE = secrets.token_urlsafe(16)
CLIENT_ID = 'b7cc6ae6953b4d0598ccc84a86f8b5f6'
CLIENT_SECRET = 'd17a6734251c42fd9a0d954cc9c92446'
REDIRECT_URI = 'tylermcgraw.herokuapp.com/dashboard/spotify'

auth_params = {
  'client_id': CLIENT_ID,
  'response_type': 'code',
  'redirect_uri': REDIRECT_URI,
  'state': STATE
}


@bp.route('/home', methods=('GET', 'POST'))
def home():
  if request.method == 'POST':
    r = requests.get('https://accounts.spotify.com/authorize', params = auth_params)
    return render_template('dashboard/spotify.html', r = r)

  return render_template('dashboard/home.html')


@bp.route('/spotify')
def spotify():
  r = request.args
  if r.get('code', default = None) != None:
    code = r.get('code')
    state = r.get('state')
    return render_template('dashboard/temp.html', code = code, state = state)
  return render_template('dashboard/temp.html', code = 'login denied', state = '')