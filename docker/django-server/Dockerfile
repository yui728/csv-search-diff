FROM python:3.7

RUN apt-get update \
    && apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
	postgresql-client \
	nginx \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./src/requirements.txt .
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

EXPOSE 8000