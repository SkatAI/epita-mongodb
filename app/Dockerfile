# spins up a bash shell

FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    curl \
    vim \
    pkg-config \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install required dependencies and add MongoDB GPG key
# RUN apt-get update && apt-get install -y wget gnupg && \
#     wget -qO - https://pgp.mongodb.com/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg && \
#     echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
#     apt-get update && \
#     apt-get install -y mongosh && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*


# Upgrade pip
RUN pip3 install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG APP_NAME=EpitaMongoDB

RUN echo "alias ll='ls -lah'" >> ~/.bashrc && \
    echo "PS1='\[\033[01;32m\]\u@$APP_NAME\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> ~/.bashrc



CMD ["/bin/bash"]