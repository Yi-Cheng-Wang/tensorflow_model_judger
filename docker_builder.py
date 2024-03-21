import docker
import os

def builder():
    docker_folder_path = 'DOCKER'
    image_name = 'judge_env'
    dockerfile_path = 'DOCKER/Dockerfile'
    built_image = build_docker_image(image_name, dockerfile_path)
    save_image_to_folder(built_image, docker_folder_path, image_name)

def build_docker_image(image_name, dockerfile_path):
    client = docker.from_env()

    abs_dockerfile_path = os.path.abspath(dockerfile_path)

    image, build_logs = client.images.build(
        path=os.path.dirname(abs_dockerfile_path),
        dockerfile=os.path.basename(abs_dockerfile_path),
        tag=image_name
    )

    for log in build_logs:
        if 'stream' in log:
            print(log['stream'], end='')

    return image

def save_image_to_folder(image, folder_path, image_name):
    image_tar_path = os.path.join(folder_path, image_name)
    with open(image_tar_path, 'wb') as f:
        for chunk in image.save():
            f.write(chunk)

if __name__ == '__main__':
    print('docker_builder: This file should not be __main__.')
