#!/usr/bin/env python3
"""
A Python script that provides some stats about Nginx
logs stored in MongoDB:

- Database: `logs`
- Collection: `nginx`
- Display (same as the example):
    • first line: `x logs` where `x` is the number of
      documents in this collection
    • second line: `Methods`:
    • 5 lines with the number of documents with the `method
      = ["GET", "POST", "PUT", "PATCH", "DELETE"]` in this
      order (see example below - warning: it's a tabulation
      before each line)
    • one line with the number of documents with:
        - `method=GET`
        - `path=/status`
"""
from pymongo import MongoClient


def get_nginx_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB.
    """

    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    total_logs = nginx_collection.count_documents({})

    method_counts = {}
    http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in http_methods:
        method_counts[method] = nginx_collection.count_documents(
            {"method": method})

    status_check_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})

    print("{} logs".format(total_logs))
    print("Methods:")
    for method, count in method_counts.items():
        print("\tmethod {}: {}".format(method, count))
    print("{} status check".format(status_check_count))


if __name__ == '__main__':
    get_nginx_stats()
