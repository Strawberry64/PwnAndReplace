from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import requests
import hashlib

app = Flask(__name__)
bootstrap = Bootstrap5(app)

def checkPassword(password):
    hashOne = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    response = requests.get('https://api.pwnedpasswords.com/range/' + hashOne[:5])
    seperatedLines = response.text.splitlines()
    hashTwo = []
    for line in seperatedLines:
        hashTwo.append(line.split(':'))
    for h in hashTwo:
        if h[0] == hashOne[5:]:
            return True 
    return False

@app.route('/')
def index():
    return render_template('pwned.html')

@app.route('/submit', methods=['POST'])
def submit():
    password = request.form['password']
    if checkPassword(password):
        message = 'Password has been pwned! If you would like to make a new password that has not been pwned, <a href="/password">go here</a>'
        image = 'pwned.jpg'
    else:
        message = 'Password has not been pwned.'
        image = 'good.webp'
    return render_template('pwned.html', message=message, image=image)


@app.route('/password')
def password():
    return render_template('password.html')


if __name__ == '__main__':
    app.run(debug=True)


"""
Test cases
password = '123Password'
print(password)
if checkPassword(password):
    print('Password has been pwned!')
else:
    print('Password has not been pwned.')
Printed True
print(" --------- ")
password = 'gorrilagoingtothebeachinsearchoftheforsakenbanana'
print(password)
if checkPassword(password):
    print('Password has been pwned!')
else:
    print('Password has not been pwned.')
Printed False
"""

"""
Sources
big example on how to use the hashlib library and code, mainly used
https://ioflood.com/blog/python-hashlib/

another step by step example on using the hashlib library for SHA1
https://www.codeease.net/programming/python/generate-sha1-python

official python docs on the hashlib library, although a lot less user friendly learning experience
https://docs.python.org/3/library/hashlib.htmlhttps://docs.python.org/3/library/hashlib.html 

official Pwned API docs with some information detailing how Pwned Passwords API works
https://haveibeenpwned.com/API/v3#AllBreacheshttps://haveibeenpwned.com/API/v3#AllBreaches

"""
