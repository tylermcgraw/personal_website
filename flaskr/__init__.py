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
  from . import auth
  app.register_blueprint(auth.bp)

  # Register blog blueprint
  from . import blog
  app.register_blueprint(blog.bp)

  from . import book_scraper

  cache_folder = 'flaskr/.cache_spotify/'

  @app.route('/dashboard', methods=('GET', 'POST'))
  def dashboard():
    # If being redirected from Spotify
    if request.args.get("code"):
      cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_folder)
      auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read',
                                                 cache_handler=cache_handler, 
                                                 show_dialog=True)
      auth_manager.get_access_token(request.args.get("code"))
      # code 307 is a POST request, so tmcgraw doesn't have to click refresh again
      return redirect('/dashboard', code=307)

    dtb = db.get_db()
    # When user tmcgraw clicks refresh
    if request.method == 'POST':
      books = book_scraper.get_books()
      # Clear books table
      dtb.execute('DELETE FROM book')
      # Populate books table
      for book in books:
        dtb.execute('INSERT INTO book(title, author, status, url) VALUES(?, ?, ?, ?)', (book['title'], book['author'], book['status'], book['url']))

      # Make sure cache exists
      if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

      cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_folder)
      auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read',
                                                 cache_handler=cache_handler, 
                                                 show_dialog=True)
      
      # Redirect to Spotify sign in if no token
      if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect(auth_manager.get_authorize_url())
        
      # Signed in, get data
      sp = spotipy.Spotify(auth_manager=auth_manager)

      # Range can be short-term, medium-term, or long-term
      artist_data = sp.current_user_top_artists(time_range='long_term', limit=20)
      track_data = sp.current_user_top_tracks(time_range='long_term', limit=20)
      
      # Check if db is empty -> insert if empty, update otherwise
      isempty = dtb.execute('SELECT count(*) FROM (SELECT 0 FROM artist LIMIT 1)').fetchone()[0] == 0
      
      # Insert into db if empty, otherwise update
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
