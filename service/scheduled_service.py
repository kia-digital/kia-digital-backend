import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from model.model import Scheduleds,StatusScheduled

class ScheduledService:

    @classmethod
    def add_scheduled(cls, data: dict, db: Session):
        if data:
            try:
                date = datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
                hour = datetime.datetime.strptime(data["hour"], "%H:%M").time()

                scheduled = Scheduleds(
                    name=data["name"],
                    date=date,
                    hours=hour,
                    location=data["location"],
                    status=False,
                    status_scheduled_id=data["status_scheduled_id"],
                    moms_id=data["mom_id"]
                )

                db.add(scheduled)
                db.commit()
                db.refresh(scheduled)
                db.close()

                return {
                    "status": "success",
                    "message": "success add scheduled",
                    "data": data
                }

            except Exception as e:
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
            
    @classmethod
    def getAllScheduledById(cls,users_id: str, db: Session):
        try:
            scheduleds = (db.query(Scheduleds)
            .join(StatusScheduled,Scheduleds.status_scheduled_id == StatusScheduled.id)
            .filter(Scheduleds.moms_id == users_id,Scheduleds.status == False)
            .all()
            )
            
            result = {
                "status": "success",
                "message": "success get scheduled",
                "data": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "date": s.date.isoformat(),
                        "hours": s.hours.isoformat(),
                        "location": s.location,
                        "status_scheduled": s.status_scheduled.name,
                        "moms_id": s.moms_id
                    }
                    for s in scheduleds
                ]
            }

            db.close()
            return result
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "internal server error",
                    "data": None
                }
            )  
        
    @classmethod
    def update_scheduled(cls, id: str, data: dict, db: Session):
        try:
            scheduled = db.query(Scheduleds).filter(Scheduleds.id == id).first()

            if not scheduled:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "status": "error",
                        "message": "Scheduled not found",
                        "data": None
                    }
                )

            # Update fields if present in data
            if "name" in data:
                scheduled.name = data["name"]
            if "date" in data:
                scheduled.date = datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
            if "hour" in data:
                scheduled.hours = datetime.datetime.strptime(data["hour"], "%H:%M").time()
            if "location" in data:
                scheduled.location = data["location"]
            if "status" in data:
                scheduled.status = data["status"]
            if "status_scheduled_id" in data:
                scheduled.status_scheduled_id = data["status_scheduled_id"]

            db.commit()
            db.refresh(scheduled)
            db.close()

            return {
                "status": "success",
                "message": "Scheduled updated successfully",
                "data": {
                    "id": scheduled.id,
                    "name": scheduled.name,
                    "date": scheduled.date.isoformat(),
                    "hour": scheduled.hours.isoformat(),
                    "location": scheduled.location,
                    "status": scheduled.status,
                    "status_scheduled_id": scheduled.status_scheduled_id,
                    "moms_id": scheduled.moms_id
                }
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": f"internal server error: {str(e)}",
                    "data": None
                }
            )
     
    @classmethod
    def getById(cls, id: str, users_id: str, db: Session):
        try:
            scheduled = (
                db.query(Scheduleds)
                .join(StatusScheduled, Scheduleds.status_scheduled_id == StatusScheduled.id)
                .filter(
                    Scheduleds.moms_id == users_id,
                    Scheduleds.status == False,
                    Scheduleds.id == id
                )
                .first()
            )

            if not scheduled:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "status": "error",
                        "message": "Scheduled not found",
                        "data": None
                    }
                )

            result = {
                "status": "success",
                "message": "success get scheduled",
                "data": {
                    "id": scheduled.id,
                    "name": scheduled.name,
                    "date": scheduled.date.isoformat(),
                    "hours": scheduled.hours.isoformat(),
                    "location": scheduled.location,
                    "status_scheduled": scheduled.status_scheduled.name,
                    "moms_id": scheduled.moms_id
                }
            }

            db.close()
            return result

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": f"internal server error: {str(e)}",
                    "data": None
                }
            )
