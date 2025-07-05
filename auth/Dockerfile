FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic[email] passlib[bcrypt] pyjwt python-dotenv

# COPY auth.db ./auth.db

EXPOSE 6190
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6190"]
