from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

#this class is used to load env variable ,,, not in .env file but global vars
class Settings(BaseSettings) : 
    database_hostname :str = "localhost"
    database_name : str  
    database_port : str  
    database_username : str 
    database_password : str 
    jwt_secret_key : str 
    jwt_algorithm : str 
    jwt_access_token_expire_minutes : int 

    # model_config = SettingsConfigDict(env_file='.env')
    #use the below line for production 
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
# print(settings.model_dump())