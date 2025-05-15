#% /bin/bash

#install uv if not installed
if ! command -v uv &> /dev/null
then
    echo "uv could not be found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
else
    echo "uv is already installed"
    uv sync
fi


# create .env file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file"
    touch .env
    echo "EMAIL=" >> .env
    echo "PASSWORD=" >> .env
fi


