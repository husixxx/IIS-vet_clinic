# official python image
FROM python:3.10

# set workdir
WORKDIR /app

# copy dependencies
COPY backend/requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy all files to the container
COPY . .

# set environment variables
ENV FLASK_APP=backend/src/app.py

# run 
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "backend.src.app:app"]

