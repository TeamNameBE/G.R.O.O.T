###########
# BUILDER #
###########

FROM ubuntu as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt install -y gcc python3-dev musl-dev python3-pip\
    && apt install -y libffi-dev
    
# lint
RUN pip3 install --upgrade pip
RUN pip3 install flake8
COPY . .
RUN flake8 --ignore=E501,F401 .

COPY ./requirements.txt .
RUN pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM ubuntu

# create directory for the groot user
RUN mkdir -p /home/groot
RUN adduser groot
RUN usermod -aG groot groot

# create the appropriate directories
ENV HOME=/home/groot
ENV APP_HOME=/home/groot/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apt update && apt install -y python3-pip libgl-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R groot:groot $APP_HOME

# change to the app user
USER groot
