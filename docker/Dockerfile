FROM debian:8
RUN mkdir /dv
RUN apt-get update && apt-get install -y python3 python3-pip curl
RUN curl -sSL https://github.com/GiovaniPM/GenericRestJDE/blob/main/api/api.py > /api/api.py
COPY requirements.txt /dv/requirements.txt
RUN cd dv && /usr/bin/pip3 install -r requirements.txt
EXPOSE 8080
CMD ["/usr/bin/python3", "api/api.py"]