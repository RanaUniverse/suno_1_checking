"""
app/shared/redis/client.py

Here i will make the client obj to use in many places

i will import this obj in differnet places this will just nothing do else
"""

import redis
from redis.exceptions import RedisError


from app.config import settings

if settings.redis.password:
    password_value = settings.redis.password.get_secret_value()
else:
    password_value = None


if settings.redis.url is not None:
    redis_client = redis.from_url(
        settings.redis.url,
        decode_responses=True,
    )

else:
    id_pass_credential_obj = redis.UsernamePasswordCredentialProvider(
        username=settings.redis.username,
        password=password_value,
    )
    redis_client = redis.Redis(
        host=settings.redis.host,
        db=settings.redis.db,
        port=settings.redis.port,
        decode_responses=True,
        credential_provider=id_pass_credential_obj,
    )


def validate_redis_connection() -> None:
    """
    i will call this at startup so that i will sure Redis will
    connect goodly correctly or not
    """
    print("Redis Connection is Checking with AUTH...")

    try:
        redis_client.ping()  # type: ignore
        print("Redis Connection Has Successfull.")
    except RedisError as e:
        raise RuntimeError(
            "Redis startup check failed now "
            "Check redis url, host, port , username, password"
        ) from e
