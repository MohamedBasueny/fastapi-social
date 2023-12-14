## you can use alembic to auto-generate any data that is not yet pupulated from the models.Base 
so it will go and check for the models that is lying in the app.models module and generate the data that is not yet created 
## use this command to auto generate data from your models logic 
> alembic revision --autogenerate -m "msg"