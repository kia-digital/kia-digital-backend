from sqlalchemy.orm import Session
from model.model import MaritalStatus, Relationship, User,MedicalRecord,EmergencyContact

class InquiryService:   
     
    @classmethod
    def get_information_mom(cls, user_id: str, db: Session):
        user = db.query(User).filter_by(id=user_id).first()
        
        marital_status = (
            db.query(MaritalStatus)
            .filter(MaritalStatus.id == user.marital_status_id)
            .first()
        )
        
        
        if not user:
            return {"error": "User not found"}

        emergency_data = (
            db.query(EmergencyContact, Relationship.name.label("relationship_name"))
            .join(Relationship, EmergencyContact.relationship_id == Relationship.id)
            .filter(EmergencyContact.user_id == user_id)
            .first()
        )

        medical_record_data = (
            db.query(MedicalRecord)
            .filter(MedicalRecord.user_id == user_id)
            .first()
        )
        
        if emergency_data:
            contact, relationship_name = emergency_data
            emergency_contact = {
                "name": contact.name,
                "telp": contact.telp,
                "relationship": relationship_name,
                "address": contact.address,
            }
            
        else:
            emergency_contact = {
                "name": "-",
                "telp": "-",
                "relationship": "-",
                "address": "-",
            }

        if medical_record_data:
            medical_record = {
                "disease_history": medical_record_data.disease_history,
                "allergies_history": medical_record_data.allergies_history,
                "body_height": medical_record_data.body_height,
                "body_weight": medical_record_data.body_weight,
                "immunization_status": medical_record_data.immunization_status,
                "pregnancy_history": medical_record_data.pregnancy_history    
            }
            
        else:
            medical_record = {
                "disease_history": "-",
                "allergies_history": "-",
                "body_height": "-",
                "body_weight": "-",
                "immunization_status": "-",
                "pregnancy_history": "-"
            }
            
        personal_info = {
            "name": user.name,
            "telp": user.phone_number,
            "birth_place": user.birth_place,
            "date_of_birth": user.date_of_birth,
            "address": user.address,
            "marital_status": user.marital_status,
            "age": user.age,
            "blood_group": user.blood_group,
        }

        return {
            "personal_info": personal_info,
            "emergency_contact": emergency_contact,
            "medical_record": medical_record
        }
    