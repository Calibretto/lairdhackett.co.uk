#!/usr/bin/python3
# -*- coding; UTF-8 -*-# enable debugging
from mysql.connector import connect, Error

import cgi
import cgitb
cgitb.enable()

def send_email(subject, body):
    pass 

host = "localhost"
database = "wedding"
user = "root"
password = "l4m4k1ng"

def run_sql(command, values):
    with connect(host=host, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command, values)
            return cursor.fetchall()

def update_sql(command, values):
    with connect(host=host, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command, values)
            connection.commit()

def update_rsvp(rsvp_id):
    command = "UPDATE rsvp SET rsvp_date=current_timestamp WHERE id=%s"
    values = [rsvp_id]
    update_sql(command, values)

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
    if "plus_one_{}".format(guest_id) in args:
        guest_name = args["plus_one_{}".format(guest_id)].value

    g = {
        "id": guest_id,
        "name": guest_name,
        "attendance": args["attendance_{}".format(guest_id)].value,
        "main": "error",
        "starter": "error",
        "dessert": "error"
    }
    
    child = guest[9]
    if child == 1:
        g["main"] = "child"
        g["starter"] = "child"
        g["dessert"] = "child"
    elif 'main_{}'.format(guest_id) in args:
        g["main"] = args["main_{}".format(guest_id)].value
        g["starter"] = args["starter_{}".format(guest_id)].value
        g["dessert"] = args["dessert_{}".format(guest_id)].value

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
    else:
        g["dietary"] = "none"

    return g

def guest_output(guest):
    return "Name: {}\nAttending: {}\nMenu Choices: {}, {}, {}\nDietary Requirements: {}".format(guest["name"], guest["attendance"], guest["starter"], guest["main"], guest["dessert"], guest["dietary"])

def update_guest(guest):
    attendance = 0 if guest["attendance"] == "neither" else 1
    evening_only = 1 if guest["attendance"] == "evening" else 0

    command = "UPDATE guests SET name=%s, attending=%s, starter=%s, main=%s, dessert=%s, dietary_requirements=%s, evening_only=%s WHERE id=%s"
    values = [guest["name"], attendance, guest["starter"],  guest["main"],  guest["dessert"], guest["dietary"], evening_only, guest["id"]]
    update_sql(command, values)

print("Content-Type: text/html;charset=utf-8")
print()

print("<html>")
print("<head>")
print("<title>Laird / Hackett Wedding - RSVP</title>")
print('<link rel="stylesheet" href="./wedding.css" type="text/css" />')
print("<body>")

args = cgi.FieldStorage()
if not 'code' in args or len(args['code'].value) < 4 or args['code'].value == '----':
    print("Invalid code.<br><br><a href='./rsvp.py'>Go Back</a>")
else:
    code = args['code'].value.upper()
    rsvp = get_rsvp(code)
    if rsvp is None:
        print("Invalid code.<br><br><a href='./rsvp.py'>Go Back</a>")
    else:
        print("<h1>Thank You</h1><br>Your RSVP has been saved.")
        print("<br><br>If you would like to update your selections, please return to the <a href='./rsvp.py'>RSVP</a> page and re-enter your code.<br><br>Please note that any submissions after the <b>20th September 2021</b> may not be counted.<br><br><a href='./index.html'>Back<a/>")

        email_subject = "RSVP"
        email_body = "An RSVP has been submitted.\n\n"

        rsvp_id = rsvp[0][0]
        guests = get_guests(rsvp_id)
        for guest in guests:
            g = parse_guest(guest, args)
            update_guest(g)
            email_body += guest_output(g)
            email_body += "\n\n"

        update_rsvp(rsvp_id)
        send_email(email_subject, email_body)

print("</body>")
print("</html>")
