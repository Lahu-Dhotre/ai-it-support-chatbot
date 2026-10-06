from dataclasses import dataclass, field
from typing import Optional, List
from pydantic import BaseModel, ValidationError

@dataclass
class Movie:
    title: str
    year: int

    def __post_init__(self):
        if self.year < 1888:
            raise ValueError("Year must be 1888 or later")
        return f"Movie(title='{self.title}', year={self.year})"

m = Movie("Interstellar", 1900)
print(m.title)  # Interstellar
print(m)        # Movie(title='Interstellar', year=2014)


@dataclass
class IssueDetails:
    os: Optional[str] = None
    device: Optional[str] = None
    app: Optional[str] = None
    error_text: Optional[str] = None
    urgency: Optional[str] = None

    def validate_for_intent(self, intent: str) -> List[str]:
        missing = []
        if intent == "VPN_ISSUE" and not self.os:
            missing.append("os")
        if intent == "SOFTWARE_INSTALL" and not self.app:
            missing.append("app")
        if intent == "ACCESS_REQUEST" and not self.app:
            missing.append("app")
        return missing

 
issue11 = IssueDetails(
    os="",
    device="",
    app="Outlook",
    error_text="Cannot open application",
    urgency="high"
)
print(issue11.validate_for_intent("VPN_ISSUE"))  # []

@dataclass
class SessionState:
    session_id: str
    intent: str = "UNKNOWN"
    entities: IssueDetails = field(default_factory=IssueDetails)
    last_steps: list[str] = field(default_factory=list)
    asked_fix_confirm: bool = False
    escalation_mode: bool = False

session = SessionState(session_id="abc123")
session.entities = issue11
print("session entities app:", session.entities.app)  # Outlook
print(session.session_id)  # abc123
print(session.intent)      # UNKNOWN    


from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Valid input
user = User(name="Alice", age=30)
print(user)  # name='Alice' age=30

# Invalid input (age is not an int)
try:
    user = User(name="Bob", age="not a number")
except ValidationError as e:
    print("Validation error:", e)