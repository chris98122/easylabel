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

def getNewImage():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path=root_dir+'\static'+'\images'
    #post = get_post(id+1) 
    files = os.listdir(img_path)
    
    former_id =request.form.get('id')
    former_id=int(former_id)
    former_id+=1
    print(former_id)
    file= "/static/images/"+files[former_id]
    print(file)
    return jsonify(url=file)



#from flask import send_from_directory
@lb.route('/<int:id>/mainpage', methods=('GET', 'POST'))
@login_required
def mainpage(id):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path=root_dir+'\static'+'\images'
    post = get_post(id+1) 
    files = os.listdir(img_path)
     #####显示图片
     ##显示方式： n-1到n页（显示为第0张）往后是第1张
    if id==len(files):
        id=0
        file= "/static/images/"+files[id]
        post = get_post(id+1) 
        
    else:
        file= "/static/images/"+files[id]

    #####   显示图片 结束
    ##### 上传分类的表单   
 
    if request.method == 'POST':
        
        title = request.form['title']

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
                return redirect( url_for('label.mainpage', id=0) )
            else:
               return redirect( url_for('label.mainpage', id=id+1) )
        ##### 如果db里面有post 则update    
        elif post is not None:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id+1)
            )
            db.commit()
            
            if id==len(files)-1:
                return redirect( url_for('label.mainpage', id=0) )
            else:
                return redirect( url_for('label.mainpage', id=id+1) )
        
    return render_template('label/mainpage.html',file=file,id=id,post=post)
    


@lb.route('/<int:id>/annotation', methods=('GET', 'POST'))
@login_required
def annotation(id):
   
    root_dir = os.path.abspath(os.path.dirname(__file__))
    img_path=root_dir+'\static'+'\images'
    files = os.listdir(img_path)
     #####显示图片
     ##显示方式： n-1到n页（显示为第0张）往后是第1张
    if id==len(files):
        id=0
        file= "/static/images/"+files[id]
    
    else:
        file= "/static/images/"+files[id]

    if request.method == 'POST':
        title = request.form['title']
        x=request.form['x']
        body = files[id]
        error = None
        
        if not title:
            error = 'tag is required.'

        if error is not None: 
            flash(error)
        print("x:",x)
        print("title:",title)
        
    
    return render_template('label/annotation.html',file=file,id=id)

