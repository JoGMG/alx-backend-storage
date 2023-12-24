#!/usr/bin/env python3
"""
A Python function that lists all documents in a collection:

- Prototype: `def list_all(mongo_collection)`:
- Return an empty list if no document in the collection
- `mongo_collection` will be the `pymongo` collection object
"""


def list_all(mongo_collection: object) -> list:
    """
    Lists all documents in a collection.

    Arguments:
        - `mongo_collection`: pymongo collection object
    """

    return [doc for doc in mongo_collection.find()]
