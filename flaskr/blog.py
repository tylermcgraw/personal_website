from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/home')
def home():
  db = get_db()
  comments = db.execute(
    'SELECT p.id, post, body, created, author_id, username'
    ' FROM comment p JOIN user u ON p.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()
  return render_template('blog/home.html', comments=comments)


@bp.route('/post/<string:post>')
def post(post):
  return render_template(f'blog/posts/{post}.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
  if request.method == 'POST':
    post = 'genesis' #todo
    body = request.form['body']
    error = None

    if not body:
      error = 'Text is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'INSERT INTO comment (post, body, author_id)'
        ' VALUES (?, ?, ?)',
        (post, body, g.user['id'])
      )
      db.commit()
      return redirect(url_for('blog.home'))

  return render_template('blog/create.html')


# Fetch comment to be updated or deleted
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


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
  comment = get_comment(id)

  if request.method == 'POST':
    post = 'genesis' #todo
    body = request.form['body']
    error = None

    if not body:
      error = 'Text is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE comment SET post = ?, body = ?'
        ' WHERE id = ?',
        (post, body, id)
      )
      db.commit()
      return redirect(url_for('blog.home'))

  return render_template('blog/update.html', comment=comment)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
  get_comment(id)
  db = get_db()
  db.execute('DELETE FROM comment WHERE id = ?', (id,))
  db.commit()
  return redirect(url_for('blog.home'))