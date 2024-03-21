import score_manager
from settings import SCORE_DB
import docker
import subprocess
import os

def judger(filename, user_id):
    host_dir = os.path.abspath('.')
    container_dir = ''
    image_name = 'judge_env'

    client = docker.from_env()
    container = client.containers.run(image_name, detach=True)
    copy_files_to_container(client, host_dir, container_dir, container.id, filename)

    score = run_judger(client, container.id, container_dir)

    container.stop()
    container.remove()

    message = updating_score(user_id, score)

    return score, message

def copy_files_to_container(client, host_dir, container_dir, container_id, filename):
    cmd = ["docker", "cp", filename, f"{container_id}:{container_dir}/evaluate/model.h5"]
    try:
        subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def run_judger(client, container_id, container_dir):
    container = client.containers.get(container_id)
    container.start()
    container.wait()
    output = container.logs()
    output = output.decode('utf-8')
    msg, result = output.split("<flag: score_appear_here>")
    return float(result)

def updating_score(user_id, result):
    score_updating = score_manager.ScoreManager(SCORE_DB)
    message = score_updating.add_score(user_id, result)
    return message

if __name__ == '__main__':
    print('tensorflow_judger: This file should not be __main__.')
