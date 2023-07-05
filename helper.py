from collections import namedtuple
import os
import mutagen
import datetime

song_metas = ["title", "artist", "album", "tracknumber", "year"]
SongTup = namedtuple("SongTup", ["id", *song_metas, "path"])

def getyear_from_datetime(datetime_str):
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
      return ""
   
def get_metas(songs):
   songlists = []
   id = 1
   for _, filepath in songs:
      song = mutagen.File(filepath, easy=True)
      if song is not None: 
         songlists.append(SongTup(id, *[try_get_meta(song, meta_type) for meta_type in song_metas], filepath))
         id += 1
   return songlists
         
def filter_search(query, songs):
   return list(filter(
      lambda song: (query.lower() in (f"{song.title} {song.artist} {song.album}").lower()), songs
   ))

if __name__ == "__main__":
   song_files = pathwalk("music/")
   song_metas = get_metas(song_files)

   #querying songs with "live" in the title, artist, or album
   for live_song in filter_search("live", song_metas):
      print(live_song)