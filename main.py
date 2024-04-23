from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

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
