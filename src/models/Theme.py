from typing import Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class Theme(BaseModel):
    """
    Representation of a subtheme (the original themes used to tag questions in the
    original corpus).
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    parent_theme_identifier: str | None
    unique_identifier: str
    level: int
    total: int
