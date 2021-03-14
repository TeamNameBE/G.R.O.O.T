git pull

docker-compose up -d --build
docker-compose restart nginx  # Sometimes the connection between nginx and web fails
