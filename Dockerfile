# preferentially run as non-root, but
# ```RUN chown -R $user:$user $HOME```
# takes too long
FROM python:3.7.3-alpine
ENV HOME=/home/pilot
ENV APP_HOME=/home/pilot/gl
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

ADD requirements.txt $APP_HOME/requirements.txt
RUN pip install -r requirements.txt --user
ADD . $APP_HOME/

EXPOSE 5000
ENV PATH='/home/pilot/.local/bin':$PATH
CMD ["/home/pilot/.local/bin/gunicorn", "wsgi", "-b", "0.0.0.0:5000"]

#$ docker build -t guestlist:alpine  .
#$ docker run -p 5000:5000 guestlist:alpine
