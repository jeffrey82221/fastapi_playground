FROM rayproject/ray
#############################
#    Redis Stack Server     #
#############################
USER root
RUN apt update \
 && apt install -y curl
RUN apt install -y lsb-release \
 && curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg \
 && echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list \
 && apt-get update \
 && apt-get install -y redis \
 && pip install redis-server
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN python -m pip install --upgrade pip wheel 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./executor_api.py /code/executor_api.py
EXPOSE 9999 8265

