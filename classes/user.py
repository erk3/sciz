#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime, bcrypt
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a SCIZ User
class USER(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'users'
    id = Column(Integer, ForeignKey('trolls.id'), primary_key=True)              # Identifiant unique du joueur
    pseudo = Column(String(50))                         # Pseudonyme
    pwd = Column(String(100))                           # Password
    mh_apikey = Column(String(50))                      # Mountyhall Key
    pushover_apikey = Column(String(50))                # Pushover Key
    role = Column(Integer())                            # Role
    
    troll = relationship("TROLL", back_populates="user")

    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override

    # Create a user from a JSON Object
    def update_from_json(self, json, update_pwd):
        self.id = json['id'] if json['id'] else self.id
        self.pseudo = json['pseudo'] if json['pseudo'] else self.pseudo
        # Rounds fixed to 10 for PHP front-end compatibility
        self.pwd = bcrypt.hashpw(json['pwd'].encode(sg.DEFAULT_CHARSET), bcrypt.gensalt(10)) if json['pwd'] and update_pwd else self.pwd
        self.mh_apikey = json['mh_apikey'] if json['mh_apikey'] else self.mh_apikey
        self.pushover_apikey = json['pushover_apikey'] if json['pushover_apikey'] else self.pushover_apikey
        self.role = json['role'] if json['role'] else self.role

    # Update user from another USER (but password)
    def update_from_new(self, user_old):
        sg.copy_properties(user_old, self, ['pseudo', 'mh_apikey', 'pushover_apikey', 'role'])

