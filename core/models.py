from dataclasses import dataclass, field
from typing import Optional, List,Literal

from pydantic import BaseModel

Intent = Literal["WIFI_ISSUE", 
                 "VPN_ISSUE", 
                 "OUTLOOK_ISSUE", 
                 "PRINTER_ISSUE",
                 "PASSWORD_RESET",
                 "SLOW_COMPUTER",
                 "UNKNOWN"]  # example

class IssueDetails(BaseModel):
    os: Optional[str] = None
    device: Optional[str] = None
    app: Optional[str] = None
    error_text: Optional[str] = None
    urgency: Optional[str] = None

class NLUResult(BaseModel):
    intent: Intent
    entities: IssueDetails
    next_question: str