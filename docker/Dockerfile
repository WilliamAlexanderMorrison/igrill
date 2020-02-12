FROM debian:stretch
RUN apt-get update && apt-get install -y \
        libglib2.0-dev \
        pkg-config \
        git \
        python-pip
RUN pip install paho-mqtt==1.4.0 \
		PyYAML==5.1.2 \
		yamlreader==3.0.4 \
		future==0.17.1 \
        psutil
ADD https://api.github.com/repos/WilliamAlexanderMorrison/rpi-monitor-mqtt/git/refs/heads/master version.json
RUN git clone https://github.com/WilliamAlexanderMorrison/rpi-monitor-mqtt.git
WORKDIR /rpi-monitor-mqtt
RUN mkdir config
VOLUME config
CMD ./monitor.py -c config