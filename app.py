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
    session["songs"] = pathwalk("music")
    return render_with_title('index.html')

@app.route("/search")
def search():
    return render_with_title('search.html')

@app.route("/api/song_query")
def query_song():
    query = request.args.get("q")

    songs = session.get("songs")

    filtered_songs = filter_search(query, songs)
    return render_template('query_results.html', songs=filtered_songs)

if __name__ == '__main__':
    app.run()