#!/usr/bin/env python3
# podman_controller.py
# A Python script to demonstrate controlling Podman containers.
#
# ---------------------------------------------------------------------------
#
# SETUP (Do this in your terminal before running the script):
#
# 1. Install Podman:
#    - On Fedora/CentOS/RHEL: sudo dnf install podman
#    - On Debian/Ubuntu: sudo apt-get install podman
#    - On macOS (with Homebrew): brew install podman
#
# 2. Enable the Podman API Service:
#    The Podman service provides the Docker-compatible REST API. You need to
#    enable and start the user-specific socket for this to work.
#
#    systemctl --user enable --now podman.socket
#
#    To verify it's running:
#    systemctl --user status podman.socket
#    (You should see 'active (listening)')
#
# 3. Install the Python Docker Library:
#    This library can talk to any Docker-compatible API, including Podman's.
#
#    pip install docker
#
# ---------------------------------------------------------------------------

import docker
import os

def get_podman_socket_path():
    """Constructs the default path for the rootless Podman socket."""
    # The socket path is typically in the user's runtime directory.
    # The XDG_RUNTIME_DIR environment variable points to this directory.
    xdg_runtime_dir = os.environ.get('XDG_RUNTIME_DIR')
    if not xdg_runtime_dir:
        # Fallback for systems where XDG_RUNTIME_DIR might not be set.
        # It constructs the path using the user's ID (UID).
        uid = os.getuid()
        xdg_runtime_dir = f"/run/user/{uid}"

    return f"{xdg_runtime_dir}/podman/podman.sock"

def main():
    """
    Main function to demonstrate Podman operations using the Python SDK.
    """
    print("--- Podman Python Controller ---")

    # Construct the DOCKER_HOST URL for the Podman socket
    socket_path = get_podman_socket_path()
    podman_socket_url = f"unix://{socket_path}"

    print(f"Attempting to connect to Podman service at: {podman_socket_url}")

    try:
        # Initialize the client, pointing it to the Podman socket
        client = docker.DockerClient(base_url=podman_socket_url)

        # Ping the server to check the connection
        if not client.ping():
            print("\nError: Could not connect to the Podman service.")
            print("Please ensure the podman socket is running with:")
            print("  'systemctl --user enable --now podman.socket'")
            return
        
        print("Successfully connected to the Podman service!")

    except Exception as e:
        print(f"\nAn error occurred while connecting to Podman: {e}")
        print("Please ensure the podman socket is enabled and you have correct permissions.")
        return

    # Define the image we want to use
    image_name = "docker.io/library/hello-world"
    container_name = "python-podman-test"
    container = None

    try:
        # --- 1. Pull an image ---
        print(f"\n1. Pulling image: '{image_name}'...")
        try:
            client.images.pull(image_name)
            print("Image pulled successfully.")
        except docker.errors.ImageNotFound:
            print(f"Error: Image '{image_name}' not found.")
            return

        # --- 2. List images ---
        print("\n2. Listing available images (showing first 5):")
        images = client.images.list()
        if not images:
            print("  No images found.")
        for img in images[:5]:
            # Some images have multiple tags, we'll show the first one
            tag = img.tags[0] if img.tags else "[No Tag]"
            print(f"  - {tag} (ID: {img.short_id})")

        # --- 3. Run a container ---
        print(f"\n3. Running a container named '{container_name}' from '{image_name}'...")
        # 'run' is a convenience method that creates and starts the container.
        # 'detach=True' runs the container in the background.
        container = client.containers.run(image_name, detach=True, name=container_name)
        print(f"  Container '{container.name}' started with ID: {container.short_id}")

        # --- 4. List running containers ---
        print("\n4. Listing currently running containers:")
        running_containers = client.containers.list()
        if not running_containers:
            print("  No containers are currently running.")
        for c in running_containers:
            print(f"  - {c.name} (ID: {c.short_id}, Status: {c.status})")

        # --- 5. Inspect container logs ---
        print(f"\n5. Fetching logs for container '{container.name}':")
        # The container runs, prints its message, and exits.
        # We need to wait for it to finish to get the logs.
        container.wait()
        logs = container.logs().decode('utf-8').strip()
        print("--- LOGS START ---")
        print(logs)
        print("--- LOGS END ---")


    except docker.errors.ContainerError as e:
        print(f"\nA container error occurred: {e}")
    except docker.errors.APIError as e:
        print(f"\nAn API error occurred: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    finally:
        # --- 6. Cleanup: Stop and remove the container ---
        print("\n6. Cleaning up...")
        # Check if the container was created before trying to remove it
        if container:
            try:
                # Refresh the container object to get the latest state
                container_to_remove = client.containers.get(container.id)
                print(f"  Stopping and removing container '{container_to_remove.name}'...")
                # The container might have already stopped, so we use a try-except block
                try:
                    container_to_remove.stop()
                except docker.errors.APIError:
                    # This can happen if the container already exited, which is expected for hello-world
                    print("  Container had already stopped.")
                
                container_to_remove.remove()
                print("  Cleanup complete.")
            except docker.errors.NotFound:
                print(f"  Container '{container.name}' was already removed.")
            except Exception as e:
                print(f"  An error occurred during cleanup: {e}")
        else:
             # If a container was not created (e.g. image pull failed), we may need to clean up
             # any container with the same name from a previous failed run.
            try:
                stale_container = client.containers.get(container_name)
                print(f"  Found and removing stale container: '{stale_container.name}'")
                stale_container.remove(force=True)
                print("  Stale container removed.")
            except docker.errors.NotFound:
                # This is the expected state if no container was created
                pass 
            except Exception as e:
                print(f"  An error occurred during stale container cleanup: {e}")
                
        print("\n--- Script Finished ---")


if __name__ == "__main__":
    main()

