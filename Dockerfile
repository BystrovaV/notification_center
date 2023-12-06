FROM python:3.12.0-slim as base

WORKDIR /src

ENV USER=app-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev build-essential \
    && apt-get clean \
    && addgroup --system $USER && adduser --system --group $USER

ENV BUILDER_DIR=/usr/src/$USER

FROM base as builder

WORKDIR $BUILDER_DIR

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir "$BUILDER_DIR"/wheels -r requirements.txt


FROM base

ENV HOME_DIR=/home/$USER
ENV APP_DIR=$HOME_DIR/src

WORKDIR $APP_DIR

COPY --from=builder $BUILDER_DIR/wheels /wheels
COPY --from=builder $BUILDER_DIR/requirements.txt $HOME_DIR
RUN pip install --no-cache /wheels/*

COPY ./src $APP_DIR

RUN chown -R "$USER":"$USER" $APP_DIR

USER $USER

CMD ["python", "main.py"]
