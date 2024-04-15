# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine as builder
Expose 8000
WORKDIR /app

#Install system dependencies
RUN apk update
RUN apk add \
    pkgconfig \
    gcc \
    musl-dev \
    bash \
    mariadb-dev

#Install any needed packages s[ecified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

#Copy the current directory contents into the container at /usr/src/app
COPY . /app
# Run server
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]