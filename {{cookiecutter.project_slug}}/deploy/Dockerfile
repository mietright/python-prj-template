FROM alpine:3.3

ARG version={{cookiecutter.version}}
ARG workdir=/opt
RUN rm -rf $workdir
RUN mkdir -p $workdir
COPY {{cookiecutter.project_slug}}-$version.tar.gz $workdir

WORKDIR $workdir
RUN tar xzvf {{cookiecutter.project_slug}}-$version.tar.gz
WORKDIR $workdir/{{cookiecutter.project_slug}}-$version

RUN apk --update add python py-pip openssl ca-certificates git
RUN apk --update add --virtual build-dependencies python-dev build-base wget openssl-dev libffi-dev
RUN pip install pip -U
RUN pip install gunicorn -U \
  && python setup.py install

CMD ["{{cookiecutter.project_slug}}"]
