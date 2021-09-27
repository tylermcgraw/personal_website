Todo:
Useful bootstrap components: quotes (card component), blog (custom component), dashboard (custom component)
Login?
Fix sticky footer js
Spotify API (see spotipy if stuck)


Structure:
Home
  About
  Bio
  Contact
Blog
  Posts
    Links
    Quotes
Dashboard
  Facebook friends birthdays
  Measurements, workout tracker
  Music tracker
  Book tracker
Projects


Notes:
Heroku scale dynos:
heroku ps:scale web=0

Remember to activate virtual environment
. .venv/bin/activate

Initialize db
flask init-db

Flask debug mode
export FLASK_DEBUG=1

To make requirements file:
pip freeze > requirements.txt