#!/usr/bin/env python
#-*- coding: utf-8 -*-

###
### /!\ Hooks should only be handled by the webapp /!\
###

# Imports
import requests, ConfigParser
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint, desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship
from classes.event import EVENT
import modules.globals as sg

# Class of a SCIZ hook
class HOOK(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'hooks'
    __tableargs__ = (UniqueConstraint('name', 'group_id'), )
    # ID unique
    id = Column(Integer, primary_key=True)
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # Nom du hook
    name = Column(String(50))
    # JWT token sans expiration (ou simple secret dans le cas d'un reverse hook)
    jwt = Column(String(250))
    # URL de post pour un reverse hook
    url = Column(String(250))
    # Révoqué ?
    revoked = Column(Boolean())
    # ID du dernier évènement
    last_event_id = Column(Integer())

    # Associations One-To-Many
    group = relationship("GROUP", back_populates="hooks")

    # Constructor is handled by SqlAlchemy, do not override
    
    # Reverse hook triggering
    def trigger(self):
        if not self.revoked and self.url != None:
            try:
                # Find the events
                events = sg.db.session.query(EVENT).filter(EVENT.id > self.last_event_id, EVENT.hidden == False, EVENT.group_id == self.group_id).order_by(asc(EVENT.time)).all()
                res = []
                max_id = 0
                for event in events:
                    max_id = max(event.id, max_id)
                    res.append({'id': event.id, 'notif': event.notif.encode(sg.DEFAULT_CHARSET)})
                # Send the data
                if len(res) > 0 :
                    try:
                        headers = {'Authorization': self.jwt}
                        r = requests.post(self.url, headers = headers, json = res, timeout = 1)
                        # Update the hook
                        self.last_event_id = max_id
                        sg.db.session.add(self)
                        sg.db.session.commit()
                    except requests.RequestException as e:
                        sg.logger.warning('Unable to send events for reverse hook %s (%s) and url %s : %s' % (self.name, self.id, self.url, str(e), ))
            except NoResultFound:
                sg.logger.warning('No event found corresponding to the reverse hook %s (%s)' % (self.name, self.id, ))


