# -*- coding: utf-8 -*-
"""
Imgur fetcher for getting links of images from reddit timeline
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

ids = ['buffalo',
       'isis',] # enter your search terms
       
from imgurpython import ImgurClient

client_id = ''
client_secret = ''

client = ImgurClient(client_id, client_secret)

Base = declarative_base()

class Messages(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    image_title = Column(String)
    image_datetime = Column(Integer)
    image_views = Column(Integer)
    image_link = Column(Text)
    image_vote = Column(Integer)
    pagenumber = Column(String)
    def __init__(self, keyword, image_title, image_datetime, image_views, image_link, 
                 image_vote,pagenumber):        
        self.keyword = keyword
        self.image_title = image_title
        self.image_datetime = image_datetime
        self.image_views = image_views
        self.image_link = image_link
        self.image_vote = image_vote
        self.pagenumber = pagenumber
    def __repr__(self):
       return "<Organization, Sender('%s', '%s')>" % (self.image_link, self.keyword)

def download_reddit_gallery(kid, page):
    try:
        d = client.subreddit_gallery(subreddit=kid, page = page)
#        if you want to limit the download to recent images uploaded during the recent week, use the following:
#        d = client.subreddit_gallery(subreddit=kid, window='week',page = page)
    except Exception, e:
        #print "Error reading id %s, exception: %s" % (kid, e)
        return None
     
    print "The number of images available for dowbload: ", len(d)
    return d
    

def write_data(self, d, kid, page):         
    for item in d:
        import time
        keyword = kid
        image_title = item.title
        time_s = item.datetime
        image_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_s))
        image_views= item.views
        image_link = item.link
        image_vote = item.vote
        pagenumber = page
        updates = self.session.query(Messages).filter_by(image_link = image_link, keyword = keyword).all() 
        if not updates:
            print "inserting new image URLs:", image_link, pagenumber                     
            upd = Messages(keyword, image_title, image_datetime, image_views, 
                           image_link, image_vote, pagenumber)
            self.session.add(upd)
        else:
            if len(updates) > 1:
                print "Duplicate Warning"
                    
            else:
                print "Duplicate images, Not inserting"
        self.session.commit()
    
class Scrape:
    def __init__(self):    
        engine = sqlalchemy.create_engine("sqlite:///Imgur_fetcher_reddit_sampler.sqlite", echo=False)  
        Session = sessionmaker(bind=engine)
        self.session = Session()  
        Base.metadata.create_all(engine)

    def main(self):
        for n,kid in enumerate(ids):
            print "search:", kid
            sys.stdout.flush()
            for page in range(5): 
                kid = kid
                print "------XXXXXX------ STARTING PAGE", page
                page = page
                d = download_reddit_gallery(kid, page)
                write_data(self, d, kid, page)
                if not d:
                    continue 
                if len(d)==0:
                    continue
        self.session.close()


if __name__ == "__main__":
    s = Scrape()
    s.main()
