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

def get_rsvp(code):
    command = "SELECT * FROM rsvp WHERE code = %s"
    values = [code.upper()]
    return run_sql(command, values)

def get_guests(rsvp_id):
    command = "SELECT * FROM guests WHERE rsvp_id = %s"
    values = [rsvp_id]
    return run_sql(command, values)

def parse_guest(guest, args):
    guest_id = guest[0]
    guest_name = guest[1]
    if guest_name.lower() == "guest":
        if "plus_one_{}".format(guest_id) in args:
            guest_name = args["plus_one_{}".format(guest_id)].value

    g = {
        "id": guest_id,
        "name": guest_name,
        "attendance": args["attendance_{}".format(guest_id)].value,
        "main": args["main_{}".format(guest_id)].value,
        "starter": args["starter_{}".format(guest_id)].value,
        "dessert": args["dessert_{}".format(guest_id)].value,
    }

    if "vegan_{}".format(guest_id) in args:
        g["main"] = "vegan"
        g["starter"] = "vegan"
        g["dessert"] = "vegan"

    if g["attendance"] == "evening" or g["attendance"] == "neither":
        g["main"] = "none"
        g["starter"] = "none"
        g["dessert"] = "none"

    if "dietary_{}".format(guest_id) in args:
        g["dietary"] = args["dietary_{}".format(guest_id)].value

    return g

print("Content-Type: text/html;charset=utf-8")
print()

print("<html>")
print("<head>")
print("<title>Laird / Hackett Wedding - RSVP</title>")
print('<link rel="stylesheet" href="./style.css" type="text/css" />')
print("<body>")

args = cgi.FieldStorage()
if not 'code' in args or len(args['code'].value) < 4:
    print("Invalid code.<br><br><a href='./rsvp.py'>Go Back</a>")
else:
    code = args['code'].value.upper()
    rsvp = get_rsvp(code)
    if rsvp is None:
        print("Invalid code.<br><br><a href='./rsvp.py'>Go Back</a>")
    else:
        rsvp_id = rsvp[0][0]
        guests = get_guests(rsvp_id)
        for guest in guests:
            g = parse_guest(guest, args)
            print(g)

print("</body>")
print("</html>")
