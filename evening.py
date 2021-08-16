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
            return cursor.lastrowid

def run_sql(command, values):
    with connect(host=host, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command, values)
            return cursor.fetchall()

def get_rsvp(rsvp_id):
    command = "SELECT * FROM rsvp WHERE id = %s"
    values = [rsvp_id]
    return run_sql(command, values)

def get_guests(rsvp_id):
    command = "SELECT * FROM guests WHERE rsvp_id = %s"
    values = [rsvp_id]
    return run_sql(command, values)

def create_rsvp():
    command = "INSERT INTO rsvp(code, rsvp_date) VALUES(%s, current_timestamp)"
    values = ["----"]
    return update_sql(command, values)

def create_guest(name, rsvp_id):
    command = "INSERT INTO guests(name, rsvp_id, attending, starter, main, dessert, dietary_requirements, evening_only) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    values = [name, rsvp_id, 1, "none", "none", "none", "none", 1]
    update_sql(command, values)

def output_error():
    return "<h1>Error</h1>Unable to create RSVP.<br><br>Please email <a href='lairdhackett@gmail.com'>lairdhackett@gmail.com<a/> for help."

def save_rsvp(names):
    rsvp_id = create_rsvp()
    rsvp = get_rsvp(rsvp_id)
    if rsvp is None:
        return output_error()
    
    for name in names:
        create_guest(name, rsvp_id)

    guests = get_guests(rsvp_id)
    if guests is None or len(guests) == 0:
        return output_error()

    return "<h1>Thank You</h1>Your RSVP has been recorded.<br><br>If you would like to change anything, please email <a href='lairdhackett@gmail.com'>lairdhackett@gmail.com<a/> before the <b>20th September 2021</b>.<br><br><a href='./index.html'>Back</a>"

print("Content-Type: text/html;charset=utf-8")
print()

print("<html>")
print("<head>")
print("<title>Laird / Hackett Wedding - RSVP</title>")
print('<link rel="stylesheet" href="wedding.css" type="text/css" />')
print("<script src='./rsvp.js'></script>")
print("</head>")
print("<body>")

args = cgi.FieldStorage()
names = []
if 'name1' in args and len(args['name1'].value) > 0:
    names.append(args['name1'].value)
if 'name2' in args and len(args['name2'].value) > 0:
    name = args['name2'].value
    if name not in names:
        names.append(name)

if len(names) > 0:
    print(save_rsvp(names))
else:
    print("<h1>RSVP</h1>")
    print("Please enter the names of the people from your invite who are able to attend for drinks and dancing in the evening.<br><br>")
    print("<form method='post'>")
    print("<b>Guest 1</b><br><input type='text' name='name1'/><br><br>")
    print("<b>Guest 2</b><br><input type='text' name='name2'/><br><br>")
    print("<button type='submit'>Submit</button>")
    print("</form>")
