from flask import Flask, request

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    return f"Message received: {data}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)