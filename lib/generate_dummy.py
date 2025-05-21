import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from sqlalchemy.orm import sessionmaker
from model.model import Relationship, Role,MaritalStatus, StatusInquiry, engine

Session = sessionmaker(bind=engine,autoflush=False)
session = Session()

def generate_role():
    role_healthcare = Role(name = "healthcare")
    role_user = Role(name = "user")
    session.add_all([role_healthcare,role_user])
    session.commit()
    session.close()
    
def generate_marital_status():
    marital_option  = ["Menikah",
        "Cerai Hidup",
        "Cerai Mati",
        "Janda"
    ]
    
    data = []
    for i in marital_option:
        marital_status = MaritalStatus(name=i)
        data.append(marital_status)
    
    session.add_all(data)
    session.commit()
    session.close()

def generate_relationship():
    relationship_option = [
        "Ibu Kandung",
        "Ayah Kandung",
        "Suami",
        "Saudara Kandung",
        "Saudara Laki-laki",
        "Saudara Perempuan",
        "Kerabat",
        "Teman Dekat",
        "Tetangga",
        "Lainnya"
    ]
    
    data = []
    for i in relationship_option:
        relationship = Relationship(name=i)
        data.append(relationship)
    
    session.add_all(data)
    session.commit()
    session.close()

def generate_status_inquiry_anc():
    status_inquiry_option = ["Terlaksana","Terjadwalkan"]
    data = []
    for i in status_inquiry_option:
        status_inquiry = StatusInquiry(name=i)
        data.append(status_inquiry)
    
    session.add_all(data)
    session.commit()
    session.close()

generate_role()
generate_marital_status()
generate_relationship()
generate_status_inquiry_anc()

