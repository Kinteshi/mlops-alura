from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import os

reg = pickle.load(open('models/reg.pkl', 'rb'))
app = Flask(__name__)  # create an instance of the Flask class
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')  # decorator
def index():
    return '<h1>Hello World!</h1>'


@app.route('/sentiment/<string:phrase>')
@basic_auth.required
def sentiment(phrase):
    tb = TextBlob(phrase)
    lang = tb.detect_language
    if lang != 'en':
        tb = tb.translate(to='en')
    polarity = tb.sentiment.polarity
    return '<h1>' + f'Polarity: {polarity}' + '</h1>'


@app.route('/price/', methods=['POST'])
@basic_auth.required
def price():
    data = request.get_json()
    cols = ['tamanho', 'ano', 'garagem']
    input_data = [data[col] for col in cols]
    price = reg.predict([input_data])[0]
    return jsonify({'price': price})


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0' 
        )  # run the app in debug mode
