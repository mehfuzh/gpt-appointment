FROM python:3.9.16

ENV HOME=/home/assort-health
ENV TMPDIR='/var/tmp'

# ENV DATA_DIR='/nlp_data'
# ENV CUDA_VISIBLE_DEVICES=0
# ENV NLTK_DATA=/app/nltk_data

RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libasound-dev libsndfile1-dev -y
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY . ${HOME}

RUN python -m pip install -U pip

WORKDIR ${HOME}

RUN python -m pip install -r requirements.txt

# RUN set -eux; \
#     python -m nltk.downloader stopwords

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]
