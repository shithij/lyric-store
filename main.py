from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

app=Flask(__name__)

@app.route('/')
def index():
	res= requests.get("http://www.metrolyrics.com/top100.html")
	soup= BeautifulSoup(res.text,'html.parser')
	s= soup.findAll('a',{'class':'song-link hasvidtoplyric'})

	songs=[]
	links=[]
	singers=[]

	for i in s:
		songs.append(i.text)
	
	for j in s:
		links.append(j['href'])

	singer=soup.findAll('a',{'class':'subtitle'})
	for k in singer:
		sing=k.text
		sing= sing.strip()
		singers.append(sing)
	return render_template("index.html", songs=songs, singers=singers)

@app.route('/lyric/<singers>/<song>')
def lyric(song,singers):
	song= song.replace(" ", "-")
	song= song.lower()
	song=song.strip()

	singers= singers.replace(" ","-")
	singers =singers.lower()

	songurl= "http://www.metrolyrics.com/"+song+'-'+singers+".html"
	#return songurl
	r= requests.get(songurl)
	soup= BeautifulSoup(r.text,'html.parser')
	a= soup.findAll('p',{'class':'verse'})

	lyrics=[]
	for i in a:
		lyrics.append(i.text)

	with open('Lyric.cv','w') as file:
		writer=csv.writer(file)
		writer.writerow(lyrics)

	return render_template('lyric.html', lyrics=lyrics)

if __name__=='__main__':
	app.jinja_env.globals.update(zip=zip)
	app.run(host="0.0.0.0", port=8000, debug=True, threaded=True)