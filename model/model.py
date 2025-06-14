import uuid
from sqlalchemy import TIME, URL, DateTime, ForeignKey,FLOAT ,String,CHAR,DATE,INT, create_engine, func, BOOLEAN
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String,name="id",primary_key=True,default=generate_uuid)
    name = Column(String, name="name")
    email = Column(String,name="email",unique=True)
    phone_number = Column(String,name="phone_number",nullable=True)
    password = Column(String,name="password")
    birth_place = Column(String, name="birth_place",nullable=True)
    date_of_birth = Column(DATE, name="date_of_birth",nullable=True)
    address = Column(String, name="address",nullable=True)
    age = Column(INT, name="age",nullable=True)
    blood_group = Column(CHAR, name="blood_group",nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    role_id = Column(INT, ForeignKey("roles.id"),nullable=False)
    role = relationship("Role",back_populates="users")
    
    account_verification = relationship("AccountVerification",
                                        back_populates="users")
    
    hpht = Column(DATE,name="hpht")
    hpl = Column(DATE,name="hpl")
    
    marital_status_id = Column(INT,ForeignKey("marital_status.id"),nullable=True)
    marital_status = relationship("MaritalStatus",back_populates="users")
    emergency_contact = relationship("EmergencyContact", back_populates="user")
    medical_records = relationship("MedicalRecord", back_populates="user")
    inquiry_anc = relationship("InquiryAnc", back_populates="users")
    scheduleds = relationship("Scheduleds",back_populates="mom")
    weekly_monitorings = relationship("WeeklyMonitoring", back_populates="user")
    
    category_classification = relationship("CategoryClassification",back_populates="users")

class AccountVerification(Base):
    __tablename__ = "account_verifications"
    
    id = Column(INT,name="id",primary_key = True,autoincrement=True)
    users_id = Column(String,ForeignKey("users.id"),nullable=False)
    token = Column(String,name="token",nullable=False)
    verified = Column(BOOLEAN,name="is_verified",nullable=False)
    users = relationship("User",back_populates="account_verification")

class MaritalStatus(Base):
    __tablename__ = "marital_status"
    id = Column(INT,name="id",primary_key=True,autoincrement=True)
    name = Column(String,name="name",nullable=False)
    users = relationship("User", back_populates="marital_status")

class Role(Base):
    __tablename__ = "roles"     
       
    id = Column(INT,name="id",primary_key=True,autoincrement=True)
    name = Column(String, name="name")
    users = relationship("User",back_populates="role")

class EmergencyContact(Base):
    __tablename__ = "emergency_contact"
    
    id = Column(String, name="id", primary_key= True , default = generate_uuid)
    name= Column(String, name="name",nullable=False)
    user_id = Column(String,ForeignKey("users.id"),nullable=False)
    user = relationship("User",back_populates="emergency_contact")
    telp = Column(String,name="telp")
    address = Column(String, name="address")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())
    relationship_id = Column(INT,ForeignKey("relationship.id"),nullable=True)
    relationship = relationship("Relationship",back_populates="emergency_contact")

class Relationship(Base):
    __tablename__ = "relationship"
    id = Column(INT,name="id",primary_key=True,autoincrement=True)
    name = Column(String,name="name",nullable=False)
    emergency_contact = relationship("EmergencyContact",back_populates="relationship")

class MedicalRecord(Base):
    __tablename__  = "medical_records"
    
    id = Column(String,name="id",primary_key=True,default=generate_uuid)
    disease_history = Column(String,name="disease_history")
    allergies_history = Column(String,name="allergies_history")
    body_weight = Column(String,name="body_weight")
    body_height = Column(String,name="body_height")
    immunization_status = Column(String,name="immunization_status")
    pregnancy_history = Column(String,name="pregnancy_history")
    user_id = Column(String,ForeignKey("users.id"),nullable=False)
    user = relationship("User",back_populates="medical_records")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())
    
class InquiryAnc(Base):
    __tablename__ = "inquiry_anc"
    
    id = Column(String,name="id",primary_key=True,default=generate_uuid)
    scheduled_at = Column(DATE,name="scheduled_at",nullable=False)
    location = Column(String,name="location",nullable=False)
    body_weight = Column(FLOAT,name="body_weight",nullable=False)
    healthcare = Column(String,name="healthcare",nullable=False)
    height_uterine_fundus = Column(FLOAT,name="height_uterine_fundus",nullable=True)
    blood_sugar = Column(FLOAT,name="blood_sugar",nullable=False)
    heart_rate = Column(FLOAT,name="heart_rate",nullable=False)
    note = Column(String,name="note",nullable=True)
    sistolik = Column(INT,name="sistolik",nullable=False)
    diastolik = Column(INT,name="diastolik",nullable=False)
    users_id = Column(String,ForeignKey("users.id"),nullable=False)
    users = relationship("User",back_populates="inquiry_anc")
    body_temperature= Column(FLOAT,name="body_temperature",nullable=False)
    status_inquiry_id = Column(INT,ForeignKey("status_inquiry.id"),nullable=False)
    status_inquiry = relationship("StatusInquiry",back_populates="inquiry_anc")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
class StatusInquiry(Base):
    __tablename__ = "status_inquiry"
    
    id = Column(INT,name="id",primary_key=True,autoincrement=True)
    name = Column(String,name="name",nullable=False)
    inquiry_anc = relationship("InquiryAnc",back_populates="status_inquiry")
    

class Scheduleds(Base):
    __tablename__= "scheduleds"
    
    id = Column(INT,name="id",primary_key=True,autoincrement=True)
    name = Column(String,name="name",nullable=False)
    date = Column(DATE,name="date_scheduled",nullable=False)
    hours = Column(TIME,name="time_scheduled",nullable=False)
    location = Column(String,name="location",nullable=False)
    status = Column(BOOLEAN,name="status",nullable=False)
    status_scheduled_id = Column(INT,ForeignKey("status_scheduled.id"),nullable=False)
    status_scheduled = relationship("StatusScheduled",back_populates="scheduleds")
    
    moms_id = Column(String,ForeignKey("users.id"),nullable=False)
    mom = relationship("User",back_populates="scheduleds")
    

class StatusScheduled(Base):
    __tablename__="status_scheduled"
    id = Column(INT,name="id",primary_key=True,autoincrement=True)
    name= Column(String,name="name",nullable=False)
    scheduleds = relationship("Scheduleds",back_populates="status_scheduled")
    

class WeeklyMonitoring(Base):
    __tablename__ = "weekly_monitorings"

    id = Column(String, primary_key=True, default=generate_uuid)
    weekly_pregnantcy = Column(INT, nullable=False)
    fever = Column(BOOLEAN, nullable=False)
    headache = Column(BOOLEAN, nullable=False)
    insomnia_or_anxiety = Column(BOOLEAN, nullable=False)
    tb_risk = Column(BOOLEAN, nullable=False)
    fetal_movement = Column(BOOLEAN, nullable=False)
    abdominal_pain = Column(BOOLEAN, nullable=False)
    discharge = Column(BOOLEAN, nullable=False)
    urination_issues = Column(BOOLEAN, nullable=False)
    diarrhea = Column(BOOLEAN, nullable=False)

    users_id = Column("users_id", String, ForeignKey("users.id"), nullable=False)
    type_inquiry = Column("type_inquiry", INT, ForeignKey("type_inquiry.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="weekly_monitorings")
    type_inquiry_rel = relationship("TypeInquiry", back_populates="weekly_monitoring")


class CategoryClassification(Base):
    __tablename__ = "category_classification"
    id = Column(INT,name="id",autoincrement=True,primary_key=True)
    tag = Column(String,name="tag",nullable=False)
    users_id = Column(String,ForeignKey("users.id"),nullable=False)
    users = relationship("User",back_populates="category_classification")

class TypeInquiry(Base):
    __tablename__ = "type_inquiry"
    
    id = Column(INT,name="id",autoincrement=True,primary_key=True)
    name = Column(String,name="name",nullable=False)
    weekly_monitoring = relationship("WeeklyMonitoring", back_populates="type_inquiry_rel")
 
class Article(Base):
    __tablename__ = "article"
    
    id = Column(INT,name="id",autoincrement=True,primary_key=True)    
    judul = Column(String,name="judul",nullable= False)    
    kategori =  Column(String,name="kategori",nullable= False)    
    deskripsi =  Column(String,name="deskripsi",nullable= False)  
    content =  Column(String,name="content",nullable= False)   
    tag =  Column(String,name="tag",nullable= False) 

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="anggara123",
    host="localhost",
    database="kia",
    port=5432
)

engine = create_engine(url=url)
Base.metadata.create_all(engine)