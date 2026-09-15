"""
I need to start this first to start with my application


docker run -d --name mail_local -p 1025:1025 -p 8025:8025 axllent/mailpit

docker run -d --name cache_redis_local -p 6379:6379 redis:8.10.0

"""

import subprocess

command = [
    "ls",
    "-a",
]
result = subprocess.run(command)
# print(result)


command = [
    "docker",
    "start",
    "mail_local",
    "cache_redis_local",
]
print("Starting the Docker services.")
result = subprocess.run(command)
# print(result)
