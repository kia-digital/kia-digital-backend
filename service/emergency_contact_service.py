from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from model.model import EmergencyContact

class EmergencyContactService:

    @classmethod
    def updateData(cls, id: str, data: dict, db: Session):
        try:
            # Cari data emergency contact berdasarkan user_id
            emergencyContact = (
                db.query(EmergencyContact)
                .filter(EmergencyContact.user_id == id)
                .first()
            )

            # Jika belum ada, buat baru
            if not emergencyContact:
                emergencyContactData = EmergencyContact(
                    name=data["name"],
                    telp=data["telp"],
                    address=data["address"],
                    user_id=id,
                    relationship_id=data["relationship_id"]
                )
                db.add(emergencyContactData)
                db.commit()
                db.refresh(emergencyContactData)

                return {
                    "status": "success",
                    "message": "Emergency contact created successfully",
                    "data": {
                        "id": emergencyContactData.id,
                        "name": emergencyContactData.name,
                        "telp": emergencyContactData.telp,
                        "address": emergencyContactData.address,
                        "relationship_id": emergencyContactData.relationship_id,
                    }
                }

            # Jika sudah ada, lakukan update
            else:
                if "name" in data:
                    emergencyContact.name = data["name"]
                if "telp" in data:
                    emergencyContact.telp = data["telp"]
                if "address" in data:
                    emergencyContact.address = data["address"]
                if "relationship_id" in data:
                    emergencyContact.relationship_id = data["relationship_id"]

                db.commit()
                db.refresh(emergencyContact)

                return {
                    "status": "success",
                    "message": "Emergency contact updated successfully",
                    "data": {
                        "id": emergencyContact.id,
                        "name": emergencyContact.name,
                        "telp": emergencyContact.telp,
                        "address": emergencyContact.address,
                        "relationship_id": emergencyContact.relationship_id,
                    }
                }

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
