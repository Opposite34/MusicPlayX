from helper import pathwalk, filter_search
from secret import APP_SECRET_KEY

from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

title = "MusicPlayX"

def render_with_title(html_file, **context):
    return render_template(html_file, title=title, **context)

@app.route("/")
def home():
    session["music"] = pathwalk("music")
    return render_with_title('index.html')

@app.route("/search")
def search():
    return render_with_title('search.html')

@app.route("/query_music")
def query_music():
    query = request.args.get("query")

    music = session.get("music")

    music_list = filter_search(query, music)
    return render_template('query_results.html', music_list=music_list)

if __name__ == '__main__':
    app.run()