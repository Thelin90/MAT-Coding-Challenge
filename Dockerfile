FROM ubuntu:latest

# PATH
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Python
ENV alias python=/usr/bin/python3.6
ENV PYTHONPATH /etc/app/

# Install Python 3.6, 2.7 is standard to ubuntu:latest
RUN apt-get update && \
    apt-get install -y python3.6 && \
    apt-get install -y python3-pip

# Set workspace
WORKDIR /etc/app

# Add all the project files to the
ADD . /etc/app

# Make run.sh executable
RUN chmod +x /etc/app/tools/docker/run.sh

ENTRYPOINT ["./run.sh"]

# Replace the Entrypoint running the run.sh with this
# to keep the container alive, tobe able to debug the container
#ENTRYPOINT ["tail", "-f", "/dev/null"]