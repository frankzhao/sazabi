FROM centos:7
LABEL maintainer="frank@frankzhao.net"

ENV REPOSITORY=https://github.com/frankzhao/sazabi
ENV INSTALLDIR=/usr/local/bin/sazabi
ENV CONFIGDIR=/etc/sazabi
ENV CONFIGFILE=config.yaml
ENV LOGFILE=/var/log/sazabi.log
ENV DAEMON=bin/sazabi

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
  && yum update -y \
  && yum install -y python36u python36u-pip python36u-devel git \
  && yum clean all

RUN git clone $REPOSITORY $INSTALLDIR

WORKDIR $INSTALLDIR

RUN mkdir -p $CONFIGDIR && touch $CONFIGDIR/$CONFIGFILE && chmod 750 $CONFIGDIR/$CONFIGFILE
RUN pip3.6 install -r requirements.txt && pip3.6 install -e .

ENTRYPOINT python3.6 $DAEMON -c $CONFIGDIR/$CONFIGFILE -l $LOGFILE