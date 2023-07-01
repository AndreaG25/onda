from fastapi import APIRouter, Body, Depends
from ..auth.auth_bearer import JWTBearer
from .utils_functions.models import NewTicketSchema
from .utils_functions.createid import createID
from .utils_functions.crud import createTicket
from ..auth.auth_handler import  get_id_user, get_username


router = APIRouter()

@router.post("/createticket", dependencies=[Depends(JWTBearer())])
async def createTicket_function(ticketObj: NewTicketSchema):
    id_user = get_id_user(jwtoken=ticketObj.token)
    id_ticket = createID(aim="tkt")
    return {
        "result": createTicket(id_ticket=id_ticket, id_user=id_user, ticketOBJ=ticketObj)
    }