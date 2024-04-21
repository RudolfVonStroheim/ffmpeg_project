from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html', title='MPEG ONLINE: Easy video and audio converter tool.', log_st=0)

if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
