from sqlalchemy.orm import Session
from model.model import MaritalStatus, Relationship, Role, User,MedicalRecord,EmergencyContact

class InquiryService:   
     
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
                        "date_of_birth": user.date_of_birth,
                        "address": user.address,
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


    