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
		If you do wish to buy us a gift, please choose from one of the options below, or donate to our chosen charities.<br>If you do pick a gift from the list below, please click the button to 'claim' it so that it is removed from the list for other guests.<br><br>Please do not feel obliged to buy us a gift or donate. Thank you very much.
		<br><br>
		<h2>Charities</h2>
		<b>Crohn's &amp; Colitis UK</b>
		<br><img src='candcuk.jpg' width='250'/>
		<br>"We’re here to give people affected by Crohn's and Colitis hope, comfort and confidence. To make sure their voices are heard and help them live freer, fuller lives."
		<br>Find out more <a href='https://www.crohnsandcolitis.org.uk/about-us/what-we-do' target='_blank'>here</a>.
		<br><br>
		<a href='https://e.crohnsandcolitis.org.uk/donations/main-donation/donate'>Donate</a>
		<br><br>
		<b>Samaritans</b>
		<br><img src='./samaritans.jpg' width='250'/>
		<br>Every day, Samaritans volunteers respond to around 10,000 calls for help.
		<br>Find out more <a href='https://www.samaritans.org/scotland/about-samaritans/our-organisation/what-we-do/' target='_blank'>here</a>.
		<br><br>
		<a href='https://www.samaritans.org/scotland/donate-now/'>Donate</a>
		<br><br>
		Gift list items will be added soon.
	</body>
</html>
''')
