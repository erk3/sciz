#!/usr/bin/env python
#-*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# CLASS DEFINITION
class AssocUsersGroups(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'assoc_users_groups'

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"), primary_key=True)
    # Acess level numeric representation (1,2,4 / guest,user,admin)
    role = Column(Integer)

    user = relationship("USER", back_populates="groups")
    group = relationship("GROUP", back_populates="users")

