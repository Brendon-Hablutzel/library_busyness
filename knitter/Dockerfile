FROM rocker/r-apt:bionic

RUN add-apt-repository ppa:marutter/c2d4u
RUN apt update

WORKDIR /knitter

COPY requirements-bin.txt .
RUN cat requirements-bin.txt | xargs apt install -y -qq

# cleans up package lists
RUN rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["Rscript", "knit.R"]