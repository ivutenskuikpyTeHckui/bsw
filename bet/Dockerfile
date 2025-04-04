FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8001

CMD ["uvicorn", "src.drivers.rest.main:app", "--host", "0.0.0.0", "--port", "8001"]