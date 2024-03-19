FROM python:3.12

RUN pip install \
  openai \
  python-dotenv

ENV TERM=xterm-256color
ENV PATH=$PATH:/ai

COPY . /ai
WORKDIR /ai
