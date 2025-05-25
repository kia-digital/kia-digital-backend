from sqlalchemy.orm import Session
from model.model import MaritalStatus, Role, Relationship, StatusInquiry

class UIService:
    
    @classmethod
    def get_mmarital_status(cls,db: Session):
        marital_status = db.query(MaritalStatus).all()
        db.close()
        
        response = []
        
        if marital_status:
            for marital in marital_status:
                marital_data = { "id": marital.id, "name": marital.name}
                response.append(marital_data)
            
            return {
                "status" : "success",
                "message": "success get marital status",
                "data": response
            }
        
        else : 
            return None
    
    @classmethod
    def get_roles(cls,db: Session):
        roles = db.query(Role).all()
        db.close()
        
        response = []
        
        if roles:
            for role in roles:
                role_data = { "id": role.id, "name": role.name}
                response.append(role_data)
            
            return {
                "status" : "success",
                "message": "success get marital status",
                "data": response
            }
        
        else : 
            return None
    
    @classmethod    
    def get_relationship( cls, db : Session ):
        relationships = db.query(Relationship).all()
        db.close()
        response = []
        
        if relationships:
            for relationship in relationships:
                relationship_data = { "id": relationship.id, "name": relationship.name}
                response.append(relationship_data)
            
            return {
                "status" : "success",
                "message": "success get marital status",
                "data": response
            }
        
        else : 
            return None
    
    @classmethod
    def get_status_inquiry( cls, db: Session):
        status_inquirys = db.query(StatusInquiry).all()
        db.close()
        response = []
        
        if status_inquirys:
            for status_inquiry in status_inquirys:
                status_inquiry_data = { "id": status_inquiry.id, "name": status_inquiry.name}
                response.append(status_inquiry_data)
            
            return {
                "status" : "success",
                "message": "success get marital status",
                "data": response
            }
        
        else : 
            return None