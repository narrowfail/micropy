"""
Microservice configuration.
"""

# Action array
ACTION_ARRAY_INIT_SIZE = 1000000
ACTION_GROW_FACTOR = 1.5

SCORE_VALUES = [1, 3, 2, 5, 5]  # For actions 1 to N

# Local server configuration
LOCAL_SERVER_DEBUG = True
LOCAL_SERVER_PORT = 8000
LOCAL_SERVER_IP = "0.0.0.0"

# Cassandra settings
CASSANDRA_SUPPORT = True
CASSANDRA_CLUSTER_IPS = ['127.0.0.1', ]
CASSANDRA_KEYSPACE = 'micropy'

# Try to impor local settigs to override
try:
    from local_settings import *
except:
    pass
