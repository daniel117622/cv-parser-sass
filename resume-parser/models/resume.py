from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List, Optional

@dataclass
class Resume:
    name         : Optional[str]  = None
    email        : Optional[str]  = None
    phone        : Optional[str]  = None
    education    : List           = field(default_factory=list)
    experience   : List           = field(default_factory=list)
    skills       : List           = field(default_factory=list)
    introduction : Optional[str]  = None
    technologies : List           = field(default_factory=list)
    hyperlinks   : List           = field(default_factory=list)

    def get(self):
        """Return the asdict representation of the Resume."""
        return asdict(self)

    def set(self, other):
        """
        Set all fields from another Resume dataclass instance.
        Returns self for chaining.
        """
        if not (is_dataclass(other) and isinstance(other, Resume)):
            raise TypeError("Setter only accepts another Resume dataclass instance.")
        for field_name in self.__dataclass_fields__:
            setattr(self, field_name, getattr(other, field_name))
        return self

    @classmethod
    def from_dict(cls, data):
        return cls(
            name       = data.get("name"),
            email      = data.get("email"),
            phone      = data.get("phone"),
            education  = data.get("education", []),
            experience = data.get("experience", []),
            skills     = data.get("skills", []),
            raw_text   = data.get("raw_text"),
        )


def save_parsed_resume(mongo, parsed_data, filename, token):
    """
    Dummy implementation: just returns a fake ID.
    In a real implementation, this would insert into MongoDB.
    """
    # For now, just return a dummy ID
    return "dummy_resume_id"