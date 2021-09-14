# python class to create redis cache. Simplified for this use case
import sys
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import redis
from config import CACHE_SETTINGS



class RedisCache:
    rconn = redis.Redis(**CACHE_SETTINGS)




if __name__ == '__main__':
    print(RedisCache.rconn.get("hello"))

