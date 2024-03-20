FROM ubuntu:22.04

WORKDIR /opt/watch-dog
ADD . /opt/watch-dog

# update APT repos and install dependencies.
RUN apt-get update && \
    apt-get install libgl1-mesa-glx && \
    apt-get install libglib2.0-0 && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

RUN pip install -r requirements.txt

CMD ["sleep", "3600"]