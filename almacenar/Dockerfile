FROM python:3.10-slim
WORKDIR /microservicios2
COPY almacenar.py .
RUN pip install fastapi uvicorn pydantic mysql-connector-python
CMD ["uvicorn", "almacenar:app", "--host", "0.0.0.0", "--port", "8000"]