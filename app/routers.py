from fastapi import APIRouter, Query, Response

from app.dao import done_appeal_, get_appeal_by_id, get_appreals, get_user_by_code
from app.schemas import AppealSchema, DateSort
from app.utils import reply_to_email

router = APIRouter()


@router.post("/send_message", name="отправить сообщение по обращению")
async def send_message(id_appreal: int, message: str, user_code: str):
    user = await get_user_by_code(user_code)
    apprel = await get_appeal_by_id(id_appreal)

    if not user:
        return Response(status_code=404, content="User not found")

    if not apprel:
        return Response(status_code=404, content="Appeal not found")

    reply_to_email(apprel.email, f"Ответ от {user.name}", message)

    return Response(status_code=200, content="Message sent")


@router.post("/done_appeal", name="закрыть обращение")
async def done_appeal(user_code: str, id_appeal: int):
    user = await get_user_by_code(user_code)
    apprel = await get_appeal_by_id(id_appeal)

    if not user:
        return Response(status_code=404, content="User not found")

    if not apprel:
        return Response(status_code=404, content="Appeal not found")

    await done_appeal_(id_appeal)
    reply_to_email(apprel.email, f"Ответ от {user.name}", "Ваше обращение выполнено")

    return Response(status_code=200, content="Appeal done")


@router.get("/appeals", name="получить список обращений")
async def get_appeals(status: str | None = None, date_sort: DateSort = Query(...)):
    appeals = await get_appreals(status, date_sort)
    return [AppealSchema.model_validate(appeal).model_dump() for appeal in appeals]
