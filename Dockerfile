FROM quay.io/tictrac/tictrac:CNNGesture-base

COPY server-requirements.txt /app/
RUN pip install -r server-requirements.txt

COPY . /app/

COPY docker-entrypoint.sh /entrypoint.sh
