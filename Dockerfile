#running cmake in Docker

FROM ubuntu:latest

MAINTAINER Jeff Machyo <machyo.j@northeastern.edu>

RUN apt-get -y update && apt-get install -y
RUN apt-get -y install g++ cmake git 


COPY . .

WORKDIR .

RUN rm -rf Version_1/out/build CMakelists.txt
RUN cmake -S Version_1/ -B Version_1/out/build
RUN make -C Version_1/out/build

# CMD ["./out/build/main"]
CMD ["bash","Version_1/run.sh"]