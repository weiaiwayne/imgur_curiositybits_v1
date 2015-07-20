# -*- coding: utf-8 -*-
"""
Imgur fetcher for getting links of images from keyword search
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
import time
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
from imgurpython import ImgurClient # makesure this package is installed

ids = ['obama',
       'hillary',] # enter your search terms
       

# go to https://imgur.com/signin?redirect=http://api.imgur.com/oauth2/addclient to register an app
client_id = ''
client_secret = ''

client = ImgurClient(client_id, client_secret)

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

def search_image(kid, page):
    try:
        d = client.gallery_search(q = kid, advanced=None, sort='time', window='all', page=page)
    except Exception, e:
        #print "Error reading id %s, exception: %s" % (kid, e)
        return None
     
    print "The number of images available for dowbload: ", len(d)
    return d
    

def write_data(self, d, kid, page):         
    for item in d:
        import time
        keyword = kid
        image_id = item.id
        image_link = item.link
        if image_link.endswith('jpg') or image_link.endswith('gif') or image_link.endswith('png') or image_link.endswith('bmp'):
            multiple_images = "NO"
        else:
            multiple_images = "this link contains multiple images"
        image_title = item.title
        image_description = item.description
        time_s_temp1 = item.datetime
        image_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_s_temp1))
        image_favoritecount = item.favorite
        image_votecount = item.vote
        image_comment_count = item.comment_count
        image_comments = item.comment_preview
        image_account_url = item.account_url
        image_account_id = item.account_id
        image_upvotecount = item.ups
        image_downvotecount = item.downs 
        image_popularitycount = item.score
        pagenumber = page
        updates = self.session.query(Messages).filter_by(image_id = image_id, keyword = keyword).all() 
        if not updates:
            print "inserting new image URLs:", image_link, pagenumber                     
            upd = Messages(keyword, image_id,image_link, image_title, image_description, image_datetime, image_favoritecount, image_votecount,
                           image_comment_count, image_comments, image_account_url, image_account_id, image_upvotecount, image_downvotecount, 
                           image_popularitycount, pagenumber, multiple_images)
            self.session.add(upd)
        else:
            if len(updates) > 1:
                print "Duplicate Warning"
                    
            else:
                print "Duplicate images, Not inserting"
        self.session.commit()
    
class Scrape:
    def __init__(self):    
        engine = sqlalchemy.create_engine("sqlite:///image_keywords3.sqlite", echo=False)  
        Session = sessionmaker(bind=engine)
        self.session = Session()  
        Base.metadata.create_all(engine)

    def main(self):
        for n,kid in enumerate(ids):
            print "search keyword:", kid
            sys.stdout.flush()
            for page in range(5): 
                kid = kid
                print "------XXXXXX------ STARTING PAGE", page
                page = page
                d = search_image(kid, page)
                write_data(self, d, kid, page)
                if not d:
                    continue 
                if len(d)==0:
                    continue
        self.session.close()


if __name__ == "__main__":
    s = Scrape()
    s.main()
