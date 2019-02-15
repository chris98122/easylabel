from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from robolabel.auth import login_required
from robolabel.db import get_db

from flask import current_app
from flask import make_response
import os
import json
from flask import jsonify
from flask import Response

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


def get_post(id, check_author=True):
    
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
       print("post",id," is none")
       
    return post


@lb.route('/getNewImage', methods=('GET', 'POST'))
@login_required
def getNewImage():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path=root_dir+'\static'+'\images'
    files = os.listdir(img_path)
    
    id =request.form.get('id')
    id=int(id)
    if(id==len(files)):
        id=len(files)
    
    file= "/static/images/"+files[id]
    return jsonify(url=file)


    
@lb.route('/getPost', methods=('GET', 'POST'))
@login_required
def getPost():
    id =request.form.get('id')
    title=request.form.get('title')
    id=int(id)
    post = get_post(id+1) 
    return jsonify(label=post['title'])


#from flask import send_from_directory
@lb.route('/mainpage', methods=('GET', 'POST'))
@login_required
def mainpage():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path=root_dir+'\static'+'\images'
    
    files = os.listdir(img_path)
    file= "/static/images/"+files[0]
    for i in range(len(files)):
        post=get_post(i+1)
        if post is None:
            file= "/static/images/"+files[i]
            print(file)
            id=i
            break
        if post is not None and i == len(files)-1:
            file= "/static/images/"+files[i]
            id=i
            

    if request.method == 'POST':
        id= request.form['id']
        id=int(id)
        title = request.form['title']
        post = get_post(id+1) 
        body = files[id]
        error = None
        if not title:
            error = 'Category is required.'

        if error is not None: 
            flash(error)

        ##### 如果db里面没有post 则insert    
        elif post is None:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            if id==len(files)-1:
                return redirect( url_for('label.mainpage') )
            else:
               return redirect( url_for('label.mainpage') )
        ##### 如果db里面有post 则update    
        elif post is not None:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id+1)
            )
            db.commit()
            
            if id==len(files)-1:
                return redirect( url_for('label.mainpage') )
            else:
                return redirect( url_for('label.mainpage') )
        
    
    return render_template('label/mainpage.html',file=file,post=post,id=id)
    

@lb.route('/loadimage', methods=('GET', 'POST'))
@login_required
def loadimage():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path=root_dir+'\static'+'\images'
    files = os.listdir(img_path)
    id =int(request.form.get('id'))
    if(id==len(files)):
        id=len(files)

    file= "/static/images/"+files[id]
    
    folder=""
    annotations={}
    return jsonify(url=file,id=id,\
    folder=folder,annotations=annotations)


from robolabel.writexml import writexml

@lb.route('/annotation', methods=('GET', 'POST'))
@login_required
def annotation():
    if request.method == 'POST':
        data = json.loads(request.form.get('sendInfo'))
        id=data["id"]
        url=data["url"]
        folder=data["folder"]
        width=data["width"]
        height=data["height"]
        annotations=data["annotations"]
        ##打印所有tag
        #print(' '.join( str(v) for v in annotations))
        file=url.split("/")
        writexml(annotations,file[-1],width,height)
        message = str(id) +".xml has been created."
        return jsonify(message=message)
      
    return render_template('label/annotation.html')

