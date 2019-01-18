import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
import os.path
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def store_db():        
    db = get_db()
    
    UPLOAD_FOLDER = 'C:/Users/roborock/Documents/GitHub/easylabel/robolabel/static/images'
    #ALLOWED_EXTENSIONS = set(['.bmp'])
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    files=os.listdir(UPLOAD_FOLDER) 
    count=0
    for filename in files:
        count= count + 1
        db = get_db()
        db.execute(
                'INSERT INTO pic (id,body)'
                ' VALUES (?, ?)',
                (count,filename)
        ) 
        db.commit()
       


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    store_db()
    click.echo('Initialized the database.')
    


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
