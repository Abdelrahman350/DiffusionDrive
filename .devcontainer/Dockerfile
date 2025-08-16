# -----------------------------------------------------------------------------
# Stage 1: Builder Stage - Install dependencies and set up the environment
# -----------------------------------------------------------------------------
FROM nvcr.io/nvidia/cuda-dl-base:25.04-cuda12.9-devel-ubuntu24.04 AS builder

# Build arguments
ARG USERNAME="abdelrahman"
ARG USER_UID=1000
ARG USER_GID=1000

ARG USER_PASSWORD="ubuntu"
ARG ENV_NAME="base-env"
ARG MAINTAINER_EMAIL="eng.abdelrahman.ahmad@gmail.com"

# Set environment variables
ENV TZ="Africa/Cairo" \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# -----------------------------------------------------------------------------
# Install system dependencies and DVC (from apt repository)
# -----------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tree htop sudo wget gdb nano unzip ffmpeg libsm6 libxext6 \
    python3 python3-pip python3-dev manpages-dev build-essential openssh-client git \
    pkg-config libglvnd0 libgl1 libglx0 libegl1 libgles2 \
    libglvnd-dev libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev \
    cmake curl ca-certificates tar file \
    libosmesa6 libosmesa6-dev freeglut3-dev && \
    # Install DVC via its apt repository
    mkdir -p /etc/apt/keyrings && \
    wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor -o /etc/apt/keyrings/packages.iterative.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.iterative.gpg] https://dvc.org/deb/ stable main" \
    | tee /etc/apt/sources.list.d/dvc.list && \
    chmod 644 /etc/apt/keyrings/packages.iterative.gpg /etc/apt/sources.list.d/dvc.list && \
    apt-get update && \
    apt-get install -y dvc && \
    rm -rf /var/lib/apt/lists/* && \
    apt autoremove -y

# -----------------------------------------------------------------------------
# Create and configure a non‑root user
# -----------------------------------------------------------------------------
RUN set -eux; \
    # Remove existing conflicting users/groups
    { [ "$(id -u ubuntu 2>/dev/null)" = "1000" ] && userdel -r ubuntu || true; }; \
    { getent passwd 1000 && userdel -r $(getent passwd 1000 | cut -d: -f1) || true; }; \
    { getent group ${USER_GID} && groupdel $(getent group ${USER_GID} | cut -d: -f1) || true; }; \
    # Create user and group
    groupadd -g ${USER_GID} ${USERNAME}; \
    useradd -u ${USER_UID} -g ${USER_GID} -ms /bin/bash ${USERNAME}; \
    # Configure sudo privileges
    usermod -aG sudo ${USERNAME}; \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}; \
    chmod 0440 /etc/sudoers.d/${USERNAME}; \
    # Set password
    echo "${USERNAME}:${USER_PASSWORD}" | chpasswd; \
    # Create home directory structure
    mkdir -p /home/${USERNAME}/.local /home/${USERNAME}/.ssh; \
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}; \
    chmod 700 /home/${USERNAME}/.ssh

# Switch to the non‑root user and set the working directory
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# -----------------------------------------------------------------------------
# Configure Git for the non‑root user
# -----------------------------------------------------------------------------
RUN git config --global user.email "eng.abdelrahman.ahmad@gmail.com" && \
    git config --global user.name "Abdelrahman350" && \
    git config --global init.defaultBranch main

# -----------------------------------------------------------------------------
# Install UV (Python package manager) and set up shell autocompletion in one RUN
# -----------------------------------------------------------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv --version || echo "UV installation failed" && \
    echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc

# Ensure UV binary location is in PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# -----------------------------------------------------------------------------
# Install Pixi (Rust‑based environment manager) and verify installation in one RUN
# -----------------------------------------------------------------------------
# Install Pixi and verify installation, updating PATH inline
RUN curl -fsSL https://pixi.sh/install.sh | bash -s -- -y && \
    export PATH="/home/${USERNAME}/.pixi/bin:${PATH}" && \
    pixi --version || echo "Pixi binary not found or not executable" && \
    echo 'eval "$(pixi completion --shell bash)"' >> ~/.bashrc


# -----------------------------------------------------------------------------
# Install additional Python tools (example: ruff via UV)
# -----------------------------------------------------------------------------
RUN uv tool install ruff@latest

# (Optional) Reset working directory for subsequent build steps
WORKDIR /home/mount

# -----------------------------------------------------------------------------
# Stage 2: Final Stage - Attach frequently changing metadata
# -----------------------------------------------------------------------------
FROM builder AS final

LABEL maintainer="${MAINTAINER_EMAIL}" \
    description="Docker image for Generative AI, Computer Vision and Graphics using PyTorch, DVC, UV, Pixi and Rust (Cargo)" \
    version="1.1"

RUN echo 'case "$-" in' >> /home/${USERNAME}/.bashrc && \
    echo '  *i*)' >> /home/${USERNAME}/.bashrc && \
    echo '    if [ -z "$PIXISHELL_STARTED" ]; then' >> /home/${USERNAME}/.bashrc && \
    echo '      if [ -f "pixi.toml" ]; then' >> /home/${USERNAME}/.bashrc && \
    echo '        export PIXISHELL_STARTED=1' >> /home/${USERNAME}/.bashrc && \
    echo '        echo "Welcome! Starting Pixi shell..."' >> /home/${USERNAME}/.bashrc && \
    echo '        exec pixi shell' >> /home/${USERNAME}/.bashrc && \
    echo '      else' >> /home/${USERNAME}/.bashrc && \
    echo '        echo "No pixi.toml found. Starting regular shell."' >> /home/${USERNAME}/.bashrc && \
    echo '      fi' >> /home/${USERNAME}/.bashrc && \
    echo '    fi ;;' >> /home/${USERNAME}/.bashrc && \
    echo '  *) ;;' >> /home/${USERNAME}/.bashrc && \
    echo 'esac' >> /home/${USERNAME}/.bashrc

CMD ["/bin/bash"]
