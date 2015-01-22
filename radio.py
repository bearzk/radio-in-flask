#!/usr/bin/python -tt
# -*- coding: utf8 -*-

import subprocess
from flask import Flask, jsonify, redirect, render_template

app = Flask(__name__)

def run(*args):
    command = ['piradio']
    if 0 < len(args):
        for arg in args:
            command.append(arg)
    try:
        r = subprocess.check_output(command)
    except Exception, e:
        r = str(e)
    return r


@app.route('/')
def status():
    r = run()
    r = r.split('\n')[1:3]
    d = {}
    for i in r:
        k,v = i.split(':')
        d[k] = v
    return render_template('radio.html', d=d)


@app.route('/on')
def on():
    run('on')
    return redirect('/')


@app.route('/off')
def off():
    run('off')
    return redirect('/')


@app.route('/channels')
def list():
    r = run('list')
    r = [c.strip('\t') for c in r.split('\n')][2:-2]
    return render_template('channels.html', channels=r)


@app.route('/channel/<channel_id>')
def channel(channel_id=None):
    if channel_id is None:
        r = run('list')
        r = [c.strip('\t') for c in r.split('\n')][2:-2]
        return str(r)
    else:
        run(channel_id)
        return redirect('/')


@app.route('/vol/<action>')
def vol(action):
    if action not in ['up','down']:
        return run('vol')
    else:
        if action == 'up':
            arg = '+'
        else:
            arg = '-'
    run('vol', arg)
    return redirect('/')


@app.route('/mute')
def mute():
    run('mute')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

