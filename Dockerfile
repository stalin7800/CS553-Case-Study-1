# get base container from Python
FROM python:3.10-slim


WORKDIR /opt/app 
COPY . .
# install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /opt/app/requirements.txt


ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get upgrade -yq ca-certificates && \
    apt-get install -yq --no-install-recommends \
    prometheus-node-exporter 

# Expose the port for gradio
EXPOSE 7860 
EXPOSE 8000
EXPOSE 9100

ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD bash -c "prometheus-node-exporter --web.listen-address=':9100' & python opt/app/app.py"
