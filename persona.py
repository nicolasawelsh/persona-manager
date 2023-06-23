import random
import datetime
import json
import secrets
import names
import random_address

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create the engine and session
engine = create_engine('sqlite:///personas.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Person(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)
    gender = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    phone = Column(String)
    birthday = Column(String)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_data()

    def generate_data(self):
        """Generate random data for each attribute if not already set"""
        self.set_gender()
        self.set_firstname()
        self.set_lastname()
        self.set_address()
        self.set_phone()
        self.set_birthday()
        self.set_username()
        self.set_password()
        self.set_email()

    def set_gender(self):
        """Set gender attribute randomly if not already set"""
        self.gender = self.gender or random.choice(["male", "female"])
    
    def set_firstname(self):
        """Set first name attribute randomly based on gender if not already set"""
        self.firstname = self.firstname or names.get_first_name(gender=self.gender)

    def set_lastname(self):
        """Set last name attribute randomly if not already set"""
        self.lastname = self.lastname or names.get_last_name()
    
    def set_address(self):
        """Set address attribute randomly using random_address library if not already set"""
        if self.address is None:
            address_dict = random_address.real_random_address()
            self.address = json.dumps(address_dict)
    
    def set_phone(self):
        """Set phone attribute randomly if not already set"""
        if self.phone is None:
            area_code = random.randint(200, 999)
            prefix = random.randint(200, 999)
            line_number = random.randint(1000, 9999)
            self.phone = f"{area_code}{prefix}{line_number}"
    
    def set_birthday(self):
        """Set birthday attribute randomly if not already set"""
        if self.birthday is None:
            start_date = datetime.datetime.now() + datetime.timedelta(days=(-365*18))
            end_date = datetime.datetime.now() + datetime.timedelta(days=(-365*60))
            self.birthday = datetime.datetime.strftime((start_date + (end_date - start_date) * random.random()), "%Y-%m-%d")

    def set_username(self):
        """Set username attribute based on first initial, last name, and random 5-digit number if not already set"""
        if self.username is None:
            self.username = self.firstname[0].lower() + self.lastname.lower() + str(random.randint(10000,99999))

    def set_password(self):
        """Set password attribute if not already set (16 characters)"""
        self.password = self.password or secrets.token_urlsafe(12)

    def set_email(self):
        """Set email attribute based on username and fixed domain if not already set"""
        if self.email is None:
            self.email = self.username + "@proton.me"

    def print_person(self):
        """Print the person's information in a readable format"""
        print()
        print("Person Information:")
        print(f"ID: {self.id}")
        print(f"Gender: {self.gender}")
        print(f"First Name: {self.firstname}")
        print(f"Last Name: {self.lastname}")
        print(f"Address: {self.address}")
        print(f"Phone: {self.phone}")
        print(f"Birthday: {self.birthday}")
        print(f"Username: {self.username}")
        print(f"Password: {self.password}")
        print(f"Email: {self.email}")
    
    def save(self):
        """Save the person object to the database"""
        session = Session()
        session.add(self)
        session.commit()

    @classmethod
    def get_all(cls):
        """Retrieve all person objects from the database"""
        session = Session()
        return session.query(cls).all()

    @classmethod
    def delete_all(cls):
        """Delete all person objects from the database"""
        session = Session()
        session.query(cls).delete()
        session.commit()
    
    @classmethod
    def delete_by_id(cls, id):
        """Delete a person object from the database by ID"""
        session = Session()
        session.query(cls).filter_by(id=id).delete()
        session.commit()


# Create the table if it doesn't exist
Base.metadata.create_all(engine)
