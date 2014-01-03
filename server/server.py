#!/usr/bin/env python

import sqlite3
#import ipdb
from datetime import datetime
from flask import Flask, render_template, request, g
import ipdb

app = Flask(__name__)
DATABASE = '../analisis/base.db'
lastPing = ""


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/totem", methods=['POST', 'GET'])
def totem():
	db = sqlite3.connect(DATABASE)
	cur = db.cursor()
	dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now'));").fetchall()[0][0]
	anio = cur.execute("select count(*) from bicis where strftime('%Y',millis)=strftime('%Y', date('now'));").fetchall()[0][0]/7500
	global lastPing
	lastPing = "%s: %s" % (request.remote_addr, datetime.now())
	return "#####" + " " * (5-len(str(dia))) + str(dia) + "0" * (2-len(str(anio))) + str(anio)
	cur.close() 
	db.close()

@app.route("/dia", methods=['POST', 'GET'])
def dia():
	db = sqlite3.connect(DATABASE)
	cur = db.cursor()
	dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now'));").fetchall()[0][0]
	return str(dia)
	cur.close() 
	db.close()

@app.route("/semana", methods=['POST', 'GET'])
def semana():
	db = sqlite3.connect(DATABASE)
	cur = db.cursor()
	semana = cur.execute("select count(*), strftime('%Y-%m-%d',millis) from bicis group by strftime('%Y%m%d', millis);").fetchall()
	return str(semana)
	cur.close() 
	db.close()

@app.route("/lastping", methods=['POST', 'GET'])
def lastping():
	return lastPing

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)

#cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
