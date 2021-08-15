#!/usr/bin/python3
# -*- coding; UTF-8 -*-# enable debugging
import cgi
import cgitb
cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

print("<html>")
print("<head>")
print("<title>Laird / Hackett Wedding - RSVP</title>")
print('<link rel="stylesheet" href="./style.css" type="text/css" />')
print("<body>")

args = cgi.FieldStorage()
if not 'code' in args or len(args['code']) < 4:
    print("Invalid code.<br><br><a href='./rsvp.py'>Go Back</a>")

print("</body>")
print("</html>")
