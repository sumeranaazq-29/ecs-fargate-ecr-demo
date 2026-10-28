from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from ECS!"

@app.route("/health")
def health():
    return "ok"
