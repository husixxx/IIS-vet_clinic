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
ENV PYTHONPATH=/app/backend
# expose port 5000
EXPOSE 5000

# run gunicorn
CMD ["sh", "-c", "cd backend && python run.py"]

