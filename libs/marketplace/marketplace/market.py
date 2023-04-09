from flask import Flask

app = Flask(__name__)

@app.route('/market')
def index():
    return 'Hi!'

if __name__ == "__main__":
    app.run()
