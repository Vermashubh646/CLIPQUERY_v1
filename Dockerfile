# baseimage
FROM python:3.12-slim

# workdir 
WORKDIR /app

#  install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# copy requirements t ocontainer
COPY requirements.txt .

# run
RUN pip install --no-cache-dir -r requirements.txt

# copy app to container
COPY app/ ./app/

# port
EXPOSE 8000

# command
CMD ["uvicorn", "app.main:app","--host","0.0.0.0","--port", "8000"]

