FROM python:3-alpine

# RUN apt update && apt upgrade -y && apt install -y --no-install-recommends locales libzbar0 && \
#     echo 'de_DE.UTF-8 UTF-8' >> /etc/locale.gen && \
#     locale-gen && update-locale LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8 && \
#     pip install --upgrade pip && \
#     mkdir -p /churchbot && \
#     apt-get clean && rm -rf /var/lib/apt/* /var/cache/apt/*

ENV VIRTUAL_ENV=/opt/venv \
    MY_USER=xfs
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /bot
ADD ./requirements.txt ./

RUN pip install -r requirements.txt

ADD ./ ./
RUN chown -R $MY_USER ./

USER $MY_USER

CMD ["python", "main.py"]
