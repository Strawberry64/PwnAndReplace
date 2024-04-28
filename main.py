from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import requests
#hashlib is a built in python library that can make hashs
import hashlib

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/')
def index():
    return render_template('pwned.html')

@app.route('/submit', methods=['POST'])
def submit():
    password = request.form['password']
    #empty for now
    return 'Password submitted: ' + password

if __name__ == '__main__':
    app.run(debug=True)


def checkPassword(password):
    #the sha1() function is the function that hashes the argument
    #the encode() function is used to convert the string into something that sha1() function can use
    #the hexdigest() function is used to convert the hash back into a string
    #the upper() function makes all the characters uppercase. it is nessecery because pwned passwrods api needs uppercase string hashes
    hashOne = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    #request goes through, will return all hashes that begin with the first 5 characters of our hash
    response = requests.get('https://api.pwnedpasswords.com/range/' + hashOne[:5])
    
    #seperates all the values into a list by every new line
    seperatedLines = response.text.splitlines()

    #seperates every index into a 2d array so hash values and appearances are seperated
    hashTwo = []
    for line in seperatedLines:
        hashTwo.append(line.split(':'))

    # print(hashTwo)
    
    #compares the hashes returned by the api with the hash we made with every character after the 5th character
    #this is done because the hashes by the api have the first 5 characters removed, because they are all the same as our initial hash
    #this is also a security measure as removing the first 5 makes it ambigiuos what the first 5 values are, so attackers can't use it without decrypting the first hash
    for h in hashTwo:
        if h[0] == hashOne[5:]:
            # print(h[0])
            # print(hashOne)
            return True 
    return False

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
big example on how to use the hashlib library and code
https://ioflood.com/blog/python-hashlib/

another step by step example on using the hashlib library for SHA1
https://www.codeease.net/programming/python/generate-sha1-python

official python docs on the hashlib library, although a lot less user friendly learning experience
https://docs.python.org/3/library/hashlib.htmlhttps://docs.python.org/3/library/hashlib.html 
"""
