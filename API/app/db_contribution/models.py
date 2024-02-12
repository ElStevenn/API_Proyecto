#!/usr/bin/env python3

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BINARY, Float, TEXT, DateTime, DATE, Date, DECIMAL, Table, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid, requests
from datetime import datetime, date
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
    bookeds_trips = relationship("Booked_Trips", back_populates='registered_user')
    billings = relationship("Billing", back_populates='registered_user')
    travels_historys = relationship("Travel_history", back_populates='registered_user')

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
    favorite_places = Column(TEXT)  
    favorite_types_of_trips = Column(TEXT)  
    user_labels = Column(TEXT) 
    user_description_ideal_trip = Column(TEXT)
    dates_available_to_travel = Column(TEXT) 

    def __repr__(self):
        return f"<Travel_Preferences(favorite_places='{self.favorite_places}')>"


# HELP TICKETS TABLES
    
class Ticket_Suport(Base):
    __tablename__ = "ticket_suport"    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('registered_user.id'))
    subject = Column(String(255))
    description = Column(TEXT)
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
    message = Column(TEXT)
    created = Column(DateTime, default=datetime.now)

    # Relationships
    help_answer = relationship('Ticket_Suport', back_populates='tickets_help')

    def __repr__(self):
        return f"<Ticket_Help_Answers(ticket_id={self.ticket_id}, message={self.message}, created={self.created})>"


# BOOKING TABLES & BILLING
class Booked_Trips(Base):
    __tablename__ = "booked_trips"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('registered_user.id'))
    reservation_time = Column(DATE, nullable=False)
    reservation_status = Column(String(15), nullable=False)

    # Relationships
    user_rela = relationship('Registered_User', back_populates='bookeds_trips')

    # External Relationships
    billings = relationship('Billing', back_populates='booked_trips')

    def __repr__(self):
        return f"<Booked_Trips(user_id='{self.user_id}', reservation_time='{self.reservation_time}', reservation_status='{self.reservation_status}')>"


class Billing(Base):
    __tablename__ = "billing"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUID(as_uuid=True), ForeignKey('registered_user.id'))
    id_booking = Column(UUID(as_uuid=True), ForeignKey('booked_trips.id'))
    total_cost = Column(DECIMAL)
    payment_method = Column(String(20), nullable=False)
    payment_status = Column(String(20), default='pending') # pending, completed, cancelled, refused
    notes = Column(TEXT)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user_rela = relationship('Registered_User', back_populates='billings')
    booked_rela = relationship('Booked_Trips', back_populates='billings')

    def __repr__(self):
        return f"<Billing(id_user='{self.id_user}', id_booking='{self.id_booking}', total_cost='{self.total_cost}', payment_method='{self.payment_method}', payment_status='{self.payment_status}', notes='{self.notes}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"


# FLIGHTS AND ACCOMMODATION
flights_trips = Table(
    'flights_boocked_trips',
    Base.metadata,
    Column('travel_id', UUID(as_uuid=True), ForeignKey('booked_trips.id'), primary_key=True),
    Column('flight_id', UUID(as_uuid=True), ForeignKey('flights.id'), primary_key=True)
)

accommodation_trips = Table(
    'accommodation_boocked_trips',
    Base.metadata(),
    Column('travel_id', UUID(as_uuid=True), ForeignKey('booked_trips.id'), primary_key=True),
    Column('accommodation_id', UUID(as_uuid=True), ForeignKey('accommodations.id'), primary_key=True)
)

class Flights(Base):
    __tablename__ = "flights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    departure = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    duration = Column(DECIMAL)
    departure_date = Column(DateTime)
    arrival_time = Column(DateTime)
    flight_price = Column(DECIMAL)

    # Relationship to BookedTrips
    booked_trips = relationship(
        "BookedTrips",
        secondary=flights_trips,
        back_populates="flights"
    )

    def __repr__(self):
        return f"<Flights(departure='{self.departure}', destination='{self.destination}', duration='{self.duration}', departure_date='{self.departure_date}', arrival_time='{self.arrival_time}', flight_price='{self.flight_price}')>"
    
class Accommodations(Base):
    __tablename__ = 'accommodations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    direction = Column(String) 
    type_accommodation = Column(String)
    contact_information = Column(String)
    price_per_night = Column(DECIMAL)
    mod_cons = Column(String)  
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    rating = Column(DECIMAL)
    availability_status = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Relationship to BookedTrips
    booked_trips = relationship(
        "BookedTrips",
        secondary=accommodation_trips,
        back_populates="accommodations"
    )

    def __repr__(self):
        return f"<Accommodations(name='{self.name}', direction='{self.direction}', type_accommodation='{self.type_accommodation}', contact_information='{self.contact_information}', price_per_night='{self.price_per_night}', mod_cons='{self.mod_cons}', check_in_time='{self.check_in_time}', check_out_time='{self.check_out_time}', rating='{self.rating}', availability_status='{self.availability_status}')>"


# TRAVEL HISTORY
class Travel_history(Base):
    __tablename__ = "travel_history"

    
    # Relationships
    user_rela = relationship('Registered_User', back_populates='travel_histories')


    
