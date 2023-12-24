#!/usr/bin/env python3
"""
A Python function that returns all students sorted by average score:

- Prototype: `def top_students(mongo_collection):`
- `mongo_collection` will be the `pymongo` collection object
- The top must be ordered
- The average score must be part of each item returns with
  key = `averageScore`
"""


def top_students(mongo_collection):
    """
    Returns all students in a collection sorted by average score.

    Arguments:
        - `mongo_collection`: pymongo collection object
    """

    students = mongo_collection.find({}, {"name": 1, "topics": 1})

    for student in students:
        topic_scores = [topic["score"] for topic in student["topics"]]
        avg_score = sum(topic_scores) / len(topic_scores)
        mongo_collection.update_one(
            {"_id": student["_id"]},
            {"$set": {"averageScore": avg_score}}
        )

    students_list = [doc for doc in mongo_collection.find()]
    sorted_students_list = sorted(students_list, key=lambda x: x["averageScore"], reverse=True)
    return sorted_students_list
