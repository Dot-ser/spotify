from flask import Flask, request, send_file
from flask_cors import CORS
from puppeteer import launch

app = Flask(__name__)
CORS(app)

@app.route('/screenshot', methods=['GET'])
def screenshot():
    url = request.args.get('url')
    browser = launch(headless=True)
    page = browser.newPage()
    page.goto(url)
    screenshot = page.screenshot()
    browser.close()
    return send_file(screenshot, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
