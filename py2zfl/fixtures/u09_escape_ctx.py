import os, html
x = html.escape(input())
os.system("echo " + x)           # EXPECT REFUTED (html.escape does not protect a shell)
