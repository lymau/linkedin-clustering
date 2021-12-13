from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import os
from app.auth import login_required
from app.db import get_db
from app.helper.model import text_to_tfidf, load_model

bp = Blueprint('predict', __name__)

# Initiate the object models
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
tf_idf = load_model(os.path.join(APP_ROOT, './models/tf_idf.pkl'))
pca = load_model(os.path.join(APP_ROOT, './models/pca.pkl'))
kmeans = load_model(os.path.join(APP_ROOT, './models/model.pkl'))

def predict(text, tf_idf, pca, model):
    pca_text = text_to_tfidf(text, tf_idf, pca)
    cluster = model.predict(pca_text)
    return cluster

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, body, created, user_id, username'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post doesn't exist.")

    if check_author and post['user_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, body, created, predicted, user_id, username'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('predict/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        body = request.form['body']
        error = None

        if not body:
            error = 'Text body is required.'

        cluster = predict(body, tf_idf, pca, kmeans)
        cluster = int(cluster)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (body, user_id, predicted)'
                ' VALUES (?, ?, ?)',
                (body, g.user['id'], cluster)
            )
            db.commit()
            return redirect(url_for('predict.index'))

    return render_template('predict/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        body = request.form['body']
        error = None

        if not body:
            error = 'Text body is required.'

        cluster = predict(body, tf_idf, pca, kmeans)
        cluster = int(cluster)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET body = ?, predicted = ?'
                ' WHERE id = ?',
                (body, cluster, id)
            )
            db.commit()
            return redirect(url_for('predict.index'))

    return render_template('predict/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    try:
        get_post(id)
        db = get_db()
        db.execute('DELETE FROM post WHERE id = ?', (id,))
        db.commit()
        message = "Post was deleted successfully."
    except db.IntegrityError:
        message = "Sorry. Something's wrong :("

    flash(message)
    return redirect(url_for('predict.index'))

@bp.route('/about')
def about():
    return render_template('about.html')