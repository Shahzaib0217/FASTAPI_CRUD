from pydantic import BaseModel


class SentimentsBase(BaseModel):
    campaign_id: str
    comment_id: int
    description: str
    sentiment: str


class SentimentsCreate(SentimentsBase):
    pass


class SentimentsUpdate(SentimentsBase):
    pass


class Sentiments(SentimentsBase):
    class Config:
        orm_mode = True
