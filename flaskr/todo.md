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

CLIENT_ID = 'b7cc6ae6953b4d0598ccc84a86f8b5f6'
CLIENT_SECRET = 'd17a6734251c42fd9a0d954cc9c92446'
REDIRECT_URI = 'http://www.tylermcgraw.com/dashboard'
code = 'AQDlZp2WhLO3HGbxAIegPOd0NPQ_8ErJZTNE2zerz7ookLeAsHXuCurIx5KgicIvT06Pkv4UzbkLFxprnYTWu6JjbXRdqg3-b7reo3pb9F3SOnSu52S8pDfoXgBu4f7wu9s24UG_XSiKnO_9rqYghF2h1SVqVTCOJ2H8JwbDD0vekJKzsZN494E5JKKvnShUyvCSPHJb2O0JW0n-S4WD'