FROM ubuntu:22.04

# Install Python and curl
RUN apt-get update && apt-get install -y python3 python3-pip curl

# Copy scripts
COPY ai_agent.py /usr/local/bin/ai_agent.py
COPY exploit.sh /usr/local/bin/exploit.sh

# Make scripts executable
RUN chmod +x /usr/local/bin/*.sh /usr/local/bin/ai_agent.py

# Default command
CMD ["/usr/local/bin/ai_agent.py"]
