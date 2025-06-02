FROM python:3.10-slim
WORKDIR /microservicios2
COPY resta.py .
RUN pip install fastapi uvicorn pydantic requests
CMD ["uvicorn", "resta:app", "--host", "0.0.0.0", "--port", "8000"]