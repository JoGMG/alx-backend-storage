#!/usr/bin/env python3
"""
Improve `12-log_stats.py` by adding the top 10 of the most
present IPs in the collection `nginx` of the database `logs`:

- The IPs top must be sorted (descending)
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
    
    sorted_ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$project": {"ip": "$_id", "count": 1, "_id": 0}}
    ])

    print("{} logs".format(total_logs))
    print("Methods:")
    for method, count in method_counts.items():
        print("\tmethod {}: {}".format(method, count))
    print("{} status check".format(status_check_count))
    print("IPs:")
    _count = 0
    for items in sorted_ips:
        if _count == 10:
            break
        print("\t{}: {}".format(items.get('ip'), items.get('count')))
        _count += 1

if __name__ == '__main__':
    get_nginx_stats()
