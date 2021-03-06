#!/usr/bin/env python3

import os

from flask import Flask, render_template, redirect, url_for, request
from db import setup_db, get_db

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = bool(os.environ.get('FLASK_DEBUG', 1))
setup_db(app)

@app.route('/add_meme', methods=['POST'])
def add_meme():
    get_db().execute('INSERT INTO memes(url, caption1, caption2) VALUES(?, ?, ?);', (
        request.form['image'],
        request.form['top_caption'],
        request.form['bottom_caption']
    ))

    return redirect(url_for('index'))

@app.route('/meme/<id>')
def show(id):
    meme = get_db().select('SELECT id, url, caption1, caption2 FROM memes WHERE id=?;',
                           [id])[0]

    return render_template('show.html', meme=meme)

@app.route('/meme_form')
def meme_form():
    return render_template('meme-form.html')

@app.route('/')
def index():
    memes = get_db().select('SELECT id, url, caption1, caption2 FROM memes')
    return render_template('homepage.html', memes=memes)

if __name__ == '__main__':
    app.run(host=os.environ.get('BIND_TO', '127.0.0.1'),
            port=int(os.environ.get('PORT', 5000)),
            debug=bool(int(os.environ.get('FLASK_DEBUG', 1))))
