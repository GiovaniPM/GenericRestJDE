FROM debian
RUN mkdir /api
RUN apt-get update && apt-get install -y python3 python3-pip curl
RUN curl -sSL https://raw.githubusercontent.com/GiovaniPM/GenericRestJDE/main/api/api.py > /api/api.py
COPY requirements.txt /api/requirements.txt
RUN cd api && /usr/bin/pip3 install -r requirements.txt
EXPOSE 8080
CMD ["/usr/bin/python3", "api/api.py"]