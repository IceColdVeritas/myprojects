# # Official Docker Python image becasue it has the latest bug fixes
# FROM python:3.9-bullseye as build

# # Install dependencies
# COPY requirements.txt /app/

# # Copy the source code into a container directory
# COPY con.py /app/

# # Change to the container directory to execute all subsequent code
# WORKDIR /app/

# RUN pip install --upgrade pip && pip install -r requirements.txt

# EXPOSE 5672 15672

# RUN python con.py

# # Run the application. Default to this if no command is added after 'docker run publisher'
# CMD ["python", "con.py"]

FROM python:3.9-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY con.py .

CMD ["python", "con.py"]
