# Pull base image
FROM python:3.7

WORKDIR /code

# Install dependencies
RUN pip3 install pandas
RUN pip3 install requests
RUN pip3 install git+git://github.com/rodrigoazs/mlmonitoring.git \
    && apt-get clean

EXPOSE 8000
