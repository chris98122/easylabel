from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from robolabel.auth import login_required
from robolabel.db import get_db
from flask import current_app
from flask import make_response
import os
lb = Blueprint('label', __name__)

@lb.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title,body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('label/index.html', posts=posts)



@lb.route('/mainpage', methods=('GET', 'POST'))
@login_required
def mainpage():
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('label.index'))
    
    return render_template('label/mainpage.html')

@lb.route('/<int:id>')
def dir_listing(id):
    BASE_DIR = '/Users/roborock/Documents/GitHub/easylabel/robolabel/static/images/'

    # Joining the base and the requested path
    
    print(id)
    # Return 404 if path doesn't exist
    if not os.path.exists(BASE_DIR):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(BASE_DIR):
        return send_file(BASE_DIR)

    # Show directory contents
    files = os.listdir(BASE_DIR)
    return render_template('label/mainpage.html', files=files)

@lb.route('/<string:pic>')
       return send_file