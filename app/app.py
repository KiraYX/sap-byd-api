from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask!"

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to make it accessible over the network
    app.run(host='0.0.0.0', port=5000)
