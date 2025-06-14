from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from model.model import MaritalStatus, Relationship, Role, User,MedicalRecord,EmergencyContact,CategoryClassification,InquiryAnc
from datetime import datetime

class InquiryService:   
    @classmethod
    def getInformationHpht(cls,id:str,db: Session):
        try:
            user = (db.query(User).filter(User.id == id).first())
            
            hpht = datetime.strptime(user.hpht.isoformat(),"%Y-%m-%d")
            
            today = datetime.today()
            
            selisih_hari = (today - hpht).days
            minggu = selisih_hari // 7
            hari = selisih_hari % 7
            
            result = {
                "status": "success",
                "message": "success get user monitoring",
                "data": {
                    "name": user.name,
                    "hpl": user.hpl.isoformat() if user.hpl else None,
                    "hpht": user.hpht.isoformat() if user.hpht else None,
                    "usia_kehamilan": f"{minggu} minggu {hari} hari"
                }
            }
            
            db.close()
            return result
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": str(e),
                    "data": None
                }
            )            
     
    @classmethod
    def getUserByID(cls, user_id: str, db: Session):
        try:
            user = (
                db
                .query(User)
                .outerjoin(CategoryClassification, CategoryClassification.users_id == User.id)
                .filter(User.id == user_id)
                .first()
            )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "status": "error",
                        "message": f"User with ID {user_id} not found",
                        "data": None
                    }
                )

            result = {
                "status": "success",
                "message": "success get user monitoring",
                "data": {
                    "name": user.name,
                    "age": user.age,
                    "hpht": user.hpht.isoformat() if user.hpht else None,
                    "telepon": user.phone_number,
                    "kondisi": user.category_classification[0].tag if user.category_classification else None,
                    "address": user.address
                }
            }

            return result

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": str(e),
                    "data": None
                }
            )
        finally:
            db.close()

     
    @classmethod
    def get_information_mom(cls, user_id: str, db: Session):
        try:
            user = (
                db.query(User)
                .outerjoin(Role, User.role_id == Role.id)
                .outerjoin(EmergencyContact, User.id == EmergencyContact.user_id)
                .outerjoin(MedicalRecord, User.id == MedicalRecord.user_id)
                .outerjoin(Relationship, EmergencyContact.relationship_id == Relationship.id)
                .outerjoin(MaritalStatus, User.marital_status_id == MaritalStatus.id)
                .filter(User.id == user_id)
                .first()
            )

            emergency = user.emergency_contact[0] if user.emergency_contact else None
            medical = user.medical_records[0] if user.medical_records else None

            result = {
                "status": "success",
                "message": "get information user success",
                "data": {
                    "personal_info": {
                        "name": user.name,
                        "telp": user.phone_number,
                        "birth_place": user.birth_place,
                        "date_of_birth": user.date_of_birth.isoformat()if user.date_of_birth else None,
                        "address": user.address,
                        "hpht": user.hpht.isoformat() if user.hpht else None,
                        "hpl": user.hpl.isoformat() if user.hpl else None,
                        "marital_status": user.marital_status.name,
                        "age": user.age,
                        "blood_group": user.blood_group,
                        "emergency_contact": {
                            "name": emergency.name if emergency else None,
                            "telp": emergency.telp if emergency else None,
                            "relationship": emergency.relationship.name if emergency and emergency.relationship else None,
                            "address": emergency.address if emergency else None,
                        }
                    },
                    "medical_record": {
                        "disease_history": medical.disease_history if medical else None,
                        "allergies_history": medical.allergies_history if medical else None,
                        "body_height": medical.body_height if medical else None,
                        "body_weight": medical.body_weight if medical else None,
                        "immunization_status": medical.immunization_status if medical else None,
                        "pregnancy_history": medical.pregnancy_history if medical else None
                    },
                }
            }
            return result

        except Exception as e:
            db.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            db.close()


    