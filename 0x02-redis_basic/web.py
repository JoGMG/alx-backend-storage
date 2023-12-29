#!/usr/bin/env python3
"""
Caches and tracks requests.
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Connects to Redis database
redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    Decorator function to add caching functionality to the `get_page` method.

    Argument:
        - `method`: The decorated function `get_page`.
    """
    @wraps(method)
    def wrapper(url) -> str:
        """
        Wrapper function that checks if the URL is in the Redis cache.
        If it is, it increments the count and returns the cached value.
        If it's not, it calls the `get_page` method to get new data,
        stores this data in the Redis cache with an expiration time of
        10 seconds, and returns it.

        Argument:
            - `url`: The URL to fetch data from.
        """
        # Check if URL is in cache
        if redis_store.exists(url):
            redis_store.incr("count:{}".format(url))  # Increase count
            return redis_store.get(url).decode('utf-8')

        # If URL is not in cache, get new data
        result = method(url)
        # Store the data in cache with an expiration time of 10 seconds
        redis_store.set(url, result, ex=10)
        redis_store.set("count:{}".format(url), 1, ex=10)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a particular URL and returns it.

    Argument:
        - `url`: The URL to fetch data from.
    """
    return requests.get(url).text
