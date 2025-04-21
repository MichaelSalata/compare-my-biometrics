# Use BuildKit syntax
# syntax=docker/dockerfile:1.3
FROM apache/airflow:2.10.4

ENV AIRFLOW_HOME=/opt/airflow

USER root

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    vim curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ARG CLOUD_SDK_VERSION=480.0.0
ENV GCLOUD_HOME=/opt/google-cloud-sdk
ENV PATH="${GCLOUD_HOME}/bin/:${PATH}"

RUN --mount=type=cache,target=/tmp/gcloud-cache \
    DOWNLOAD_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" \
    && CACHE_FILE="/tmp/gcloud-cache/google-cloud-sdk-${CLOUD_SDK_VERSION}.tar.gz" \
    && if [ ! -f "$CACHE_FILE" ]; then \
         curl -fL "${DOWNLOAD_URL}" --output "$CACHE_FILE"; \
       fi \
    && mkdir -p "${GCLOUD_HOME}" \
    && tar xzf "$CACHE_FILE" -C "${GCLOUD_HOME}" --strip-components=1 \
    && "${GCLOUD_HOME}/install.sh" \
       --bash-completion=false \
       --path-update=false \
       --usage-reporting=false \
       --quiet \
    && gcloud --version

USER airflow

COPY requirements.lock.txt .
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-deps -r requirements.lock.txt

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID
