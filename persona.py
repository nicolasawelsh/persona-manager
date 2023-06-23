import random
import datetime
import json
import secrets
import names
import random_address

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
        self.gender = self.gender or random.choice(["male", "female"])
    
    def set_firstname(self):
        self.firstname = self.firstname or names.get_first_name(gender=self.gender)

    def set_lastname(self):
        self.lastname = self.lastname or names.get_last_name()
    
    def set_address(self):
        # Example: 
            # {
            #   'address1': '1600 Pennsylvania Avenue NW', 
            #   'address2': '', 
            #   'city': 'Washington', 
            #   'state': 'DC', 
            #   'postalCode': '20500', 
            #   'coordinates': {'lat': 38.8976800, 'lng': -77.0365300}
            # }
        if self.address is None:
            address_dict = random_address.real_random_address()
            self.address = json.dumps(address_dict)
    
    def set_phone(self):
        # Example:
            # 9876543210
        if self.phone is None:
            area_code = random.randint(200, 999)
            prefix = random.randint(200, 999)
            line_number = random.randint(1000, 9999)
            self.phone = f"{area_code}{prefix}{line_number}"
    
    def set_birthday(self):
        # Format:
            # Year-Month-Day
        # Example:
            # 1947-07-30
        if self.birthday is None:
            start_date = datetime.datetime.now() + datetime.timedelta(days=(-365*18))
            end_date = datetime.datetime.now() + datetime.timedelta(days=(-365*60))
            self.birthday = datetime.datetime.strftime((start_date + (end_date - start_date) * random.random()), "%Y-%m-%d")

    def set_username(self):
        # Format:
            # First initial + last name + random 5-digit number
        # Example:
            # aschwarzenegger12345
        if self.username is None:
            self.username = self.firstname[0].lower() + self.lastname.lower() + str(random.randint(10000,99999))

    def set_password(self):
        self.password = self.password or secrets.token_urlsafe(10)

    def set_email(self):
        # Format:
            # username + @proton.me
        # Example: 
            # aschwarzenegger12345@proton.me
        if self.email is None:
            self.email = self.username + "@proton.me"

    def print_person(self):
        print(', '.join("%s: %s" % item for item in vars(self).items()))
    
    def save(self):
        session = Session()
        session.add(self)
        session.commit()

    @classmethod
    def get_all(cls):
        session = Session()
        return session.query(cls).all()

    @classmethod
    def delete_all(cls):
        session = Session()
        session.query(cls).delete()
        session.commit()
    
    @classmethod
    def delete_by_name(cls, firstname, lastname):
        session = Session()
        session.query(cls).filter_by(firstname=firstname, lastname=lastname).delete()
        session.commit()


Base.metadata.create_all(engine)
