#!/usr/bin/python3
# -*- coding; UTF-8 -*-# enable debugging
from mysql.connector import connect, Error

import cgi
import cgitb
cgitb.enable()

host = "localhost"
database = "wedding"
user = "root"
password = "l4m4k1ng"

def run_sql(command, values):
    with connect(host=host, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command, values)
            return cursor.fetchall()

def get_gifts():
    command = "SELECT gifts.*,(SELECT COUNT(*) FROM giftclaims WHERE giftclaims.gift_id=gifts.id) AS claims FROM gifts HAVING claims < quantity;"
    values = []
    return run_sql(command, values)

def output_selectbox(box_name, count):
    print("<select id='{}' name='{}'>".format(box_name, box_name))
    for c in range(count):
        print("<option value='{}'>{}</option>".format(c+1, c+1))
    print("</select>")

def output_gift_list_row(gift_id, image, link, description, quantity):
    print("<tr>")
    print("<td id='giftlist-image'><img src='{}' width='150'></td>".format(image))
    print("<td>")
    print("<a href='{}' target='_blank'>{}</a>".format(link, description))
    print("<br><br><form id='gift_form_{}' method='POST' action='claim.py'>".format(gift_id))
    output_selectbox("quantity_{}".format(gift_id), quantity)
    print(" / {}".format(quantity))
    print("<br><input type='text' name='claim_name_{}' id='claim_name_{}'/>".format(gift_id, gift_id))
    print("<input type='hidden' name='gift_id' value='{}'/>".format(gift_id))
    print("</form>")
    print(" <button onclick='claim({});'>Claim</button>".format(gift_id))
    print("</td>")
    print("</tr>")

def output_gift(gift):
    output_gift_list_row(gift[0], gift[4], gift[2], gift[1], gift[3] - gift[5])

print("Content-Type: text/html;charset=utf-8")
print()

print('''
<html>
	<head>
		<title>Fiona & Brian's Wedding</title>
		<link rel="stylesheet" href="./wedding.css" type="text/css" />
                <script src='./giftlist.js'></script>
	</head>
	<body>
		<h1>Gift List</h1>
		If you do wish to buy us a gift, please choose from one of the options below, or donate to our chosen charities.
                <br><br>
                Once you have chosen an item please click the button to claim it and this will remove it for other guests. 
                <br><br>
                Please do not feel obliged to buy us a gift or donate to our chosen charities. 
                <br><br>
                Thank you very much.
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
''')

gifts = get_gifts()
for gift in gifts:
    output_gift(gift)

print('''
                </table>
                <br><br>
	</body>
</html>
''')
