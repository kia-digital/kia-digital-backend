from sqlalchemy.orm import Session
from model.model import MaritalStatus, Role, Relationship, StatusInquiry,TypeInquiry,User

class UIService:
    
    @classmethod
    def getAllUser(cls, db: Session):
        try:
            users = (
                db.query(User)
                .filter(User.role_id == 2, User.hpht != None)
                .all()
            )

            if not users:
                return {
                    "status": "success",
                    "message": "No users found with role_id 2 and hpht",
                    "data": []
                }

            result = {
                "status": "success",
                "message": "Success get user status",
                "data": [
                    {
                        "id": user.id,
                        "name": user.name,
                        "hpht": user.hpht.isoformat() if user.hpht else None
                    }
                    for user in users
                ]
            }
            return result

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": f"Internal server error: {str(e)}",
                    "data": None
                }
            )

        finally:
            db.close()
    
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
        
    