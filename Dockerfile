FROM archlinux:base

COPY . /PurrfectKit/.

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOSTNAME=SUWALUTIONS \
    HF_HOME=/PurrfectKit/.cache/huggingface/ \
    TIKTOKEN_CACHE_DIR=/PurrfectKit/.cache/tiktoken/ \
    TESSDATA_PREFIX=/PurrfectKit/.cache/traineddata/ \
    EASYOCR_MODULE_PATH=/PurrfectKit/.cache/eazy/ \
    DOCTR_CACHE_DIR=/PurrfectKit/.cache/doctr/ \
    VENV_PATH=/root/meow

RUN mkdir -p /root/.cache/datalab && \
    mv /PurrfectKit/.cache/datalab /root/.cache/datalab

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm python \
    python-pip bash \
    tesseract \
    tesseract-data-eng \
    tesseract-data-tha && \
    pacman -Scc --noconfirm

RUN python -m venv $VENV_PATH

RUN echo "source $VENV_PATH/bin/activate" >> /root/.bashrc

RUN $VENV_PATH/bin/pip install -e /PurrfectKit/.

WORKDIR /home

CMD ["/bin/bash"]
