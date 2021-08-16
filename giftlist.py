#!/usr/bin/python3
# -*- coding; UTF-8 -*-# enable debugging
from mysql.connector import connect, Error

import cgi
import cgitb
cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

print('''
<html>
	<head>
		<title>Fiona & Brian's Wedding</title>
		<link rel="stylesheet" href="./style.css" type="text/css" />
	</head>
	<body>
		<h1>Gift List</h1>
		If you do wish to buy us a gift, please choose from one of the options below, or donate to our chosen charities.<br>If you do pick a gift from the list below, please click the button to 'claim' it so that it is removed from the list for other guests.
		<br><br>
		<h2>Charities</h2>
		<b>Samaritans</b>
		<img src='./samaritans.jpg'/>
		Every day, Samaritans volunteers respond to around 10,000 calls for help. FInd out more <a href='https://www.samaritans.org/scotland/about-samaritans/our-organisation/what-we-do/' target='_blank'>here</a>
		<br><br>
		<a href='https://www.samaritans.org/scotland/donate-now/'>Donate</a>
	</body>
</html>
''')