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

def guest_attendance(guest):
    guest_id = guest[0]
    options = guest_label(guest)
    options += "<br><input type='radio' name='attendance_{}' id='day_{}' value='day' onclick='attendance_changed(\"day\", {})' checked/> ".format(guest_id, guest_id, guest_id)
    options += "<label for='day_{}'>Full day</label>".format(guest_id)
    options += "<br><input type='radio' name='attendance_{}' id='evening_{}' value='evening' onclick='attendance_changed(\"evening\", {})'/> ".format(guest_id, guest_id, guest_id)
    options += "<label for='evening_{}'>Evening only</label>".format(guest_id)
    options += "<br><input type='radio' name='attendance_{}' id='neither_{}' value='neither' onclick='attendance_changed(\"neither\", {})'/>".format(guest_id, guest_id, guest_id)
    options += "<label for='neihter_{}'>Unable to attend</label>".format(guest_id)
    return options

def guest_label(guest):
    guest_name = guest[1]
    guest_id = guest[0]

    if guest_name.lower() == "guest":
        guest_name = "<b>Guest:</b> <input name='plus_one_{}' id='plus_one_{}' value='+1'/>".format(guest_id, guest_id)
    else:
        guest_name = "<b>{}</b>".format(guest_name)

    return guest_name

def guest_row(title, contents):
        return "<tr><td valign='top'>{}</td><td valign='top'>{}</td></tr>".format(title, contents)

def attendance_form(code):
    try:
        rsvp = get_rsvp(code)
        if rsvp is not None and len(rsvp) > 0 and len(rsvp[0]) > 0:
            rsvp_id = rsvp[0][0]
            guests = get_guests(rsvp_id)
            table = "<table>"
            for guest in guests:
                table += guest_attendance(guest)
                table += "<br><br>"
            table += "</table>"
            return table
        else:
            return "Invalid code"
    except Error as e:
        return "An error occurred, please reload the page."

def menu_item(item, value, course, guest_id, selected = False):
    item_id = "{}_{}".format(course, guest_id)
    checked = "checked" if selected else ""
    item_checkbox = "<input type='radio' name='{}' id='{}' value='{}' {}/>".format(item_id, item_id, value, checked)
    item_label = " <label for='{}'>{}</label>".format(item_id, item)
    return guest_row(item_checkbox, item_label)

def menu_table(guest):
    guest_name = guest[1].split(" ")[0]
    guest_id = guest[0]

    options = "<input type='checkbox' id='vegan_{}' name='vegan_{}' onclick='vegan_selected({})'/> <label for='vegan_{}'>Vegan</label>".format(guest_id, guest_id, guest_id, guest_id)

    menu = "<table id='menu_{}'>".format(guest_id)
    menu += guest_row("<u>Starter<u/>", "")
    menu += menu_item("Roasted tomato and basil soup. (v)", "soup", "starter", guest_id, True)
    menu += menu_item("Chicken and bacon terrine with mixed leaves.", "terrine", "starter", guest_id)
    menu += guest_row("<u>Main<u/>", "")
    menu += menu_item("Chicken stuffed with haggis, fondant potato, carrots, whisky sauce.", "chicken", "main", guest_id, True)
    menu += menu_item("Steak pie with roast potatoes and seasonal vegetables.", "steak", "main", guest_id)
    menu += menu_item("Vegetarian main course. (v)", "vegetarian", "main", guest_id)
    menu += guest_row("<u>Dessert</u>", "")
    menu += menu_item("Roasted apple crumble tart, vanilla cream, almond tuille. (v)", "crumble", "dessert", guest_id, True)
    menu += menu_item("Sticky toffee pudding and vanilla ice cream. (v)", "pudding", "dessert", guest_id)
    menu += "</table>"

    table = "<b>{}</b>".format(guest_name)
    table += "<div id='evening_only_{}' style='display: none;'>None</div>".format(guest_id)
    table += "<table id='choices_{}'>".format(guest_id)
    table += "<tr><td colspan='2'>{}</td></tr>".format(options)
    table += "<tr><td colspan='2'>{}</td></tr>".format(menu)
    table += guest_row("&nbsp;", "&nbsp;")
    table += "<tr><td colspan='2'>Dietary Requirements: <input type='text' name='dietary_{}' id='dietary_{}'/></td></tr>".format(guest_id, guest_id)
    table += "<table>"
    return table

def menu_choices(code):
    try:
        rsvp = get_rsvp(code)
        if rsvp is not None and len(rsvp) > 0 and len(rsvp[0]) > 0:
            rsvp_id = rsvp[0][0]
            guests = get_guests(rsvp_id)
            table = ""
            for guest in guests:
                table += menu_table(guest)
                table += "<br><br>"
            return table
    except Error as e:
        return "An error has occurred, please reload the page."

def code_value(code):
    html = code.upper()
    html += " <input type='hidden' name='code' id='code' value='{}'/>".format(code.upper())
    return html

def day_guest_form(code):
    print("<form method='post' action='submitday.py'>")
    print("<table>")
    print(guest_row("<b>Your Code</b>", code_value(code)))
    print(guest_row("<b>Guests</b>", attendance_form(code)))
    print(guest_row("&nbsp;", "&nbsp;"))
    print(guest_row("<b>Menu Choices</b>", menu_choices(code)))
    print("<tr><td><button type='submit'>Submit</button></td><td></td></tr>")
    print("</table>")
    print("</form>")

print("Content-Type: text/html;charset=utf-8")
print()

print("<html>")
print("<head>")
print("<title>Laird / Hackett Wedding - RSVP</title>")
print('<link rel="stylesheet" href="./wedding.css" type="text/css" />')
print("<script src='./rsvp.js'></script>")
print("</head>")
print("<body>")

print("<h1>RSVP</h1>")
args = cgi.FieldStorage()
if 'code' in args and len(args['code'].value) == 4:
    code = args['code'].value
    day_guest_form(code)
else:
    print("<form method='post'>")
    print("Enter your 4 letter code: <input name='code'/>")
    print("<br><button type='submit'>Submit</button>")
    print("</form>")
    print("<br>")
    print("<b>OR</b>")
    print("<br><br>")
    print("<form action='./evening.py'>")
    print("<button type='submit'>I don't have a code</button>")
    print("</form>")

print("</body>")
