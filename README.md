# Dependency Injection Example with FastAPI

## Karlsruhe Python Meetup 2023-07-12

Simple FastAPI app showcasing dependency injection.

Implements 3 services that can be plugged into the available view functions,
one using a Redis backend, one Postgres and one randomly generated data.

With `docker compose`, the app can be started with either the Redis

    DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml -f docker-compose.redis.yml up

or the Postgres flavor:

    DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml -f docker-compose.postgres.yml up

## License

`di-example-fastapi` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
