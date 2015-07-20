# -*- coding: utf-8 -*-
"""
Imgur fetcher for getting links of images from Imgur albums
This version of Imgur fetcher is built on the Python package 'imgurpython', please install the package before running the app.
@author: Curiosity Bits (curiositybits.com)
"""

#!/usr/bin/python
#-*-coding:utf-8-*-
#!/usr/bin/env python

import sys
import urllib
import string
import sqlite3

import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text #
from sqlalchemy import DECIMAL
from sqlalchemy import Unicode
from sqlalchemy.sql import join

from types import *

from datetime import datetime, date, time

ids = ['NMFEl',
       'ROYAZ',] # enter the names of the albums to be downloaded
       
from imgurpython import ImgurClient

client_id = ''
client_secret = ''

client = ImgurClient(client_id, client_secret)

Base = declarative_base()

class Messages(Base):
    __tablename__ = 'album_images'
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer)
    image_title = Column(String)
    image_description = Column(String)
    image_datetime = Column(Integer)
    image_views = Column(Integer)
    image_link = Column(String)
    album_name = Column(String)
    def __init__(self, image_id, image_title, image_description, image_datetime,
                 image_views, image_link, album_name):        
        self.image_id = image_id
        self.image_title = image_title
        self.image_description = image_description
        self.image_datetime = image_datetime
        self.image_views = image_views
        self.image_link = image_link
        self.album_name = album_name

    def __repr__(self):
       return "<Organization, Sender('%s', '%s')>" % (self.album_name, self.album_image_link)

def download_album(kid):
    try:
        d = client.get_album_images(album_id = kid)
#        if you want to limit the download to recent images uploaded during the recent week, use the following:
#        d = client.subreddit_gallery(subreddit=kid, window='week',page = page)
    except Exception, e:
        #print "Error reading id %s, exception: %s" % (kid, e)
        return None
     
    print "The number of images available for dowbload: ", len(d)
    return d
    

def write_data(self, d, kid):         
    for item in d:
        import time
        image_id = item.id
        image_title = item.title
        image_description = item.description
        time_s = item.datetime
        image_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_s))
        image_views = item.views
        image_link = item.link
        album_name = kid
        updates = self.session.query(Messages).filter_by(album_name = album_name, image_link = image_link).all() 
        if not updates:
            print "inserting new image URLs:", album_name, image_link                     
            upd = Messages(image_id, image_title, image_description, image_datetime, image_views, image_link, album_name)
            self.session.add(upd)
        else:
            if len(updates) > 1:
                print "Duplicate Warning"
                    
            else:
                print "Duplicate images, Not inserting"
        self.session.commit()
    
class Scrape:
    def __init__(self):    
        engine = sqlalchemy.create_engine("sqlite:///Imgur_fetcher_album_sample.sqlite", echo=False)  
        Session = sessionmaker(bind=engine)
        self.session = Session()  
        Base.metadata.create_all(engine)

    def main(self):
        for n,kid in enumerate(ids):
            print "search albumn:", kid
            sys.stdout.flush()
            kid = kid
            d = download_album(kid)
            write_data(self, d, kid)
            if not d:
                continue 
            if len(d)==0:
                continue
        self.session.close()

if __name__ == "__main__":
    s = Scrape()
    s.main()
