from pydantic import BaseModel, ConfigDict

class ModelBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=False,
        str_to_lower=False,
        validate_assignment=True,
    )
