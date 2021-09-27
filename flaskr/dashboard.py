import requests
import secrets
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Blueprint, session, request, render_template, redirect

bp = Blueprint('dashboard', __name__, url_prefix="/dashboard")

scope = 'user-read-top'
ranges = ['short_term', 'medium_term', 'long_term']

code = 'AQDlZp2WhLO3HGbxAIegPOd0NPQ_8ErJZTNE2zerz7ookLeAsHXuCurIx5KgicIvT06Pkv4UzbkLFxprnYTWu6JjbXRdqg3-b7reo3pb9F3SOnSu52S8pDfoXgBu4f7wu9s24UG_XSiKnO_9rqYghF2h1SVqVTCOJ2H8JwbDD0vekJKzsZN494E5JKKvnShUyvCSPHJb2O0JW0n-S4WD'

@bp.route('/home', methods=('GET', 'POST'))
def home():
  if request.method == 'POST':
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    for sp_range in ['short_term', 'medium_term', 'long_term']:
      print("range:", sp_range)

      results = sp.current_user_top_artists(time_range=sp_range, limit=50)

      for i, item in enumerate(results['items']):
        print(i, item['name'])
      print()

  return render_template('dashboard/home.html')


@bp.route('/spotify')
def spotify():
  r = request.args
  if r.get('code', default = None) != None:
    code = r.get('code')
    state = r.get('state')
    return render_template('dashboard/temp.html', code = code, state = state)
  return render_template('dashboard/temp.html', code = 'login denied', state = '')