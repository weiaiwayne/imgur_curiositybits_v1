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
    image_id = Column(Integer)
    image_link = Column(Text)
    image_title = Column(String)
    image_description = Column(String)
    image_datetime = Column(Integer)
    image_favoritecount = Column(Integer)
    image_votecount = Column(Integer)
    image_comment_count = Column(Integer)
    image_comments = Column(Text)
    image_account_url = Column(String)
    image_account_id = Column(String)
    image_upvotecount = Column(Integer)
    image_downvotecount = Column(Integer)
    image_popularitycount = Column(Integer)
    pagenumber = Column(String)
    multiple_images = Column(String)
    def __init__(self, keyword, image_id, image_link, image_title, image_description, image_datetime, image_favoritecount, image_votecount, 
                 image_comment_count, image_comments, image_account_url, image_account_id, image_upvotecount, image_downvotecount, image_popularitycount,
                 pagenumber, multiple_images):
        self.keyword = keyword
        self.image_id = image_id
        self.image_link = image_link
        self.image_title = image_title
        self.image_description = image_description
        self.image_datetime = image_datetime
        self.image_favoritecount = image_favoritecount
        self.image_votecount = image_votecount 
        self.image_comment_count = image_comment_count
        self.image_comments = image_comments
        self.image_account_url = image_account_url
        self.image_account_id = image_account_id
        self.image_upvotecount = image_upvotecount
        self.image_downvotecount = image_downvotecount
        self.image_popularitycount = image_popularitycount
        self.pagenumber = pagenumber
        self.multiple_images = multiple_images
    def __repr__(self):
       return "<Organization, Sender('%s', '%s')>" % (self.image_id, self.keyword)

engine = sqlalchemy.create_engine("sqlite:///C:/xxxxxx/image_keywords.sqlite", echo=False)  #OR FOUR SLASHES FOR ABSOLUTE FILE PATH
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
        image_name = str(row.image_id)+'.'+extension
        filepath = "C:/xxxx/image_downloaded"
        urllib.urlretrieve(image_url, filepath + '/'+ image_name)
        print "downloading", image_name
    else:
        print "this link may contain multiple images. Please check!"
    session.commit()

session.close()