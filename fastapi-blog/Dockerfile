FROM python:3.9.7-slim-bullseye

# PYTHONUNBUFFERED 1 causes all output to stdout to be flushed immediately, without helding logs somewhere
ENV PYTHONUNBUFFERED 1

# We use virtual env as our environment, to avoid installing dependencies in system python and avoid pip bugs
# This commands equalls to source venv/bin/acitvate but for the whole container
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create dir's for app and its requirement file
RUN mkdir -p /app/src
WORKDIR /app/src

# COPY files to container env and install application dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt

# COPY app code
COPY src /app/src
COPY setup.cfg setup.py /app/

# Install app as python package and set PYTHONPATH to project root so imports will work correctly
RUN cd /app && pip install .
ENV PYTHONPATH=/app/src
