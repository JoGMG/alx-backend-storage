#!/usr/bin/env python3
"""
A Python function that returns the list of school having a specific topic:

- Prototype: `def schools_by_topic(mongo_collection, topic):`
- `mongo_collection` will be the `pymongo` collection object
- `topic` (string) will be topic searched
"""


def schools_by_topic(mongo_collection: object, topic):
    """
    Returns the list of school having a specific topic.

    Arguments:
        - `mongo_collection`: pymongo collection object
        - `topic`: topic to filter by
    """

    topic_filter = {
        'topics': {
            '$in': [topic],
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
