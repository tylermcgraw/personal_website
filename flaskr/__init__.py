import os
import requests
import secrets

from flask import Flask, redirect, render_template, session, request


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


  @app.route('/')
  def index():
    return render_template('index.html')


  @app.route('/dashboard')
  def dashboard():
    state = secrets.token_urlsafe(16)
    r = requests.get(f"https://accounts.spotify.com/authorize?client_id=b7cc6ae6953b4d0598ccc84a86f8b5f6&response_type=code&redirect_uri=https%3A%2F%2Fexample.com&scope=user-top-read&state={state}")
    return render_template('dashboard.html')


  @app.route('/projects')
  def projects():
    return render_template('projects.html')


  return app