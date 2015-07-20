# -*- coding: utf-8 -*-
"""
Imgur fetcher for downloading images from keyword search
This version of Imgur fetcher is built on the Python package 'imgurpython', please install the package before running the app.
@author: Curiosity Bits (curiositybits.com)
"""

import sys
import urllib
import string
#import simplejson
import sqlite3


import time
import datetime
from pprint import pprint

import sqlalchemy 
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Unicode 
from types import *


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

engine = sqlalchemy.create_engine("sqlite:///C:/xxxxxx/Imgur_fetcher_reddit_sampler.sqlite", echo=False)  #OR FOUR SLASHES FOR ABSOLUTE FILE PATH
Session = sessionmaker(bind=engine)
session = Session()  
Base.metadata.create_all(engine)

all_links = session.query(Messages).all()
print len(all_links)
for row in all_links[1:]:
    #print row.image_link
    sys.stdout.flush()
    image_url = row.image_link
    if image_url.endswith('jpg') or image_url.endswith('gif') or image_url.endswith('png') or image_url.endswith('bmp'):
        media_url_split = image_url.split('.')
    #print media_url_split
        extension = media_url_split[-1]
    #print extension 
        image_name = str(row.id)+'.'+extension
        filepath = "C:/xxxxxx/image_downloaded"
        urllib.urlretrieve(image_url, filepath + '/'+ image_name)
        print "downloading", image_name
    else:
        print "this link may contain multiple images. Please check!"
    session.commit()

session.close()