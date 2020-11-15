from flask import Flask, jsonify
# import controller
# import model

app= Flask(__name__)

@app.route('/getRoute', methods=['GET'])
def test1():
    return jsonify(value='Testing')


if __name__ == '__main__':
   app.run(debug = True)