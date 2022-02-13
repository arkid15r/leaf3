FROM python:3.10-slim


# Environment variables.
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Packages
RUN apt-get clean && apt-get update && apt-get -y upgrade
RUN apt-get -y --no-install-recommends install \
  build-essential \
  default-libmysqlclient-dev \
  gcc \
  libgeos-dev \
  npm \
  yarnpkg

# Create a user.
RUN adduser --uid 1000 --disabled-password -gecos '' leaf3

# Set work directory.
WORKDIR /home/leaf3

# App content.
COPY apps /home/leaf3/apps/
COPY client /home/leaf3/client/
COPY conf /home/leaf3/conf/
COPY locale /home/leaf3/locale/

COPY manage.py run.sh /home/leaf3/
RUN chmod 0744 /home/leaf3/run.sh

# Backend.
COPY requirements /home/leaf3/requirements
RUN python -m venv /home/leaf3/venv
RUN /home/leaf3/venv/bin/pip install --upgrade pip
RUN /home/leaf3/venv/bin/pip install --no-cache-dir -r requirements/prod.txt

# Frontend.
WORKDIR /home/leaf3/client/
RUN yarnpkg install && yarnpkg build

# RUN mkdir /home/leaf3/static

RUN chown leaf3:leaf3 -R /home/leaf3/

WORKDIR /home/leaf3/

# Set port.
EXPOSE 8181

# Set user.
USER leaf3

# Run the process.
# CMD /home/leaf3/venv/bin/gunicorn --user leaf3 --bind 0.0.0.0:8181 --workers 2 conf.wsgi:application
