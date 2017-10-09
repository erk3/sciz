### SCIZ DOCKERFILE ###

# Based on official python2.7 image
FROM python:2.7
MAINTAINER sciz@cerv.ovh

# Install additionals packages
RUN apt-get update && apt-get install -y build-essential libffi-dev cron

# Setup workspace
WORKDIR /sciz
COPY . /sciz

# Setup the crontab
ADD sciz-crontab /etc/cron.d/sciz-crontab
RUN chmod 0644 /etc/cron.d/sciz-crontab

# Finish the setup of Python environment
RUN pip install -r requirements.txt

# Volumes
VOLUME /sciz
VOLUME /mail

# Define defaults for an executing container
CMD ["cron", "-f"]
