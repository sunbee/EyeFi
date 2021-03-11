FROM        jjanzic/docker-python3-opencv

RUN         apt-get -y update
RUN         apt-get -y upgrade

WORKDIR     /app
VOLUME      /app/snaps
COPY        requirements.txt .
RUN         pip install -r requirements.txt

COPY        . /app

CMD         ["python3", "duralekhi.py", "&&", "python3", "sanchalak.py"]