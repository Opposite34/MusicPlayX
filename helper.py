import os

def pathwalk(startpath):
   filelist = []
   for root, _, files in os.walk(startpath, topdown=False):
      for name in files:
         filelist.append((name, os.path.join(root, name)))
   return filelist

def filter_search(query, music):
   return list(filter(lambda tup: query in tup[0].lower(), music))