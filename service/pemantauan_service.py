from fastapi import HTTPException, status
import datetime
from sqlalchemy.orm import Session

from model.model import WeeklyMonitoring

class PemantauanService:
    @classmethod
    def addPemantauan(cls, data: dict, user_id: str, db: Session):
        if data:
            try:
                def parse_bool(val):
                    if isinstance(val, bool):
                        return val
                    if isinstance(val, str):
                        return val.lower() == "true"
                    return False

                weeklyMonitoring = WeeklyMonitoring(
                    users_id=user_id,
                    weekly_pregnantcy=int(data["weekly_pregnantcy"]),
                    fever=parse_bool(data.get("fever", False)),
                    headache=parse_bool(data.get("headache", False)),
                    insomnia_or_anxiety=parse_bool(data.get("insomnia_or_anxiety", False)),
                    tb_risk=parse_bool(data.get("tb_risk", False)),
                    fetal_movement=parse_bool(data.get("fetal_movement", False)),
                    abdominal_pain=parse_bool(data.get("abdominal_pain", False)),
                    discharge=parse_bool(data.get("discharge", False)),
                    urination_issues=parse_bool(data.get("urination_issues", False)),
                    diarrhea=parse_bool(data.get("diarrhea", False)),
                    type_inquiry=int(data["type_inquiry"])
                )

                db.add(weeklyMonitoring)
                db.commit()
                db.refresh(weeklyMonitoring)

                return {
                    "status": "success",
                    "message": "success add weekly monitoring",
                    "data": data
                }

            except Exception as e:
                print(e)
                db.rollback()
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
