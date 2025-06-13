from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from model.model import InquiryAnc,WeeklyMonitoring,User
import numpy as np

from service.ml_service import MLService

class ArticleService:
    @classmethod
    def getRecommendation(cls, user_id: str, trimester: int, db: Session):
        try:
            inquiry = (
                db.query(User)
                .outerjoin(InquiryAnc, InquiryAnc.users_id == User.id)
                .outerjoin(WeeklyMonitoring, WeeklyMonitoring.users_id == User.id)
                .filter(InquiryAnc.users_id == user_id)
                .first()
            )

            if not inquiry or not inquiry.inquiry_anc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"status": "error", "message": "Data ANC tidak ditemukan", "data": None}
                )

            anc = inquiry.inquiry_anc[0]
            monitor = getattr(inquiry, "weekly_monitorings", None)

            input = np.array([[
                anc.sistolik if anc.sistolik else 0,
                anc.diastolik if anc.diastolik else 0,
                anc.blood_sugar if anc.blood_sugar else 0,
                anc.body_temperature if anc.body_temperature else 0,
                trimester,
                anc.heart_rate if anc.heart_rate else 0,
                getattr(monitor, "fever", 0),
                getattr(monitor, "headache", 0),
                getattr(monitor, "insomnia_or_anxiety", 0),
                getattr(monitor, "abdominal_pain", 0),
                getattr(monitor, "diarrhea", 0)
            ]])

            article = MLService.articleRecommendation(input)

            return {
                "status": "success",
                "message": "success get recommendation",
                "data": article
            }

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": f"internal server error: {str(e)}",
                    "data": None
                }
            )
