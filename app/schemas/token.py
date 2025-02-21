from pydantic import BaseModel, Field


class TokenCredentials(BaseModel):
    """
    Class Token credentials.
    """

    username: str = Field(description="Name of user to retrieve token")
    password: str = Field(description="Password of user")

    def dump_model(self) -> dict:
        """
        Dump model function.
        """
        return self.model_dump()


class TokenSchema(BaseModel):
    """
    Class Token schema
    """

    access_token: str = Field(description="Token to access where for requested")
    token_type: str = Field(description="Type of token")

    def dump_model(self) -> dict:
        """
        Dump model function.
        """
        return self.model_dump()
