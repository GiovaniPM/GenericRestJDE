FROM giovanimpm/debpyora:1

LABEL   version="1.0.0" \
        description="Agnostic Rest" \
        maintainer="Giovani Mesquita<giovanipm@gmail.com>" \
        Author="Giovani Perotto Mesquita"        

COPY files.zip /api/files.zip
COPY requirements.txt /api/requirements.txt

RUN cd /api && \
    /usr/bin/pip3 install -r requirements.txt

RUN cd /api && \
    unzip files.zip && \
    rm /api/files.zip

RUN echo 'export PATH="$PATH:/opt/oracle/instantclient_19_8"' >> ~/.bashrc && \
    echo 'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/oracle/instantclient_19_8"' >> ~/.bashrc

EXPOSE 8080

CMD ["/usr/bin/python3", "api/api.py"]