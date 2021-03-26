FROM giovanimpm/debpyora:1

LABEL   Version="1.0.0" \
        Description="Debian Linux with Python 3 and Oracle client 19.8" \
        Maintainer="Giovani Mesquita<giovanipm@gmail.com>" \
        Author="Giovani Perotto Mesquita"        

ENV DOWNLOAD_TEMP=/downloads \
    ORACLE_BASE=/opt/oracle \
    ORACLE_HOME=/opt/oracle/instantclient_19_8 \ 
    ORACLE_SITE_BASIC="https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-sqlplus-linux.x64-19.8.0.0.0dbru.zip" \
    ORACLE_SITE_CLIENT="https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-basic-linux.x64-19.8.0.0.0dbru.zip?xd_co_f=fae07a5a-ae5f-4c1a-8ce0-f41ed4a394c5'" \
    PATH="$PATH:/opt/oracle/instantclient_19_8" \
    LD_LIBRARY_PATH=/opt/oracle/instantclient_19_8 \
    ORACLE_SERVER="0.0.0.0"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  unzip \
                        libaio-dev \
                        python3 \
                        python3-pip \
                        curl

RUN mkdir $DOWNLOAD_TEMP && \
    curl --progress-bar $ORACLE_SITE_CLIENT -o $DOWNLOAD_TEMP/instantclient-basic-linux.zip && \
    curl --progress-bar $ORACLE_SITE_BASIC -o $DOWNLOAD_TEMP/instantclient-sqlplus-linux.zip && \
    mkdir $ORACLE_BASE && \
    cd $DOWNLOAD_TEMP && \
    unzip $DOWNLOAD_TEMP/instantclient-basic-linux.zip -d $ORACLE_BASE && \
    unzip $DOWNLOAD_TEMP/instantclient-sqlplus-linux.zip -d $ORACLE_BASE && \
    rm $DOWNLOAD_TEMP/instantclient-basic-linux.zip && \
    rm $DOWNLOAD_TEMP/instantclient-sqlplus-linux.zip

RUN echo 'export PATH="$PATH:/opt/oracle/instantclient_19_8"' >> ~/.bashrc && \
    echo 'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/oracle/instantclient_19_8"' >> ~/.bashrc