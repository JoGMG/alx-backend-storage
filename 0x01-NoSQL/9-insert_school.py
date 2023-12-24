#!/usr/bin/env python3
"""
A Python function that inserts a new document in a
collection based on `kwargs`:

- Prototype: `def insert_school(mongo_collection, **kwargs):`
- `mongo_collection` will be the `pymongo` collection object
- Returns the new `_id`
"""


def insert_school(mongo_collection: object, **kwargs):
    """
    Inserts a new document in a collection.

    Arguments:
        - `mongo_collection`: pymongo collection object
        - `kwargs`: keyword arguments
    """

    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
