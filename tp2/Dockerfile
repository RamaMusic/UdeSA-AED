FROM ubuntu
RUN apt update -y && apt upgrade -y
# RUN apt-get update -y && apt-get upgrade -y
RUN apt install gcc valgrind make -y
COPY . /tp
WORKDIR /tp
CMD make local
