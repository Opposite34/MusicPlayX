def filter_search(query, songs, fields):
   return list(filter(
      lambda song: (
         query.strip().lower() in ''.join([str(getattr(song, field)) for field in fields]).lower()
      ), songs
   ))