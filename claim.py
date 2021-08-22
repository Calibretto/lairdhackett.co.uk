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

def update_sql(command, values):
    with connect(host=host, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command, values)
            connection.commit()

def run_sql(command, values):
    with connect(host=host, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command, values)
            return cursor.fetchall()

def get_gift(gift_id):
    command = "SELECT gifts.quantity,(SELECT COUNT(*) FROM giftclaims WHERE giftclaims.gift_id=gifts.id) AS claims FROM gifts WHERE gifts.id=%s;"
    values = [gift_id]
    return run_sql(command, values)

print("Content-Type: text/html;charset=utf-8")
print()

print("<html><head>")
print("<title>Fiona & Brian's Wedding - Gift List Claim</title>")
print('<link rel="stylesheet" href="./wedding.css" type="text/css" />')
print("</head><body>")

args = cgi.FieldStorage()
if "gift_id" in args:
    gift_id = args["gift_id"].value
    claim_quantity = int(args["quantity_{}".format(gift_id)].value)
    claim_name = args["claim_name_{}".format(gift_id)].value

    gift = get_gift(gift_id)
    gift_quantity_left = gift[0][0] - gift[0][1]

    if claim_quantity <= gift_quantity_left:
        for q in range(claim_quantity):
            command = "INSERT INTO giftclaims(name, gift_id) VALUES(%s, %s)"
            values = [claim_name, gift_id]
            update_sql(command, values)

        print("<h1>Thank you</h1> You have claimed a gift.<br><br>We really appreciate your generosity.")
        print("<br><br>")
        print("If you have made a mistake or want to change your claimed gift, please contact us at <a href='mailto:lairdhackett@gmail.com'>lairdhackett@gmail.com</a>")
        print("<br><br><a href='./index.html'>Back<a/>")
    else:
        print("<h1>Oops!</h1> Someone has already claimed that gift (or there isn't enough of that gift left to claim).<br><br><a href='./giftlist.py'>Go Back</a>")
else:
    print("Something went wrong: <a href='./giftlist.py'>Go Back</a>")

print("</body></html>")
