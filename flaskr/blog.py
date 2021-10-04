from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

# Render blog homepage
@bp.route('/home')
def home():
  return render_template('blog/home.html')


# Render post and comments, add comment if POST request
@bp.route('/post/<string:post>', methods=('GET', 'POST'))
def post(post):
  db = get_db()
  if request.method == 'POST':
    # New comment
    body = request.form['body']
    error = None

    if not body:
      error = 'Text is required.'

    if error is not None:
      flash(error)
    else:
      db.execute('INSERT INTO comment (post, body, author_id) VALUES (?, ?, ?)', (post, body, g.user['id']))
      db.commit()
  # Select comment body, id, author_id, and created date; user username
  comments = db.execute('SELECT body, comment.id, author_id, username, created '
                        'FROM comment INNER JOIN user ON comment.author_id = user.id '
                        'WHERE post = :post ORDER BY created ASC', {'post': post}).fetchall()
  return render_template(f'blog/posts/{post}.html', comments=comments, post=post)


# Fetch comment to be deleted
def get_comment(id, check_author=True):
  comment = get_db().execute(
    'SELECT p.id, post, body, created, author_id, username'
    ' FROM comment p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
    (id,)
  ).fetchone()

  if comment is None:
    abort(404, f"Comment id {id} doesn't exist.")

  if check_author and comment['author_id'] != g.user['id']:
    abort(403)

  return comment


# Delete comment
@bp.route('/<int:id>/<string:post>/delete', methods=('POST',))
@login_required
def delete(id, post):
  get_comment(id)
  db = get_db()
  db.execute('DELETE FROM comment WHERE id = ?', (id,))
  db.commit()
  return redirect(url_for('blog.post', post=post))