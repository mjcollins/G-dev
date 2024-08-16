import subprocess
import shlex
import logging

logging.basicConfig(level=logging.INFO)

def execute_command(command):
    """
    Execute a system command safely without using a shell.

    Parameters:
    - command (str or list): The command to execute. It should be a list of arguments.

    Returns:
    - str: The standard output from the command, or an error message.
    """
    if isinstance(command, str):
        command = shlex.split(command)
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        logging.info(f"Executed command: {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command} with error: {e.stderr}")
        return f"Command failed with error: {e.stderr}"
    except Exception as e:
        logging.error(f"Error executing command {command}: {str(e)}")
        return f"Error executing command: {str(e)}"
