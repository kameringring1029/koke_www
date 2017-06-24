#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
どのボタンが押されたか取得する
'''
html = '''Content-Type: text/html

<html>
<head>
  <title>どのボタンが押されたか取得する</title>
</head>
<body>
<h1>どのボタンが押されたか調べる</h1>
<p>押されたボタンは、「%s」です。</p>
<form action="test.cgi" method="post">
  <input type="submit" name="btn1" value="[1]" />
  <input type="submit" name="btn2" value="[2]" />
  <input type="submit" name="btn3" value="[3]" />
</form>
</body>
</html>
'''

import cgi
f = cgi.FieldStorage()
if f.getfirst('btn1'):
    btn = '1'
elif f.getfirst('btn2'):
    btn = '2'
elif f.getfirst('btn3'):
    btn = '3'
else:
    btn = ''
print html % btn

