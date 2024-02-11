#!/usr/bin/env python3

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BINARY, Float, Text, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid, requests
from datetime import datetime
from sqlalchemy.orm import configure_mappers
configure_mappers()

from .database import Base

# MAIN USER SESSION TABLES

class Registered_User(Base):
    __tablename__ = "registered_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)

    # Relationships ONE-TO-ONE
    user_profile = relationship("User_Perfil", backref=backref("registered_user", uselist=False))
    contact_info = relationship("Contact_Information", backref=backref("registered_user", uselist=False))
    travel_prefs = relationship("Travel_Preferences", backref=backref("registered_user", uselist=False))

    # Relationships ONE-TO-MANY
    tickets_suport = relationship("Ticket_Suport",  back_populates='registered_user')

    def __repr__(self):
        return f"<Registered_User(username='{self.username}', mail='{self.mail}')>"

class User_Perfil(Base):
    __tablename__ = "user_perfil"

    user_id = Column(UUID(as_uuid=True), ForeignKey('registered_user.id'), primary_key=True)
    name = Column(String(50), nullable=False)
    surname1 = Column(String(50), nullable=False)
    surname2 = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<User_Perfil(name='{self.name}', surname1='{self.surname1}', surname2='{self.surname2}')>"

class Contact_Information(Base):
    __tablename__ = "contact_information"

    user_id = Column(UUID(as_uuid=True), ForeignKey('registered_user.id'), primary_key=True)
    zip_code = Column(String(20))
    direccion = Column(String(100))
    gender = Column(String(50))
    age = Column(Integer)
    country_of_residence = Column(String(50))
    city_of_residence = Column(String(50))
    phone_number = Column(String(20))

    def __repr__(self):
        return f"<Contact_Information(zip_code='{self.zip_code}', city_of_residence='{self.city_of_residence}')>"

class Travel_Preferences(Base):
    __tablename__ = "travel_preferences"

    user_id = Column(UUID(as_uuid=True), ForeignKey('registered_user.id'), primary_key=True)
    favorite_places = Column(Text)  
    favorite_types_of_trips = Column(Text)  
    user_labels = Column(Text) 
    user_description_ideal_trip = Column(Text)
    dates_available_to_travel = Column(Text) 

    def __repr__(self):
        return f"<Travel_Preferences(favorite_places='{self.favorite_places}')>"


# HELP TICKETS TABLES
    
class Ticket_Suport(Base):
    __tablename__ = "ticket_suport"    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('registered_user.id'))
    subject = Column(String(255))
    description = Column(Text)
    status = Column(String(15))
    priority = Column(String(15))
    created = Column(DateTime, default=datetime.now)
    last_time_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships 
    ticket = relationship('Registered_User', back_populates='tickets_suport')
    tickets_help = relationship('Ticket_Help_Answers', back_populates='ticket_suport')

    def __repr__(self):
        return f"<Ticket_Suport(subject='{self.subject}', description='{self.description}', status='{self.status}', priority='{self.priority}', created='{self.created}', last_time_updated='{self.last_time_updated}')>"
    

class Ticket_Help_Answers(Base):
    __tablename__ = "ticket_help_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey('ticket_suport.id'))
    message = Column(Text)
    created = Column(DateTime, default=datetime.now)

    # Relationships
    help_answer = relationship('Ticket_Suport', back_populates='tickets_help')

    def __repr__(self):
        return f"<Ticket_Help_Answers(ticket_id={self.ticket_id}, message={self.message}, created={self.created})>"


# BOOKING TABLES
    
    
