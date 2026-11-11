from pydantic import BaseModel, Field, ConfigDict, field_validator

class ArticleCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length= 150)
    description: str | None = None
    content: str = Field(min_length=1, max_length=20000)

class ArticleUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    content: str | None = Field(default=None, min_length=1, max_length=20000)

    @field_validator("title", "content", mode="before")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("Field cannot be null")

        return value