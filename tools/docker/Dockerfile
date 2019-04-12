FROM ubuntu:latest

# PATH
# ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Install Python 3.6, 2.7 is standard to ubuntu:latest
RUN apt-get update && \
    apt-get install -y python3.6 && \
    apt-get install -y python3-pip

# Set workspace
RUN mkdir /mat-code-challenge
WORKDIR /mat-code-challenge

# Python
ENV alias python=/usr/bin/python3.6
ENV PYTHONPATH /mat-code-challenge

# Add all the project files to the
#ADD . /mat-code-challenge

# Copy source files
COPY data ./data
COPY src ./src
COPY scripts ./scripts
COPY tests ./tests
COPY tools ./tools

# Make run.sh executable
RUN chmod +x /mat-code-challenge/scripts/run.sh

# sudo docker-compose -f tools/docker/docker-compose.yaml build && sudo docker-compose -f tools/docker/docker-compose.yaml up -d

ENTRYPOINT ["./scripts/run.sh"]

# Replace the Entrypoint running the run.sh with this
# to keep the container alive, to be able to debug the container
#ENTRYPOINT ["tail", "-f", "/dev/null"]