FROM python:3.9.16-slim-buster

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Ensure apt is in non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies.
RUN apt-get -y update --no-install-recommends \
    && apt-get -y install --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    apt-utils \
    dialog \
    git \
    vim \
    bash-completion -y \
    && apt-get autoremove -y \
    && apt-get clean -y

# Create the user.
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN mkdir /workspace

COPY requirements.txt /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt
COPY . /workspace

ENV DEBIAN_FRONTEND=dialog

USER $USERNAME


# CMD ["python3", "app.py"]