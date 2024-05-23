FROM ubuntu
RUN apt update -y && apt upgrade -y
RUN apt install gcc valgrind make time -y
COPY . /tp3
WORKDIR /tp3
CMD make local
