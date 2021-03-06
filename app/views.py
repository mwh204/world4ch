#!/usr/bin/python
# views.py - generates HTML pages using templates, databases, and logic
from flask import render_template
from app import app
import sqlite3
from collections import defaultdict

#cuts off the title in the index if it is too long
#this is necessary due to a couple of spam posts on /prog/ that skewed(?) the html table
def cutoff_title(title, cutoff):
    if len(title) > cutoff:
        c = (cutoff / 2) - 2
        return title[:c] + '....' + title[len(title)-c:]
    return title

# connect to the database to store image metadata
db_fname = "db.sqlite"

# initialize thread list
conn = sqlite3.connect(db_fname)
c1 = conn.cursor()
c1.execute('SELECT * FROM threads ORDER BY lastbumptime DESC;')
thread_query = c1.fetchall()

# insert thread list into dictionary
threads = []
for row in thread_query:
	threads.append(
		{
			'threadid' : row[0],
			'title' : cutoff_title(row[1], 256),
			'board' : row[2],
			'firstposttime' : row[3],
			'lastposttime' : row[4],
			'lastbumptime' : row[5],
			'numposts' : row[6]
		}
	)

# index page, lists all threads in database
@app.route('/')
@app.route('/index')
def index():
    if index.indx is None:
        index.indx = render_template('index.html', board="prog", title="Programming", threads=threads)
    return index.indx
index.indx = None

# threads page, figure out which thread to display from URL
@app.route('/thread/<int:url_thread_id>')
def page(url_thread_id):
	# generate list of threads
	conn = sqlite3.connect(db_fname)
	c = conn.cursor()
	c.execute("""SELECT * FROM posts WHERE threadid = ? ORDER BY postnum""", [url_thread_id])
	posts_query = c.fetchall()
	
	# insert thread list into dictionary
	posts = []
	for row in posts_query:
		posts.append(
			{
				'threadid' : row[0],
				'postnum' : row[1],
				'postername' : row[2],
				'postermeiru' : row[3],
				'postertrip' : row[4],
				'posterid' : row[5],
				'posterdate' : row[6],
				'post' : row[7]
			}
		)
	
	return render_template('thread.html', board="prog", title=get_title(url_thread_id), posts=posts)

# Database Test page
@app.route('/test')
def test():
	return(str(posts.query_all()))

#query the threads dict to find the title 
def get_title(threadid):
    for entry in threads:
        if entry['threadid'] == threadid:
                return entry['title']
    return 'Unknown Title'
