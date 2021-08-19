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
		<link rel="stylesheet" href="./wedding.css" type="text/css" />
	</head>
	<body>
		<h1>Gift List</h1>
		If you do wish to buy us a gift, please choose from one of the options below, or donate to our chosen charities.<br><br>If you do pick a gift from the list below, please click the button to 'claim' it so that it is removed from the list for other guests.<br><br>Please do not feel obliged to buy us a gift or donate.<br><br>Thank you very much.
		<br><br>
                <a href='./index.html'>Home</a>
                <br><br>
		<h2>Charities</h2>
                <div id='charity_wrapper'>
		<div id='charity'>
			<b>Crohn's &amp; Colitis UK</b>
			<br><img id='charity' src='candcuk.jpg' width='250'/>
			<br>"We’re here to give people affected by Crohn's and Colitis hope, comfort and confidence."
			<br><br>Find out more <a href='https://www.crohnsandcolitis.org.uk/about-us/what-we-do' target='_blank'>here</a>.
			<br><br>
			<a href='https://e.crohnsandcolitis.org.uk/donations/main-donation/donate'>Donate</a>
                <br><br>
		</div>
		<div id='charity'>
			<b>Samaritans</b>
			<br><img id='charity' src='./samaritans.jpg' width='250'/>
			<br>"Every day, Samaritans volunteers respond to around 10,000 calls for help."
			<br><br>Find out more <a href='https://www.samaritans.org/scotland/about-samaritans/our-organisation/what-we-do/' target='_blank'>here</a>.
			<br><br>
			<a href='https://www.samaritans.org/scotland/donate-now/'>Donate</a>
		    <br><br>
                </div>
                </div>
		<h2>Gifts</h2>
                <table id='giftlist' cellpadding='5'>
                    <tr>
                        <td id='giftlist-image'><img src='johnlewis.jpeg' width='150'></td>
                        <td><a href='https://www.johnlewis.com/customer-services/prices-and-payment/gift-cards' target='_blank'>John Lewis Gift Voucher</a></td>
                    </tr>
                    <tr>
                        <td id='giftlist-image'><img src='bandq.jpeg' width='150'></td>
                        <td><a href='https://www.diy.com/services/gift-cards' target='_blank'>B&amp;Q Gift Voucher</a></td>
                    </tr>
                </table>
                <br><br>
		<i>Other gift list items will be added soon.</i>
                <br><br>
	</body>
</html>
''')
