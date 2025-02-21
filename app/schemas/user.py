from pydantic import BaseModel, Field


class UserFromDB(BaseModel):
    """
    Class User from DB.
    """

    username: str = Field(description="Name of user to retrieve token")
    password: str = Field(description="Password of user")
    role: str = Field(description="Role of user")

    def dump_model(self) -> dict:
        """
        Dump model function.
        """
        return self.model_dump()
