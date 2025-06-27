import docker
import time
import logging
import atexit
import sys

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Docker client initialization
# This will try to connect to the Docker daemon using environment variables or default socket
try:
    client = docker.from_env()
    client.ping() # Test connection to Docker daemon
    logging.info("Successfully connected to Docker daemon.")
except docker.errors.DockerException as e:
    logging.error(f"Could not connect to Docker daemon: {e}")
    logging.error("Please ensure Docker is running and accessible.")
    sys.exit(1)

# List to hold references to launched containers
launched_containers = []

# --- Configuration for your containers ---
# Each dictionary defines a container: name, image, and the command it runs.
# 'sleep infinity' ensures the container runs indefinitely until stopped.
CONTAINER_SPECS = [
    {"name": "my-app-container-1", "image": "alpine/git", "command": ["sleep", "infinity"]},
    {"name": "my-app-container-2", "image": "alpine/git", "command": ["sleep", "infinity"]},
    {"name": "my-app-container-3", "image": "alpine/git", "command": ["sleep", "infinity"]},
]

# Monitoring interval in seconds
MONITOR_INTERVAL_SECONDS = 5

def launch_containers():
    """
    Launches Docker containers based on the CONTAINER_SPECS.
    Stores references to running containers in 'launched_containers' list.
    """
    logging.info("Attempting to launch containers...")
    for spec in CONTAINER_SPECS:
        name = spec["name"]
        image = spec["image"]
        command = spec["command"]

        # First, try to remove any existing container with the same name
        try:
            existing_container = client.containers.get(name)
            if existing_container:
                logging.warning(f"Existing container '{name}' found. Stopping and removing it.")
                existing_container.stop()
                existing_container.remove()
        except docker.errors.NotFound:
            pass # No existing container, proceed

        try:
            container = client.containers.run(
                image,
                command,
                name=name,
                detach=True,  # Run in the background
                remove=False  # Do not remove automatically on exit (we'll handle cleanup)
            )
            launched_containers.append(container)
            logging.info(f"Launched container '{name}' (ID: {container.id[:12]}) using image '{image}'. Status: {container.status}")
        except docker.errors.ImageNotFound:
            logging.error(f"Image '{image}' not found for container '{name}'. Please pull it first (e.g., 'docker pull {image}').")
            # If an image is not found, we can't launch this container, but try others.
        except docker.errors.APIError as e:
            logging.error(f"Failed to launch container '{name}': {e}")
            # If there's an API error, it might be a general Docker issue or specific to this container.

def monitor_containers():
    """
    Continuously monitors the status of launched containers.
    Logs warnings if a container is not running.
    """
    logging.info(f"Starting container monitoring (checking every {MONITOR_INTERVAL_SECONDS} seconds)...")
    if not launched_containers:
        logging.warning("No containers were launched to monitor.")
        return

    try:
        while True:
            all_running = True
            for container in launched_containers:
                try:
                    # Reload the container's status from the Docker daemon
                    container.reload()
                    status = container.status
                    if status == 'running':
                        logging.info(f"Container '{container.name}' (ID: {container.id[:12]}) is RUNNING.")
                    else:
                        logging.error(f"Container '{container.name}' (ID: {container.id[:12]}) is in status: {status}. INVESTIGATE!")
                        all_running = False
                except docker.errors.NotFound:
                    logging.error(f"Container '{container.name}' (ID: {container.id[:12]}) NO LONGER EXISTS. It might have stopped and been removed unexpectedly.")
                    # Remove from list so we don't keep trying to monitor a non-existent container
                    launched_containers.remove(container)
                    all_running = False
                except docker.errors.APIError as e:
                    logging.error(f"API error while monitoring container '{container.name}': {e}")
                    all_running = False

            if not all_running:
                logging.warning("One or more containers are not in 'running' state. Check logs for details.")

            time.sleep(MONITOR_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("Monitoring interrupted by user (Ctrl+C).")
    finally:
        logging.info("Exiting monitoring loop.")


def cleanup_containers():
    """
    Stops and removes all containers that were launched by this script.
    Registered with atexit to ensure cleanup on script exit.
    """
    if launched_containers:
        logging.info("Starting cleanup of launched containers...")
        for container in launched_containers:
            try:
                logging.info(f"Stopping container '{container.name}' (ID: {container.id[:12]})...")
                container.stop(timeout=5) # Give it 5 seconds to stop
                logging.info(f"Removing container '{container.name}' (ID: {container.id[:12]})...")
                container.remove()
                logging.info(f"Container '{container.name}' removed.")
            except docker.errors.NotFound:
                logging.warning(f"Container '{container.name}' (ID: {container.id[:12]}) was already removed or never existed. Skipping cleanup.")
            except docker.errors.APIError as e:
                logging.error(f"Error during cleanup of container '{container.name}': {e}")
        logging.info("All launched containers have been cleaned up.")
    else:
        logging.info("No containers to clean up.")

# Register the cleanup function to be called automatically on script exit
atexit.register(cleanup_containers)

if __name__ == "__main__":
    logging.info("Starting Docker container management script.")
    launch_containers()
    if launched_containers:
        monitor_containers()
    else:
        logging.error("No containers were successfully launched. Monitoring aborted.")
    logging.info("Script finished.")


