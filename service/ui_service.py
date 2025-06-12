from sqlalchemy.orm import Session
from model.model import MaritalStatus, Role, Relationship, StatusInquiry,TypeInquiry

class UIService:
    
    
    @classmethod
    def getTypeInquiry(cls,db:Session):
        type_inquirys = db.query(TypeInquiry).all()
        if type_inquirys:
            
            result= {
                "status" : "success",
                "message": "success get marital status",
                "data": [
                    {
                        "id": type_inquiry.id,
                        "name": type_inquiry.name
                    }
                    for type_inquiry in type_inquirys
                ]
            }
            
            db.close()
            return result
        
        else : 
            db.close()
            return None
    
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
    
        
        if status_inquirys:
            
            result= {
                "status" : "success",
                "message": "success get marital status",
                "data": [
                    {
                        "id": status.id,
                        "name": status.name
                    }
                    for status in status_inquirys
                ]
            }
            
            db.close()
            return result
        
        else : 
            db.close()
            return None
        
    