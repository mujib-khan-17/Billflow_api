from pydantic import BaseSettings
 
class Settings(BaseSettings):
    DATABASE_URL : str
    API_PRIFIX : str 
    JWT_SECRET: str 
    ALGORITHM : str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    USER_NOT_FOUND : str = "User not found"
    PASSWORD_INCORRECT : str = "Password is incorrect"
    NOT_AUTHORIZED : str = "You are not authorized to perform this action."
    ADD_NOT_AUTHORIZED : str = "You are not authorized to add a project."
    UPDATE_NOT_AUTHORIZED : str = "You are not authorized to update this project."
    DELETE_NOT_AUTHORIZED : str = "You are not authorized to delete this project."
    NOT_FOUND : str = "Project not found or already deleted"
    PROJECT_DELETE_SUCCESS : str = "Project deleted successfully"
    class Config:
        env_file = ".env"
    
settings = Settings()