FROM python:3.10.7-alpine3.16

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev

RUN python3 -m ensurepip

RUN pip install --no-cache-dir --upgrade pip

RUN apk update && \
    apk add --no-cache \
    build-base \
    cmake \
    jpeg-dev \
    zlib-dev \
    git \
    libjpeg \
    libpng-dev \
    tiff-dev \
    openjpeg-dev \
    libwebp-dev \
     linux-headers \
    libx264-dev \
    ffmpeg-dev \
    gstreamer-dev \
    gst-plugins-base \
    gtk+3.0 

# Instala opencv-python
RUN pip install --no-cache-dir opencv-python==4.7.0.72


WORKDIR /doctorIA
COPY ./requirements.txt /doctorIA/requirements.txt







