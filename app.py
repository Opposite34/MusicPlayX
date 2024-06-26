from src.get_music import pathwalk, get_metas
from src.query import filter_search
from secret import APP_SECRET_KEY

from flask import Flask, render_template, request, session, Response, abort
from flask_session import Session

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_COOKIE_SAMESITE"] = 'None'
app.config["SESSION_COOKIE_SECURE"] = 'True'
Session(app)

title = "MusicPlayX"

def render_with_title(html_file, **context):
    return render_template(html_file, title=title, **context)

@app.route("/")
def home():
    return render_with_title('index.html')

@app.route("/search")
def search():
    return render_with_title('search.html')

@app.route("/api/song_query")
def query_song():
    if session.get("songs") == None:
        session["songs"] = get_metas(pathwalk("static/music"))

    query = request.args.get("q")
    songs = session.get("songs")

    filtered_songs = filter_search(query, songs, ["title", "artist", "album"])
    return render_template('query_results.html', songs=filtered_songs)

@app.route("/api/refresh_dir")
def refresh_dir():
    session["songs"] = get_metas(pathwalk("static/music"))

    #force refresh as the song list will change
    resp = Response()
    resp.headers['HX-Refresh'] = 'true'
    return resp


def send_player(songid):
    if session.get("songs") == None:
        session["songs"] = get_metas(pathwalk("static/music"))
    songs = session.get("songs")
    try:
        rendered = render_template('audio_player.html', song=songs[songid-1])
        session["curr_songid"] = songid
        return rendered
    except IndexError:
        abort(404)

@app.route("/api/play")
def play_song():
    songid = int(request.args.get("id"))
    return send_player(songid)

@app.route("/api/play/next")
def play_next_song():
    if session.get("curr_songid") == None:
        abort(404)
    songid = session.get("curr_songid")
    return send_player(songid+1)

if __name__ == '__main__':
    app.run()
