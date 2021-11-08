import os
import spotipy
from flask import Flask, render_template, request, redirect

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
    # Load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # Load the test config if passed in
    app.config.from_mapping(test_config)

  # Ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # Load db
  from . import db
  db.init_app(app)

  # Register auth blueprint
  #from . import auth
  #app.register_blueprint(auth.bp)

  # Register blog blueprint
  from . import blog
  app.register_blueprint(blog.bp)

  from . import book_scraper
  

  @app.route('/dashboard', methods=('GET', 'POST'))
  def dashboard():
    dtb = db.get_db()

    # When refreshed
    if request.method == 'POST':
      books = book_scraper.get_books()
      # Clear books table
      dtb.execute('DELETE FROM book')
      # Populate books table
      for book in books:
        dtb.execute('INSERT INTO book(title, author, status, url) VALUES(?, ?, ?, ?)', (book['title'], book['author'], book['status'], book['url']))

  
      sp = spotipy.Spotify(auth_manager = spotipy.oauth2.SpotifyOAuth(scope = "user-top-read"))

      # Range can be short-term, medium-term, or long-term
      artist_data = sp.current_user_top_artists(time_range='short_term', limit=20)
      track_data = sp.current_user_top_tracks(time_range='short_term', limit=20)
      
      # Clear artists and tracks tables
      dtb.execute('DELETE FROM artist')
      dtb.execute('DELETE FROM track')
      
      # Insert new artists and tracks
      for i, item in enumerate(artist_data['items']):
        dtb.execute('INSERT INTO artist(name, image_url, spotify_url, rank) VALUES(?, ?, ?, ?)', (item['name'], item['images'][0]['url'], item['external_urls']['spotify'], i))
      for i, item in enumerate(track_data['items']):
        dtb.execute('INSERT INTO track(name, artist, spotify_url, rank) VALUES(?, ?, ?, ?)', (item['name'], item['artists'][0]['name'], item['external_urls']['spotify'], i))
      dtb.commit()
        
    artists = dtb.execute('SELECT * FROM artist ORDER BY rank').fetchall()
    tracks = dtb.execute('SELECT * FROM track ORDER BY rank').fetchall()
    books = dtb.execute('SELECT * FROM book').fetchall()
    return render_template('dashboard.html', artists=artists, tracks=tracks, books=books)


  @app.route('/')
  def index():
    return render_template('index.html')


  @app.route('/projects')
  def projects():
    return render_template('projects.html')


  @app.route('/about')
  def about():
    return render_template('about.html')


  return app
