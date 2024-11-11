# Use an official Debian image as a parent image
FROM debian:stable

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install Python, pip, and Ansible
RUN apt-get update && \
    apt-get install -y python3 python3-pip ansible && \
    apt-get clean

# Set Python3 as the default python command
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any Python dependencies specified in requirements.txt
# If you don't have a requirements.txt, you can skip this part
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Run main.py when the container launches, allowing command-line arguments
ENTRYPOINT ["python", "main.py"]
