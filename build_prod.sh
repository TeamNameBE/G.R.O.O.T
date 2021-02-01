GIT_SSH_COMMAND='ssh -i /home/ubuntu/.ssh/id_rsa_groot -o IdentitiesOnly=yes' git pull

docker-compose up -d --build
docker-compose restart nginx  # Sometimes the connection between nginx and web fails