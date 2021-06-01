from flask import render_template, request, redirect, url_for

from gitlabui import app, api


@app.route('/')
def index():
    return redirect(url_for('tags'))


@app.route('/tags')
def tags():
    return render_template('index.html', projects=api.get_projects(
        request.args.get('q'),
        opts=request.args
    ))


@app.route('/reset')
def reset():
    api.reset()
    return redirect(url_for('tags'))


@app.route('/refresh_tags')
def refresh_tags():
    api.refresh_tags()
    return redirect(url_for('tags'))


@app.route('/version')
def version():
    return api.version()
