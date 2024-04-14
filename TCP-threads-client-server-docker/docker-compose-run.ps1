# Start the Docker Compose services in detached mode
docker-compose up -d

# Get the container IDs
$server_id = docker-compose ps -q server
$client1_id = docker-compose ps -q client1
$client2_id = docker-compose ps -q client2

# Open new terminals and attach to the containers
Start-Process powershell -ArgumentList "docker attach $client1_id"
Start-Process powershell -ArgumentList "docker attach $client2_id"