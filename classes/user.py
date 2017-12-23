#!/usr/bin/env python
#-*- coding: utf-8 -*-

# IMPORTS
import bcrypt
from sqlalchemy import event, Column, Integer, String, DateTime, ForeignKey, inspect
from sqlalchemy.orm import relationship
import modules.globals as sg

# CLASS DEFINITION
class USER(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'users'
    # Unique identifier of the player
    id = Column(Integer, primary_key=True)
    # Pseudonyme
    pseudo = Column(String(50))
    # Password
    pwd = Column(String(100))
    # Mountyhall API Key
    mh_apikey = Column(String(50))
    # Default group
    default_group_id = Column(Integer, ForeignKey('groups.id'))
    # Web session duration
    session_duration = Column(Integer(), default=30)
    # Minutes between a refresh of dynamic MH scripts
    dyn_sp_refresh = Column(Integer(), default=240)
    # Last refresh of dynamic MH scripts
    last_dyn_sp_call = Column(DateTime())
    # Minutes between a refresh of static MH scripts
    static_sp_refresh = Column(Integer(), default=240)
    # Last refresh of static MH scripts
    last_static_sp_call = Column(DateTime())
    
    # Associations Many-To-Many
    groups = relationship("AssocUsersGroups", back_populates="user")
    # Associations Many-To-One
    trolls = relationship("TROLL", back_populates="user")
    # Association One-To-One
    default_group = relationship("GROUP")

    # Constructor is handled by SqlAlchemy, do not override

    # Build an instance from a JSON object
    def build_from_json(self, json):
        for key in json:
            if json[key] and (hasattr(self, key) or (key == 'role')):
                setattr(self, key, json[key]) 

@event.listens_for(USER, 'before_insert')
@event.listens_for(USER, 'before_update')
def hashPassword(mapper, conneciton, target):
    state = inspect(target)
    hist = state.get_history("pwd", True)
    if hist.has_changes() and target.pwd:
        # Rounds fixed to 10 for PHP front-end compatibility
        target.pwd = bcrypt.hashpw(target.pwd.encode(sg.DEFAULT_CHARSET), bcrypt.gensalt(10))
