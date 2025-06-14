from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from model.model import MedicalRecord

class MedicalRecordService:
    
    @classmethod
    def updateMedical(cls,data:dict,user_id:str,db:Session):
        try:
            medical_record = (db.query(MedicalRecord).filter(MedicalRecord.user_id == user_id).first())
            
            checkupResult = data["checkup_result"]
            
            if not medical_record:
                
                print("halo")
            
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "status": "error",
                        "message": f"internal Server Error",
                        "data": None
                    }
                )