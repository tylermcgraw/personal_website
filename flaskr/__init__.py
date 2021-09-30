import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request

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
  from . import auth
  app.register_blueprint(auth.bp)

  # Register blog blueprint
  from . import blog
  app.register_blueprint(blog.bp)

  from . import spotify_api
  from . import book_scraper

  @app.route('/dashboard', methods=('GET', 'POST'))
  def dashboard():
    dtb = db.get_db()
    # When tmcgraw clicks refresh
    if request.method == 'POST':
      books = book_scraper.get_books()
      # Clear books table
      dtb.execute('DELETE FROM book')
      for book in books:
        #no_book_exists = dtb.execute('SELECT count(*) FROM (SELECT title FROM book WHERE title = :title)', {'title': book['title']}).fetchone()
        #if no_book_exists:
        dtb.execute('INSERT INTO book(title, author, status, url) VALUES(?, ?, ?, ?)', (book['title'], book['author'], book['status'], book['url']))

      sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_api.CLIENT_ID,
                                                     client_secret=spotify_api.CLIENT_SECRET,
                                                     redirect_uri=spotify_api.REDIRECT_URI,
                                                     scope='user-top-read'))

      artist_data = sp.current_user_top_artists(time_range='long_term', limit=20)
      track_data = sp.current_user_top_tracks(time_range='long_term', limit=20)
      
      # Check if db is empty -> insert if empty, update otherwise
      isempty = dtb.execute('SELECT count(*) FROM (SELECT 0 FROM artist LIMIT 1)').fetchone()[0] == 0
      
      for i, item in enumerate(artist_data['items']):
        if isempty:
          dtb.execute('INSERT INTO artist(name, image_url, spotify_url, rank) VALUES(?, ?, ?, ?)', (item['name'], item['images'][0]['url'], item['external_urls']['spotify'], i))
        else:
          dtb.execute('UPDATE artist SET name = :name, image_url = :image_url, spotify_url = :spotify_url WHERE rank = :rank', {'name': item['name'], 'image_url': item['images'][0]['url'], 'spotify_url': item['external_urls']['spotify'], 'rank': i})
      for i, item in enumerate(track_data['items']):
        if isempty:
          dtb.execute('INSERT INTO track(name, artist, spotify_url, rank) VALUES(?, ?, ?, ?)', (item['name'], item['artists'][0]['name'], item['external_urls']['spotify'], i))
        else:
          dtb.execute('UPDATE track SET name = :name, artist = :artist, spotify_url = :spotify_url WHERE rank = :rank', {'name': item['name'], 'artist': item['artists'][0]['name'], 'spotify_url': item['external_urls']['spotify'], 'rank': i})

    artists = dtb.execute('SELECT * FROM artist ORDER BY rank').fetchall()
    tracks = dtb.execute('SELECT * FROM track ORDER BY rank').fetchall()
    books = dtb.execute('SELECT * FROM book').fetchall()
    dtb.commit()
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
