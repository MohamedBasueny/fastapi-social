FROM python:3.10.13 

# the dir that all this python code is running
WORKDIR  /usr/src/app 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 

CMD ["uvicorn" , "app.main:app" , "--host" , "0.0.0.0" , "--port" , "5000"]

