FROM ubuntu:latest

# Install Python 3.6, 2.7 is standard to ubuntu:latest
RUN apt-get update && \
    apt-get install -y python3.6 && \
    apt-get install -y python3-pip

RUN pip3 install haversine &&  pip3 install ftfy && pip3 install paho_mqtt && pip3 install mock && pip3 install pytest

# Set workspace
RUN mkdir /mat-code-challenge
WORKDIR /mat-code-challenge

# Python
ENV alias python=/usr/bin/python3.6
ENV PYTHONPATH /mat-code-challenge/

# Add the project files to the
COPY data ./data
COPY src ./src
COPY scripts ./scripts
COPY tests ./tests
COPY tools ./tools

# Make run.sh executable
RUN chmod +x /mat-code-challenge/scripts/run.sh

ENTRYPOINT ["./scripts/run.sh"]

# Replace the Entrypoint running the run.sh with this
# to keep the container alive, to be able to debug the container
#ENTRYPOINT ["tail", "-f", "/dev/null"]