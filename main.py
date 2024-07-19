from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    url = f'https://spotifydown.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for result in soup.find_all('div', {'class': 'result'}):
        title = result.find('h2', {'class': 'title'}).text
        link = result.find('a', {'class': 'link'})['href']
        results.append({'title': title, 'link': link})
    return jsonify(results)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    response = requests.get(url, stream=True)
    filename = url.split('/')[-1]
    return send_file(response, as_attachment=True, attachment_filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
