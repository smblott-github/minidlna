#!/usr/bin/env python

import sys, sqlite3
prefix = "* "

for db in sys.argv[1:]:
   conn = sqlite3.connect(db)

   c_details = conn.cursor()
   c_details.execute("select ID, PATH, TITLE from DETAILS;")
   details = {}

   for detail in c_details:
      details[detail[1]] = detail

   c_seen = conn.cursor()

   try:
      c_seen.execute("select NAME from SEEN;")
   except:
      conn.close()
      continue

   for path in c_seen:
      try:
         (key, _, title) = details[path[0]]
      except:
         continue
      current_prefix = title[:len(prefix)]
      if current_prefix != prefix:
         print "marking", path
         title = prefix + title
         template = """UPDATE DETAILS SET TITLE=? WHERE ID = ?"""
         c = conn.cursor()
         c.execute(template, (title,key))

   conn.commit()
   conn.close()
