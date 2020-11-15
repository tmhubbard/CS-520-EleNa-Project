from flask import Flask
import controller
import model

app= Flask(__name__)


@app.route('/')
def test1():
    return 'Testing'


if __name__ == '__main__':
   app.run(debug = True)