from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ia')
def ia_home():
    return render_template('ia.html')


if __name__ == '__main__':
    app.run(debug=True)
