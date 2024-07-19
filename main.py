from flask import Flask, jsonify

app = Flask(name)

@app.route('/hi', methods=['GET'])
def say_hi():
return jsonify({'message': 'Hi'})

if name == 'main':
app.run(debug=True)
