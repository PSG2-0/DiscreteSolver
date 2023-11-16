FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY src/ src/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.back:app", "--host", "0.0.0.0", "--port", "8000"]