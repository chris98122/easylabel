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



from flask import send_from_directory
@lb.route('/<int:id>/mainpage', methods=('GET', 'POST'))
@login_required
def mainpage(id):
    
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

    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path=root_dir+'\static'+'\images'
    files = os.listdir(img_path)
    file= "/static/images/"+files[id]
    return render_template('label/mainpage.html',file=file)
