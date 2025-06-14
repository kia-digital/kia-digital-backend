import datetime
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from model.model import InquiryAnc, StatusInquiry, User, CategoryClassification
from service.ml_service import MLService


class AncService:

    @classmethod
    def getAncById(cls,id_anc:str,db:Session):
        try:
            anc =(
                db.query(InquiryAnc)
                .outerjoin(StatusInquiry,InquiryAnc.status_inquiry_id==StatusInquiry.id)
                .outerjoin(User,InquiryAnc.users_id==User.id)
                .filter(InquiryAnc.id == id_anc)
                .first()
            ) 
            
            result = {
                    "status": "success",
                    "message": "success get anc",
                    "data": {
                        "body_weight": anc.body_weight,
                        "heart_rate": anc.heart_rate,
                        "blood_pressure": f"{anc.sistolik}/{anc.diastolik}",
                        "status": anc.status_inquiry.name,
                        "uterine_fundus_height": anc.height_uterine_fundus,
                        "blood_sugar": anc.blood_sugar,
                        "body_temperature": anc.body_temperature
                    }
                    
                }
            
            db.close()
            return result
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
    
    @classmethod
    def updateAncReport(cls, data: dict, id_anc: str, db: Session):
        try:
            anc = db.query(InquiryAnc).filter(InquiryAnc.id == id_anc).first()
            if not anc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "status": "failed",
                        "message": "ANC record not found",
                        "data": None
                    }
                )

            option = ["location", "medical_officer", "note"]
            checkup_result = data.get("checkup_result", {})

            # Update field utama dari ANC
            for key, value in data.items():
                if hasattr(anc, key):
                    if key in option:
                        setattr(anc, key, value)
                    elif key == "scheduled":
                        setattr(anc, key, datetime.datetime.strptime(value, "%Y-%m-%d").date())

            # Update hasil pemeriksaan
            for key, value in checkup_result.items():
                if hasattr(anc, key):
                    if key == "blood_pressure":
                        split_blood_pressure = value.split("/")
                        if len(split_blood_pressure) != 2:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail={
                                    "status": "failed",
                                    "message": "Invalid blood_pressure format. Use systolic/diastolic",
                                    "data": None
                                }
                            )
                        setattr(anc, "sistolik", float(split_blood_pressure[0]))
                        setattr(anc, "diastolik", float(split_blood_pressure[1]))
                    else:
                        setattr(anc, key, value)

            # Komit ke database
            db.commit()
            db.refresh(anc)

            # Ambil user untuk klasifikasi ML
            user = db.query(User).filter(User.id == anc.users_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "status": "failed",
                        "message": "User not found for ANC",
                        "data": None
                    }
                )

            # Validasi dan klasifikasi
            blood_pressure = checkup_result.get("blood_pressure")
            if not blood_pressure:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "status": "failed",
                        "message": "Blood pressure is required in checkup_result",
                        "data": None
                    }
                )
            split_blood_pressure = blood_pressure.split("/")

            inputdata = [
                user.age if user.age else 20,
                float(split_blood_pressure[0]),
                float(split_blood_pressure[1]),
                checkup_result.get("blood_sugar", 0),
                checkup_result.get("body_temperatur", 0)
            ]
            print("ML input:", inputdata)

            predictResult = MLService.maternalClassification(inputdata)
            category = db.query(CategoryClassification).filter(CategoryClassification.users_id == anc.users_id).first()

            if not category:
                categoryData = CategoryClassification(
                    users_id=anc.users_id,
                    tag=predictResult
                )
                db.add(categoryData)
                db.commit()
                db.refresh(categoryData)
            else:
                category.tag = predictResult
                db.commit()
                db.refresh(category)

            db.close()
            return {
                "status": "success",
                "message": "success update anc",
                "data": {
                    "predict_result": predictResult
                }
            }

        except Exception as e:
            print("ERROR:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "Internal Server Error",
                    "data": None
                }
            )

    
    @classmethod
    def getAll(cls,user_id:str,db:Session):
        
        try:
            ancs =(
                db.query(InquiryAnc)
                .outerjoin(StatusInquiry,InquiryAnc.status_inquiry_id==StatusInquiry.id)
                .outerjoin(User,InquiryAnc.users_id==User.id)
                .filter(InquiryAnc.users_id == user_id)
                .all()
            ) 
            
            result = {
                    "status": "success",
                    "message": "success get anc",
                    "data": [
                        {
                            "id": anc.id,
                            "scheduled": anc.scheduled_at.isoformat() if anc.scheduled_at else None,
                            "location": anc.location,
                            "checkup_result":{
                                "body_weight": anc.body_weight,
                                "heart_rate" : anc.heart_rate,
                                "blood_pressure" : f"{anc.sistolik}/{anc.diastolik}",
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
                
                inputdata = [user.age if user.age else 20,float(split_blood_pressure[0]),float(split_blood_pressure[1]),data["checkup_result"]["blood_sugar"],data["checkup_result"]["body_temperatur"]]
                print(inputdata)
                predictResult = MLService.maternalClassification(inputdata)
                category = (db.query(CategoryClassification).filter(CategoryClassification.users_id == user_id).first())
                
                if not category:
                    categoryData = CategoryClassification(
                        users_id=user_id,
                        tag = predictResult
                    )
                    db.add(categoryData)
                    db.commit()
                    db.refresh(categoryData)
                    db.close()
                else:
                    category.tag = predictResult
                    
                    db.commit()
                    db.refresh(category)
                    db.close()
                    
                return {
                    "status": "success",
                    "message": "success add anc",
                    "data": {
                        "predict_result": predictResult
                    }
                }
                
            except Exception as e:
                print("cihuy",e)
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