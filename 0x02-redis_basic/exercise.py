#!/usr/bin/env python3
"""
Using the Redis NoSQL database.
"""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """
    Tracks the number of calls of methods in Cache class.

    Argument:
        - `method`: a callable method
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after incrementing its call counter.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs of a method.

    Argument:
        - `method`: a callable method
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Returns method's output after storing its inputs and output.
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(method: Callable) -> None:
    """
    Displays the history of calls of a particular method.

    Argument:
        - `method`: a callable method
    """
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    method_name = method.__qualname__
    in_key = '{}:inputs'.format(method_name)
    out_key = '{}:outputs'.format(method_name)
    method_call_count = 0
    if redis_store.exists(method_name) != 0:
        method_call_count = int(redis_store.get(method_name))
    print('{} was called {} times:'.format(method_name, method_call_count))
    method_inputs = redis_store.lrange(in_key, 0, -1)
    method_outputs = redis_store.lrange(out_key, 0, -1)
    for method_input, method_output in zip(method_inputs, method_outputs):
        print('{}(*{}) -> {}'.format(
            method_name,
            method_input.decode("utf-8"),
            method_output,
        ))


class Cache:
    """
    A class implementing data storage in a Redis database.
    """
    def __init__(self) -> None:
        """
        Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores `data` in Redis database using a random key and returns the key.

        Arguments:
            - `data`: data to store
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str, fn: Callable = None) \
            -> Union[str, bytes, int, float]:
        """
        Retrieves and converts data from Redis database
        to desired format.

        Arguments:
            - `key`: key associated with the data to retrieve
            - `fn`: function which performs the conversion
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves and converts data from Redis database to string.

        Arguments:
            - `key`: key associated with the data to retrieve
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves and converts data from Redis database to integer.

        Arguments:
            - `key`: key associated with the data to retrieve
        """
        return self.get(key, lambda x: int(x))
