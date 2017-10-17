### SCIZ DOCKERFILE ###

# Based on official nodejs image
FROM node:latest
MAINTAINER sciz@cerv.ovh

# Arguments
ARG PORT=80
ARG WEB_PATH=/var/www/sciz/
ARG MAILDIR_PATH=/mail
ARG MYSQL_HOST=127.0.0.1
ARG MYSQL_PORT=3306
ARG MYSQL_PASSWORD=ThisPasswordShouldBeChangedUsingDockerBuildArgs
ARG JWT_SECRET=ThisSecretShouldBeChangedUsingDockerBuildArgs

# Install additionals packages
RUN apt-get update && apt-get install -y build-essential python2.7 python2.7-dev python-pip libffi-dev cron

# Setup workspace
WORKDIR /sciz
COPY . /sciz

# Configure SCIZ
RUN ./sciz_setup.sh -d $MAILDIR_PATH -h $MYSQL_HOST -o $MYSQL_PORT -m $MYSQL_PASSWORD -s $JWT_SECRET -p $PORT

# Setup the crontab
RUN crontab sciz-crontab

# Setup the webapp environment
RUN mkdir -p $WEB_PATH
RUN cp -rf web/* $WEB_PATH
RUN npm --prefix $WEB_PATH install
RUN npm --prefix $WEB_PATH run postinstall

# Build the webapp
RUN npm --prefix $WEB_PATH run build

# Finish the setup of Python environment
RUN pip install -r requirements.txt

# Volumes
VOLUME /sciz/logs
VOLUME /mail

# Ports
EXPOSE $PORT

# Define defaults for an executing container
ENV WEB_PATH $WEB_PATH
CMD cron && npm --prefix $WEB_PATH start
