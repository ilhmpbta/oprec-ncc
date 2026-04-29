import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/health')
def health_check():
    return render_template('health.html'), 200

# for local development purposes
# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)