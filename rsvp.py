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
    guest_attending = guest[3]
    guest_evening = guest[8]
    guest_attendance = "day"
    if guest_attending == 1 and guest_evening == 1:
        guest_attendance = "evening"
    elif guest_attending == 0 and guest_evening == 0:
        guest_attendance = "neither"

    options = guest_label(guest)
    option_clicked = " checked" if guest_attendance == "day" else ""
    options += "<br><input type='radio' name='attendance_{}' id='day_{}' value='day' onclick='attendance_changed(\"day\", {})'{}/> ".format(guest_id, guest_id, guest_id, option_clicked)
    options += "<label for='day_{}'>Full day</label>".format(guest_id)
    
    option_clicked = " checked" if guest_attendance == "evening" else ""
    options += "<br><input type='radio' name='attendance_{}' id='evening_{}' value='evening' onclick='attendance_changed(\"evening\", {})'{}/> ".format(guest_id, guest_id, guest_id, option_clicked)
    options += "<label for='evening_{}'>Evening only</label>".format(guest_id)
    
    option_clicked = " checked" if guest_attendance == "neither" else ""
    options += "<br><input type='radio' name='attendance_{}' id='neither_{}' value='neither' onclick='attendance_changed(\"neither\", {})'{}/>".format(guest_id, guest_id, guest_id, option_clicked)
    options += "<label for='neither_{}'>Unable to attend</label>".format(guest_id)
    return options

def guest_label(guest):
    guest_name = guest[1]
    guest_id = guest[0]
    guest_plus_one = guest[10]

    if guest_plus_one == 1:
        guest_name = "<b>Guest:</b> <input name='plus_one_{}' id='plus_one_{}' value='{}'/>".format(guest_id, guest_id, guest_name)
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
    item_id = "{}_{}".format(value, guest_id)
    item_name = "{}_{}".format(course, guest_id)
    checked = "checked" if selected else ""
    item_checkbox = "<input type='radio' name='{}' id='{}' value='{}' {}/>".format(item_name, item_id, value, checked)
    item_label = " <label for='{}'>{}</label>".format(item_id, item)
    return guest_row(item_checkbox, item_label)

def menu_table(guest):
    guest_name = guest[1].split(" ")[0]
    guest_attending = guest[3]
    guest_evening = guest[8]
    guest_id = guest[0]
    guest_starter = guest[4]
    guest_main = guest[5]
    guest_dessert = guest[6]
    guest_dietary = guest[7]
    child = guest[9]
    guest_attendance = "day" if guest_attending == 1 and guest_evening == 0 else "other"

    if child == 1:
        table = "<b>{}</b>".format(guest_name)
        table += "<div id='choices_{}'>Kid's Menu</div>".format(guest_id)
        table += "<div id='evening_only_{}' style='display: none;'>None</div>".format(guest_id)
        return table

    options_selected = "" if guest_main != 'vegan' else " checked"
    options = "<input type='checkbox' id='vegan_{}' name='vegan_{}' onclick='vegan_selected({})'{}/> <label for='vegan_{}'>Vegan</label>".format(guest_id, guest_id, guest_id, options_selected, guest_id)

    menu_display = "" if guest_main != 'vegan' else " style='display: none;'"
    menu = "<table id='menu_{}'{}>".format(guest_id, menu_display)
    menu += guest_row("<u>Starter<u/>", "")
    menu += menu_item("Roasted tomato and basil soup. (v)", "soup", "starter", guest_id, (guest_starter == 'soup'))
    menu += menu_item("Chicken and bacon terrine with mixed leaves.", "terrine", "starter", guest_id, (guest_starter == 'terrine'))
    menu += guest_row("<u>Main<u/>", "")
    menu += menu_item("Chicken stuffed with haggis, fondant potato, carrots, whisky sauce.", "chicken", "main", guest_id, (guest_main == 'chicken'))
    menu += menu_item("Steak pie with roast potatoes and seasonal vegetables.", "steak", "main", guest_id, (guest_main == 'steak'))
    menu += menu_item("Vegetarian main course. (v)", "vegetarian", "main", guest_id, (guest_main == 'vegetarian'))
    menu += guest_row("<u>Dessert</u>", "")
    menu += menu_item("Roasted apple crumble tart, vanilla cream, almond tuille. (v)", "crumble", "dessert", guest_id, (guest_dessert == 'crumble'))
    menu += menu_item("Sticky toffee pudding and vanilla ice cream. (v)", "pudding", "dessert", guest_id, (guest_dessert == 'pudding'))
    menu += "</table>"

    div_display = "" if guest_attendance != 'day' else " style='display: none;'"
    table_display = "" if guest_attendance == 'day' else " style='display: none;'"
    table = "<b>{}</b>".format(guest_name)
    table += "<div id='evening_only_{}'{}>None</div>".format(guest_id, div_display)
    table += "<table id='choices_{}'{}>".format(guest_id, table_display)
    table += "<tr><td colspan='2'>{}</td></tr>".format(options)
    table += "<tr><td colspan='2'>{}</td></tr>".format(menu)
    table += guest_row("&nbsp;", "&nbsp;")
    table += "<tr><td colspan='2'>Dietary Requirements: <input type='text' name='dietary_{}' id='dietary_{}' value='{}'/></td></tr>".format(guest_id, guest_id, guest_dietary)
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
    print("<table cellspacing='10'>")
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
if 'code' in args and len(args['code'].value) == 4 and args['code'].value is not '----':
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
