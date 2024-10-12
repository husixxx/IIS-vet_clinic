# Použijeme oficiálny Python image
FROM python:3.10

# Nastavenie pracovného adresára
WORKDIR /app

# Skopírovanie requirements.txt do kontajnera
COPY backend/requirements.txt .

# Inštalácia závislostí
RUN pip install --no-cache-dir -r requirements.txt

# Skopírovanie všetkých súborov do kontajnera
COPY . .

# Spustenie aplikácie
CMD ["python", "backend/run.py"]