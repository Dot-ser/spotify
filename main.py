from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/reply', methods=['GET', 'POST'])
def reply():
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message', '')
        return jsonify({'reply': f'You said: {message}'})
    else:
        return jsonify({'reply': 'Send a POST request with a message to get a reply'})

if __name__ == '__main__':
    app.run(debug=True)
