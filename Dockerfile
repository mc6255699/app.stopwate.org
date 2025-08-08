FROM ubuntu:latest
LABEL authors="mike-a"

ENTRYPOINT ["top", "-b"]