from collections import namedtuple
import os
import mutagen
import datetime

song_metas = ["title", "artist", "album", "tracknumber", "year"]
SongTup = namedtuple("SongTup", ["id", *song_metas, "path", "type"])

def getyear_from_datetime(datetime_str):
    if datetime_str == '' or datetime_str is None:
        return -1
    try:
        if len(datetime_str)<=4: #assuming this string is just the year
            return int(datetime_str.strip())
        
        if ':' in datetime_str: #assuming 1970-01-01T00:00:00Z format
            return datetime.datetime.strptime(datetime_str.strip(), "%Y-%m-%dT%H:%M:%SZ").year
        
        if '-' in datetime_str: #assuming 1970-01-01 format
            return datetime.datetime.strptime(datetime_str.strip(), "%Y-%m-%d").year
        
    except ValueError:
        print(f"WARNING: one of the provided datetime format: {datetime_str} was not computed correctly")
    return -1

def pathwalk(startpath):
    filelist = []
    for root, _, files in os.walk(startpath, topdown=False):
        for name in files:
            filelist.append((name, os.path.join(root, name)))
    return filelist

def try_get_meta(song, meta_type):
    try:
        return song[meta_type][0]
    except KeyError:
        #wrapping in list because of indexing in filter_search
        if meta_type == "year":
            return getyear_from_datetime(try_get_meta(song, "date"))
        
        #sometimes there's only albumartist listed
        if meta_type == "artist":
            return try_get_meta(song, "albumartist")
        return ""
    
def parse_songtype(song):
    songtype = str(type(song)).split('.')[1].lower()

    #some filetype exceptions
    if "wave" in songtype: #wave -> wav:
        return "wav"
    if "ogg" in songtype or "vorbis" in songtype: #oggvorbis -> ogg
        return "ogg"
    if "id3" in songtype: #id3 -> mp3
        return "mp3"
    if "mp4" in songtype: #easymp4 -> mp4
        return "mp4"
    return songtype

def get_metas(songs):
    songlists = []
    id = 1
    for _, filepath in songs:
        song = mutagen.File(filepath, easy=True)
        if song is not None:
            songlists.append(SongTup(id, *[try_get_meta(song, meta_type) for meta_type in song_metas], filepath.replace("\\","/"), parse_songtype(song)))
            id += 1
    return songlists

if __name__ == "__main__":
    song_files = pathwalk("static/music")
    song_metas = get_metas(song_files)

    try:
        from query import filter_search
    except ImportError:
        from src.query import filter_search

    print("querying songs with 'live' in the title, artist, or album")
    for live_song in filter_search("live", song_metas, ["artist", "album", "title"]):
        print(live_song)

    print("querying songs released in 2018")
    for song_2018 in filter_search("2018", song_metas, ["year"]):
        print(song_2018)

    print("querying song in .wav format")
    for song_wav in filter_search("wav", song_metas, ["type"]):
        print(song_wav)