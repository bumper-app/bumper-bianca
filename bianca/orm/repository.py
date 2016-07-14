"""
file: repository.py
author: Ben Grawi <bjg1568@rit.edu>
date: October 2013
description: Holds the repository abstraction class and ORM
"""
import uuid
from db import *
from datetime import datetime


class Repository(Base):
    """
    Commit():
    description: The SQLAlchemy ORM for the repository table
    """
    __tablename__ = 'repositories'

    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)
    creation_date = Column(String)
    ingestion_date = Column(String)
    last_ingested_commit = Column(String)
    analysis_date = Column(String)
    status = Column(String)
    email = Column(String)
    listed = Column(Boolean)
    last_data_dump = Column(String)

    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid1())
        self.creation_date = str(datetime.now().replace(microsecond=0))
        self.url = kwargs.pop('url', None)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'creation_date': self.creation_date,
            'ingestion_date': self.ingestion_date,
            'last_ingested_commit': self.last_ingested_commit,
            'analysis_date': self.analysis_date,
            'status': self.status,
            'email': self.email,
            'listed': self.listed,
            'last_data_dump': self.last_data_dump
        }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def __repr__(self):
    #     return "<Repository: %s - %s>" % (self.name, self.id)
