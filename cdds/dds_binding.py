import platform
import os
from ctypes import *


def get_lib_ext():
    system = platform.system()
    if system == 'Linux':
        return '.so'
    elif system == 'Darwin':
        return '.dylib'
    else:
        return '.dll'

def get_user_lib_path():
    system = platform.system()
    if system == 'Linux':
        return '/usr/local/lib'
    elif system == 'Darwin':
        return '/usr/local/lib'
    elif system in ['windows', 'Windows', 'win32']:
        return os.environ['CDDS_HOME']
    else:
        return '/usr/local/lib'


system = platform.system()
if system in ['windows', 'Windows', 'win32']:
    cham_lib = 'ddsc' + get_lib_ext()
    bit_lib = 'ddstubs' + get_lib_ext()
    cham_lib_path = get_user_lib_path() + os.sep + cham_lib
    bit_lib_path = get_user_lib_path() + os.sep + bit_lib
else:
    cham_lib = 'libddsc' + get_lib_ext()
    bit_lib = 'libddstubs' + get_lib_ext()
    cham_lib_path = get_user_lib_path() + os.sep + cham_lib
    bit_lib_path = get_user_lib_path() + os.sep + bit_lib

# Limits and Constants
MAX_SAMPLES = 256


#
#  Statuses
DDS_READ_SAMPLE_STATE = 1
DDS_NOT_READ_SAMPLE_STATE = 2
DDS_ANY_SAMPLE_STATE = DDS_READ_SAMPLE_STATE | DDS_NOT_READ_SAMPLE_STATE
DDS_NEW_VIEW_STATE = 4
DDS_NOT_NEW_VIEW_STATE = 8
DDS_ANY_VIEW_STATE = DDS_NEW_VIEW_STATE | DDS_NOT_NEW_VIEW_STATE

DDS_ALIVE_INSTANCE_STATE = 16
DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE = 32
DDS_NOT_ALIVE_NO_WRITERS_INSTANCE_STATE = 64
DDS_ANY_INSTANCE_STATE =  DDS_ALIVE_INSTANCE_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE | DDS_NOT_ALIVE_NO_WRITERS_INSTANCE_STATE

DDS_ANY_STATE = DDS_ANY_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_ANY_INSTANCE_STATE


DDS_NOT_REJECTED = 0
DDS_REJECTED_BY_INSTANCES_LIMIT = 1
DDS_REJECTED_BY_SAMPLES_LIMIT = 2
DDS_REJECTED_BY_SAMPLES_PER_INSTANCE_LIMIT = 3

#  QoS IDs
DDS_INVALID_QOS_POLICY_ID = 0
DDS_USERDATA_QOS_POLICY_ID = 1
DDS_DURABILITY_QOS_POLICY_ID = 2
DDS_PRESENTATION_QOS_POLICY_ID = 3
DDS_DEADLINE_QOS_POLICY_ID = 4
DDS_LATENCYBUDGET_QOS_POLICY_ID = 5
DDS_OWNERSHIP_QOS_POLICY_ID = 6
DDS_OWNERSHIPSTRENGTH_QOS_POLICY_ID = 7
DDS_LIVELINESS_QOS_POLICY_ID = 8
DDS_TIMEBASEDFILTER_QOS_POLICY_ID = 9
DDS_PARTITION_QOS_POLICY_ID = 10
DDS_RELIABILITY_QOS_POLICY_ID = 11
DDS_DESTINATIONORDER_QOS_POLICY_ID = 12
DDS_HISTORY_QOS_POLICY_ID = 13
DDS_RESOURCELIMITS_QOS_POLICY_ID = 14
DDS_ENTITYFACTORY_QOS_POLICY_ID = 15
DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID = 16
DDS_READERDATALIFECYCLE_QOS_POLICY_ID = 17
DDS_TOPICDATA_QOS_POLICY_ID = 18
DDS_GROUPDATA_QOS_POLICY_ID = 19
DDS_TRANSPORTPRIORITY_QOS_POLICY_ID = 20
DDS_LIFESPAN_QOS_POLICY_ID = 21
DDS_DURABILITYSERVICE_QOS_POLICY_ID = 22

#
# QoS Kinds

# Durability
DDS_DURABILITY_VOLATILE = 0
DDS_DURABILITY_TRANSIENT_LOCAL = 1
DDS_DURABILITY_TRANSIENT = 2
DDS_DURABILITY_PERSISTENT = 3

# History
DDS_HISTORY_KEEP_LAST = 0
DDS_HISTORY_KEEP_ALL = 1

# Ownership
DDS_OWNERSHIP_SHARED = 0
DDS_OWNERSHIP_EXCLUSIVE = 1

# Reliability
DDS_RELIABILITY_BEST_EFFORT = 0
DDS_RELIABILITY_RELIABLE = 1

# Dest Order
DDS_DESTINATIONORDER_BY_RECEPTION_TIMESTAMP = 0
DDS_DESTINATIONORDER_BY_SOURCE_TIMESTAMP = 1

DDS_LIVELINESS_AUTOMATIC = 0
DDS_LIVELINESS_MANUAL_BY_PARTICIPANT = 1
DDS_LIVELINESS_MANUAL_BY_TOPIC = 2

DDS_DESTINATIONORDER_BY_RECEPTION_TIMESTAMP = 0
DDS_DESTINATIONORDER_BY_SOURCE_TIMESTAMP = 1

def dds_secs(n):
    return n*1000000000

def dds_millis(n):
    return n*1000000

def dds_micros(n):
    return n*1000

def dds_nanos(n):
    return n


#
# DDS Sample Info
#
class SampleInfo(Structure):
    _fields_ = [('sample_state', c_uint),
                ('view_state', c_uint),
                ('instance_state', c_uint),
                ('valid_data', c_bool),
                ('source_timestamp', c_int64),
                ('instance_handle', c_uint64),
                ('pubblication_handle', c_uint64),
                ('disposed_generation_count', c_uint32),
                ('no_writer_generation_count', c_uint32),
                ('sample_rank', c_uint32),
                ('generation_rank', c_uint32),
                ('absolute_generation_rank', c_uint32)]

    def is_new_sample(self):
        return self.sample_state == DDS_NOT_READ_SAMPLE_STATE

    def is_read_sample(self):
        return not self.is_new_sample()

    def is_new_instance(self):
        return self.view_state == DDS_NEW_VIEW_STATE

    def is_alive_instance(self):
        return self.instance_state == DDS_ALIVE_INSTANCE_STATE

    def is_disposed_instance(self):
        return self.instance_state == DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE

    def is_not_alive_instance(self):
        return self.instance_state == DDS_NOT_ALIVE_NO_WRITERS_INSTANCE_STATE


dds_entity_t = c_int32
dds_time_t = c_int64
dds_duration_t = c_int64
dds_instance_handle_t = c_int64
dds_domainid_t = c_uint32
dds_sample_state_t = c_int
dds_view_state_t = c_int
dds_instance_state_t = c_int
dds_qos_p_t = c_void_p
dds_attach_t = c_void_p
dds_listener_p_t = c_void_p
dds_topic_descriptor_p_t = c_void_p
dds_return_t = c_int32

REQUESTED_DEADLINE_MISSED_PROTO = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
REQUESTED_INCOMPATIBLE_QOS_PROTO = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
SAMPLE_REJECTED_PROTO = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
LIVELINESS_CHANGED_PROTO = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
DATA_AVAILABLE_PROTO = CFUNCTYPE(None, c_void_p, c_void_p)
SUBSCRIPTION_MATCHED_PROTO = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
SAMPLE_LOST_PROTO = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)




# There are actually used to check the the listener are actually working...

def trivial_on_requested_deadline_missed(r, s):
    global logger
    logger.debug('DefaultListener', '>> Requested Deadline Missed')


def trivial_on_requested_incompatible_qos(r, s):
    global logger
    logger.debug('DefaultListener', '>> Requested Incompatible QoS')


def trivial_on_sample_rejected(r, s):
    global logger
    logger.debug('DefaultListener', '>> Sample Rejected')




class DDSValue(Structure):
    _fields_ = [('value', c_char_p)]


class DDSKeyValue(Structure):
    _fields_ = [('key', c_char_p),
                ('value', c_char_p)]


#
# These types are used for binary payload
#
class DDSSequence(Structure):
    _fields_ = [('_maximum', c_uint32),
                ('_length', c_uint32),
                ('_buffer', c_char_p),
                ('_release', c_bool)]

#
# Built-in key-value type
#
class DDSKeyBValue(Structure):
    _fields_ = [('key', c_char_p),
                ('value', DDSSequence)]


class KeyHolder(object):
    def __init__(self, k):
        self.key = k
