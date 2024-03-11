from src.ctrm.models.users import User
from src.ctrm.models.clients import Client
from src.ctrm.models.logs import InboundLog, OutboundLog


def gather_models():
    return [User, Client, InboundLog, OutboundLog]
