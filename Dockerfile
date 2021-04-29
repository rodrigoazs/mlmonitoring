# Pull base image
FROM python:3.7

WORKDIR /code

# Install dependencies
RUN pip install git+git://github.com/rodrigoazs/mlmonitoring.git

EXPOSE 8000
