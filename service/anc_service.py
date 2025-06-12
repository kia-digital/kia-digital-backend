import datetime
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from model.model import InquiryAnc, StatusInquiry, User
from service.ml_service import MLService


class AncService:
    
    @classmethod
    def getAll(cls,user_id:str,db:Session):
        
        try:
            ancs =(
                db.query(InquiryAnc)
                .join(StatusInquiry,InquiryAnc.status_inquiry_id==StatusInquiry.id)
                .join(User,InquiryAnc.users_id==User.id)
                .filter(InquiryAnc.users_id == user_id)
                .all()
            ) 
            
            result = {
                    "status": "success",
                    "message": "success add anc",
                    "data": [
                        {
                            "id": anc.id,
                            "scheduled": anc.scheduled_at.isoformat() if anc.scheduled_at else None,
                            "location": anc.location,
                            "checkup_result":{
                                "body_weight": anc.body_weight,
                                "heart_rate" : anc.heart_rate,
                                "blood_pressure" : anc.type_blood_pressure.name,
                                "status" : anc.status_inquiry.name,
                                "uterine_fundus_height": anc.height_uterine_fundus,
                                "blood_sugar": anc.blood_sugar,
                                "body_temperature": anc.body_temperature
                            }
                        }
                        for anc in ancs
                    ]
                }
            
            db.close()
            return result
        except:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "status": "error",
                        "message": f"internal Server Error",
                        "data": None
                    }
                )
    
    @classmethod
    def addAncReport(cls,data: dict,user_id: str,db: Session):
        blood_pressure = data["checkup_result"]["blood_pressure"]
        split_blood_pressure = blood_pressure.split("/")
        if data:
            try:
                inquiry_anc = InquiryAnc(
                    scheduled_at=data["scheduled"],
                    location=data["location"],
                    body_weight=data["checkup_result"]["body_weight"],
                    healthcare=data["medical_officer"],
                    height_uterine_fundus=data["checkup_result"]["uterine_fundus_height"],
                    blood_sugar=data["checkup_result"]["blood_sugar"],
                    heart_rate=data["checkup_result"]["heart_rate"],
                    note= data["note"],
                    status_inquiry_id=data["checkup_result"]["status_inquiry_anc_id"],
                    sistolik=float(split_blood_pressure[0]),
                    diastolik=float(split_blood_pressure[1]),
                    users_id=user_id,
                    body_temperature = data["checkup_result"]["body_temperatur"]
                )
                
                db.add(inquiry_anc)
                db.commit()
                db.refresh(inquiry_anc)
                
                user = db.query(User).filter(User.id == user_id).first()
                
                inputdata = [user.age,float(split_blood_pressure[0]),float(split_blood_pressure[1]),data["checkup_result"]["blood_sugar"],data["checkup_result"]["body_temperatur"]]
                predictResult = MLService.maternalClassification(inputdata)
                
                return {
                    "status": "success",
                    "message": "success add anc",
                    "data": {
                        "predict_result": predictResult
                    }
                }
                
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "status": "failed",
                        "message": f"content unprocessable: {str(e)}",
                        "data": None
                    }
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "make sure the data is filled in",
                    "data": None
                }
            )