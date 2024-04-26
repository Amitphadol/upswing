#!/bin/bash

# Install Python 3.8 if not already installed
if ! command -v python3.8 &>/dev/null; then
    echo "Installing Python 3.8..."
    sudo apt-get update
    sudo apt-get install -y python3.8
fi

# Install python3.8-venv package to create virtual environments
if ! command -v python3.8-venv &>/dev/null; then
    echo "Installing python3.8-venv..."
    sudo apt-get update
    sudo apt-get install -y python3.8-venv
fi

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3.8 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install RabbitMQ
echo "Installing RabbitMQ..."
sudo apt-get update
sudo apt-get install -y rabbitmq-server

# Install MongoDB
echo "Installing MongoDB..."
sudo apt-get install -y mongodb

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install -r requirements.txt


echo "Setup completed."
