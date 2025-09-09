FROM archlinux:base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOSTNAME=SUWALUTIONS \
    VENV_PATH=/root/meow

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm python \
    python-pip bash && \
    pacman -Scc --noconfirm

RUN python -m venv $VENV_PATH

RUN echo "source $VENV_PATH/bin/activate" >> /root/.bashrc

WORKDIR /home

CMD ["/bin/bash"]
