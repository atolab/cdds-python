__author__ = 'Angelo Corsaro'

from ctypes import *
import os
import jsonpickle
import platform
import logging
import sys
import time

class DDSLogger:
    class __SingletonLogger:
        def __init__(self, file_name=None, debug_flag=False):

            if file_name is None:
                self.log_file = 'pycham.log'
            else:
                self.log_file = file_name

            self.debug_flag = debug_flag

            log_format = '[%(asctime)s] - [%(levelname)s] > %(message)s'
            log_level = logging.DEBUG

            self.logger = logging.getLogger(__name__ + '.pycham')

            self.logger.setLevel(log_level)
            formatter = logging.Formatter(log_format)
            if not debug_flag:
                log_filename = self.log_file
                handler = logging.FileHandler(log_filename)
            else:
                handler = logging.StreamHandler(sys.stdout)

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)



        def info(self, caller, message):
            self.logger.info(str('< %s > %s') % (caller, message))

        def warning(self, caller, message):
            self.logger.warning(str('< %s > %s') % (caller, message))

        def error(self, caller, message):
            self.logger.error(str('< %s > %s') % (caller, message))

        def debug(self, caller, message):
            self.logger.debug(str('< %s > %s') % (caller, message))

    instance = None
    enabled = True

    def __init__(self, file_name=None, debug_flag=False):

        if not DDSLogger.instance:
            DDSLogger.instance = DDSLogger.__SingletonLogger(file_name, debug_flag)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def info(self, caller, message):
        if self.enabled:
            self.instance.info(caller, message)

    def warning(self, caller, message):
        if self.enabled:
            self.instance.warning(caller, message)

    def error(self, caller, message):
        if self.enabled:
            self.instance.error(caller, message)

    def debug(self, caller, message):
        if self.enabled:
            self.instance.debug(caller, message)


logger = DDSLogger()

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
    else:
        return '/usr/local/lib'


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

DDS_State = 0
DDS_Event = 1

def dds_secs(n):
    return n*1000000000

def dds_millis(n):
    return n*1000000

def dds_micros(n):
    return n*1000

def dds_nanos(n):
    return n

class TopicType(object):
    def gen_key(self): None


class Policy:
    def __init__(self, id, kind):
        self.id = id
        self.kind = kind

class Partition(Policy):
    def __init__(self, ps):
        Policy.__init__(self, DDS_PARTITION_QOS_POLICY_ID, None)
        self.partitions = ps


class Reliable(Policy):
    def __init__(self, blocking_time = 0):
        Policy.__init__(self, DDS_RELIABILITY_QOS_POLICY_ID, DDS_RELIABILITY_RELIABLE)
        self.max_blocking_time = blocking_time


class BestEffort(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_RELIABILITY_QOS_POLICY_ID, DDS_RELIABILITY_BEST_EFFORT)
        self.max_blocking_time = 0


class KeepLastHistory(Policy):
    def __init__(self, depth):
        Policy.__init__(self, DDS_HISTORY_QOS_POLICY_ID, DDS_HISTORY_KEEP_LAST)
        self.depth = depth


class KeepAllHistory(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_HISTORY_QOS_POLICY_ID, DDS_HISTORY_KEEP_ALL)
        self.depth = 0


class Volatile(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID, DDS_DURABILITY_VOLATILE)


class TransientLocal(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID, DDS_DURABILITY_TRANSIENT_LOCAL)


class Transient(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID,  DDS_DURABILITY_TRANSIENT)


class Persistent(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID, DDS_DURABILITY_PERSISTENT)


class ExclusiveOwnership(Policy):
    def __init__(self, strength):
        Policy.__init__(self, DDS_OWNERSHIP_QOS_POLICY_ID, DDS_OWNERSHIP_EXCLUSIVE)
        self.strength = strength


class SharedOwnership(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_OWNERSHIP_QOS_POLICY_ID, DDS_OWNERSHIP_SHARED)


class ManualInstanceDispose(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID, None)
        self.auto_dispose = False


class AutoInstanceDispose(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID)
        self.auto_dispose = True


the_runtime = None


def read_samples():
    return c_uint(DDS_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_ANY_VIEW_STATE)


def new_samples():
    return c_uint(DDS_NOT_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_ANY_VIEW_STATE)


def all_samples():
    return c_uint(DDS_ANY_STATE)


def new_instance_samples():
    return c_uint(DDS_NOT_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_NEW_VIEW_STATE)


def not_alive_instance_samples():
    return c_uint(DDS_ANY_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_NOT_ALIVE_NO_WRITERS_INSTANCE_STATE)


#
# Built-in Key-Value type
#

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
                ('absolute_generation_rank', c_uint32),
                ('reception_timestamp', c_int64)]

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


class KeyHolder(object):
    def __init__(self, k):
        self.key = k


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


def trivial_on_liveliness_changed(r, s):
    Runtime.dispatch_liveliness_changed_listener(c_void_p(r), s)

@DATA_AVAILABLE_PROTO
def trivial_on_data_available(r, a):
    Runtime.dispatch_data_listener(r)


def trivial_on_subscription_matched(e, s):
    Runtime.dispatch_subscription_matched_listener(e, s)


def trivial_on_sample_lost(e, s):
    global logger
    logger.debug('DefaultListener', '>> Sample Lost')


# class DDSReaderListener(Structure):
#     _fields_ = [("on_requested_deadline_missed", CFUNCTYPE(None, c_void_p, c_void_p)),
#                 ("on_requested_incompatible_qos", CFUNCTYPE(None, c_void_p, c_void_p)),
#                 ("on_sample_rejected", CFUNCTYPE(None, c_void_p, c_void_p)),
#                 ("on_liveliness_changed", CFUNCTYPE(None, c_void_p, c_void_p)),
#                 ("on_data_available", CFUNCTYPE(None, c_void_p)),
#                 ("on_subscription_matched", CFUNCTYPE(None, c_void_p, c_void_p)),
#                 ("on_sample_lost", CFUNCTYPE(None, c_void_p, c_void_p))]


class Participant:
    def __init__(self, did):
        global the_runtime
        self.rt = the_runtime
        self.did = did
        self.handle = self.rt.stublib.s_create_participant(did)
        self.dp = self


class Publisher:
    def __init__(self, dp, partition):
        global the_runtime
        self.rt = the_runtime
        self.dp = dp
        self.partition = partition
        if partition is None:
            self.handle = self.rt.stublib.s_create_pub(self.dp.handle)
        else:
            self.handle = self.rt.stublib.s_create_pub_wp(self.dp.handle, partition.encode())

class Subscriber:
    def __init__(self, dp, partition):
        global the_runtime
        self.rt = the_runtime
        self.dp = dp
        self.partition = partition
        if partition is None:
            self.handle = self.rt.stublib.s_create_sub(self.dp.handle)
        else:
            self.handle = self.rt.stublib.s_create_sub_wp(self.dp.handle, partition.encode())



class FlexyTopic:
    def __init__(self, dp, name, keygen=None, qos=None):
        global the_runtime
        self.rt = the_runtime
        if keygen is None:
            self.keygen = lambda x: x.gen_key()
        else:
            self.keygen = keygen

        self.topic = self.rt.stublib.s_create_topic_sksv(dp.handle, name.encode())
        self.type_support = self.rt.get_key_value_type_support()
        self.data_type = DDSKeyValue
        self.dp = dp

    def gen_key(self, s):
        return self.keygen(s)


class Topic:
    def __init__(self, dp, topic_name, type_support, data_type, qos):
        global the_runtime
        self.rt = the_runtime
        self.topic_name = topic_name
        self.type_support = type_support
        self.data_type = data_type
        self.qos = self.rt.to_rw_qos(qos)

        self.handle = c_void_p()
        self.rt.ddslib.dds_create_topic(dp.handle, byref(self.handle), type_support, topic_name.encode(), self.qos, None)


class FlexyWriter:
    def __init__(self, pub, flexy_topic, kind = None):
        global the_runtime
        self.rt = the_runtime
        self.dp = pub.dp
        if (kind is None) or (kind == DDS_State):
            self.handle = self.rt.stublib.s_create_state_writer(pub.handle, flexy_topic.topic)
        else:
            self.handle = self.rt.stublib.s_create_event_writer(pub.handle, flexy_topic.topic)

        self.keygen = flexy_topic.gen_key

    def write(self, s):
        gk = self.keygen(s)
        kh = KeyHolder(gk)
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        self.rt.stublib.s_write_key_value(self.handle, key.encode(), value.encode())

    def write_all(self, xs):
        for x in xs:
            self.write(x)

    def dispose_instance(self, s):
        gk = self.keygen(s)
        kh = KeyHolder(gk)
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        x = DDSKeyValue(key.encode(), value.encode())
        self.rt.ddslib.dds_dispose(self.handle, byref(x))




# The current waitset implementation has the limitation that can wait
# on a single condition.
class WaitSet(object):
    def __init__(self, dp, condition):
        global the_runtime
        self.rt = the_runtime
        self.handle = c_void_p(self.rt.ddslib.dds_create_waitset(dp.handle))
        self.condition = condition
        self.rt.ddslib.dds_waitset_attach(self.handle, self.condition, None)

    def close(self):
        self.rt.ddslib.dds_waitset_detach(self.handle, self.condition)
        self.rt.ddslib.dds_delete(self.handle)

    def wait(self, timeout):
        # we only have one condition
        cs = (c_void_p * 1)()
        pcs = cast(cs, c_void_p)
        s = self.rt.ddslib.dds_waitset_wait(self.handle, byref(pcs), 1, timeout)
        if s == 0:
            return False
        else:
            return True


def do_nothing(a):
    return a


class FlexyReader:
    def __init__(self, sub, flexy_topic, flexy_data_listener = None, kind = None):
        global the_runtime
        self.rt = the_runtime
        self.dp = sub.dp
        self.sub = sub
        self.flexy_topic = flexy_topic
        if flexy_data_listener is None:
            self.data_listener = do_nothing
        else:
            self.data_listener = flexy_data_listener

        self.subsciption_listener = None
        self._liveliness_listener = None

        self.handle = c_void_p()

        topic = self.flexy_topic.topic

        if kind is None or kind == DDS_State:
            # self.handle = self.rt.stublib.s_create_state_reader(sub.handle, topic) # , callback)
            self.handle = self.rt.stublib.s_create_state_reader_wl(sub.handle, topic, trivial_on_data_available)
        else:
            # self.handle = self.rt.stublib.s_create_state_reader(sub.handle, topic) #, callback)
            self.handle = self.rt.stublib.s_create_event_reader_wl(sub.handle, topic, trivial_on_data_available)

        self.rt.register_data_listener(self.handle, self.__handle_data)



    def on_data_available(self, fun):
        self.data_listener = fun

    def on_subscription_matched(self, fun):
        self.subsciption_listener = fun
        self.rt.register_subscription_matched_listener(self.handle, self.__handle_sub_matched)

    def on_liveliness_changed(self, fun):
        self._liveliness_listener = fun
        self.rt.register_liveliness_changed_listener(self.handle, self.__handle_liveliness_change)

    def __handle_data(self, r):
        self.data_listener(self)

    def __handle_sub_matched(self, r, s):
        self.subsciption_listener(self, s)

    def __handle_liveliness_change(self, r, s):
        self._liveliness_listener(self, s)

    def wait_for_data(self, selector, timeout):
        condition = c_void_p(self.rt.ddslib.dds_create_readcondition(self.handle, selector))
        ws = WaitSet(self.dp, condition)
        r = ws.wait(timeout)
        ws.close()
        return r

    # sread is the synchronous read, that means this blocks until some data is received
    def sread(self, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.read(selector)
        else:
            return []

    def read(self, selector):
        return self.read_n(MAX_SAMPLES, selector)

    def sread_n(self, n, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.read_n(n, selector)
        else:
            return []

    def read_n(self, n, sample_selector):
        ivec = (SampleInfo * n)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * n)()

        nr = self.rt.ddslib.dds_read_mask_wl(self.handle, samples, infos, n, sample_selector)

        data = []
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(self.flexy_topic.data_type))
            if infos[i].valid_data:
                v = sp[0].value.decode(encoding='UTF-8')
                data.append(jsonpickle.decode(v))
            else:
                kh = jsonpickle.decode(sp[0].key.decode(encoding='UTF-8'))
                data.append(kh)

        self.rt.ddslib.dds_return_loan(self.handle, samples, nr)

        return zip(data, infos)

    def stake(self, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.take(selector)
        else:
            return []

    def take(self, selector):
        return self.take_n(MAX_SAMPLES, selector)

    def stake_n(self, n, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.take_n(n, selector)
        else:
            return []

    def take_n(self, n, sample_selector):
        ivec = (SampleInfo * n)()
        infos = cast(ivec, POINTER(SampleInfo))

        SampleVec_t = c_void_p * n
        samples = SampleVec_t()
        nr = self.rt.ddslib.dds_take_mask_wl(self.handle, samples, infos, n, sample_selector)
        data = []

        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(self.flexy_topic.data_type))
            if infos[i].valid_data:
                v = sp[0].value.decode(encoding='UTF-8')
                data.append(jsonpickle.decode(v))
            else:
                kh = jsonpickle.decode(sp[0].key.decode(encoding='UTF-8'))
                data.append(kh)

        self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        return zip(data, infos)

    def wait_history(self, timeout):
        return the_runtime.ddslib.dds_reader_wait_for_historical_data(self.handle, timeout)


class Error(Exception):
    pass


class Runtime:
    @staticmethod
    def get_runtime():
        global the_runtime
        if the_runtime is not None:
            return the_runtime
        else:
            the_runtime = Runtime()
            return the_runtime

    def __init__(self):
        self.dataListenerMap = {}
        self.subscriptionMatchedListenerMap = {}
        self.livelinessChangeListenerMap = {}

        self.ddslib = CDLL(cham_lib_path)
        self.stublib = CDLL(bit_lib_path)

        self.kv_topic = None
        self.v_topic = None



        # self.ddslib.dds_qos_create.restype = c_void_p
        # self.ddslib.dds_qos_create.argtypes = []


        ### Stub API

        # dds_entity_t s_create_participant(int id)
        self.stublib.s_create_participant.restype = c_void_p
        self.stublib.s_create_participant.argtypes = [c_int]

        # dds_entity_t s_create_topic_sksv(dds_entity_t dp, const char * name);
        self.stublib.s_create_topic_sksv.restype = c_void_p
        self.stublib.s_create_topic_sksv.argtypes = [c_void_p, c_char_p]

        # dds_entity_t s_create_topic_sv(dds_entity_t dp, const char * name);
        self.stublib.s_create_topic_sv.restype = c_void_p
        self.stublib.s_create_topic_sv.argtypes = [c_void_p, c_char_p]

        # dds_entity_t s_create_pub(dds_entity_t dp);
        self.stublib.s_create_pub.restype = c_void_p
        self.stublib.s_create_pub.argtypes = [c_void_p]

        # dds_entity_t s_create_sub(dds_entity_t dp);
        self.stublib.s_create_sub.restype = c_void_p
        self.stublib.s_create_sub.argtypes = [c_void_p]

        # dds_entity_t s_create_pub_wp(dds_entity_t dp, const char * partition);
        self.stublib.s_create_pub.restype = c_void_p
        self.stublib.s_create_pub.argtypes = [c_void_p, c_char_p]

        # dds_entity_t s_create_sub_wp(dds_entity_t dp, const char * partition);
        self.stublib.s_create_sub_wp.restype = c_void_p
        self.stublib.s_create_sub_wp.argtypes = [c_void_p, c_char_p]

        # dds_entity_t s_create_state_reader(dds_entity_t  s, dds_entity_t  t);
        self.stublib.s_create_state_reader.restype = c_void_p
        self.stublib.s_create_state_reader.argtypes = [c_void_p, c_void_p]

        # dds_entity_t s_create_event_reader(dds_entity_t  s, dds_entity_t t);
        self.stublib.s_create_event_reader.restype = c_void_p
        self.stublib.s_create_event_reader.argtypes = [c_void_p, c_void_p]

        # dds_entity_t s_create_state_reader_wl(dds_entity_t s, dds_entity_t t, dds_on_data_available_fn f);
        self.stublib.s_create_state_reader_wl.restype = c_void_p
        self.stublib.s_create_state_reader_wl.argtypes = [c_void_p, c_void_p, DATA_AVAILABLE_PROTO]

        # dds_entity_t s_create_event_reader_wl(dds_entity_t s, dds_entity_t t, dds_on_data_available_fn f);
        self.stublib.s_create_state_reader_wl.restype = c_void_p
        self.stublib.s_create_state_reader_wl.argtypes = [c_void_p, c_void_p, DATA_AVAILABLE_PROTO]

        # dds_entity_t s_create_state_writer(dds_entity_t  s, dds_entity_t  t);
        self.stublib.s_create_state_writer.restype = c_void_p
        self.stublib.s_create_state_writer.argtypes = [c_void_p, c_void_p]

        # dds_entity_t s_create_event_writer(dds_entity_t  s, dds_entity_t t);
        self.stublib.s_create_event_writer.restype = c_void_p
        self.stublib.s_create_event_writer.argtypes = [c_void_p, c_void_p]


        # int s_write_sksv(dds_entity_t w, const dds_bit_SKeySValue * v);
        self.stublib.s_write_sksv.restype = c_int
        self.stublib.s_write_sksv.argtypes = [c_void_p, POINTER(DDSKeyValue)]

        # int s_write_sv(dds_entity_t  w, const dds_bit_SValue * v);
        self.stublib.s_write_sv.restype = c_int
        self.stublib.s_write_sv.argtypes = [c_void_p, POINTER(DDSValue)]

        # int s_write_key_value(dds_entity_t w, const char * key, const char * value);
        self.stublib.s_write_key_value.restype = c_int
        self.stublib.s_write_key_value.argtypes = [c_void_p, c_char_p, c_char_p]

        # int s_write_value(dds_entity_t w, const char * value);
        self.stublib.s_write_value.restype = c_int
        self.stublib.s_write_value.argtypes = [c_void_p, c_char_p]

        # dds_bit_SKeySValue * s_take_sksv(dds_entity_t r);
        self.stublib.s_take_sksv.restype = POINTER(DDSKeyValue)
        self.stublib.s_take_sksv.argtypes = [c_void_p]

        # int s_take_sksv_a(dds_entity_t r, dds_bit_SKeySValue * sample);
        self.stublib.s_take_sksv_a.restype = c_int
        self.stublib.s_take_sksv_a.argtypes = [c_void_p, POINTER(DDSKeyValue)]

        # dds_bit_SValue * s_take_sv(dds_entity_t r);
        self.stublib.s_take_sv.restype = POINTER(DDSKeyValue)
        self.stublib.s_take_sv.argtypes = [c_void_p]

        # Chameleon has changed the listener API.
        # self.on_requested_deadline_missed = REQUESTED_DEADLINE_MISSED_PROTO(trivial_on_requested_deadline_missed)
        # self.on_requested_incompatible_qos = REQUESTED_INCOMPATIBLE_QOS_PROTO(trivial_on_requested_incompatible_qos)
        # self.on_sample_rejected = SAMPLE_REJECTED_PROTO(trivial_on_sample_rejected)
        # self.on_liveliness_changed = LIVELINESS_CHANGED_PROTO(trivial_on_liveliness_changed)
        # self.on_data_available = DATA_AVAILABLE_PROTO(trivial_on_data_available)
        # self.on_subscription_matched = SUBSCRIPTION_MATCHED_PROTO(trivial_on_subscription_matched)
        # self.on_sample_lost = SAMPLE_LOST_PROTO(trivial_on_sample_lost)

        # -- QoS operations --
        self.ddslib.dds_qos_create.restype = c_void_p
        self.ddslib.dds_qos_create.argtypes = []

        self.ddslib.dds_qos_delete.restype = None
        self.ddslib.dds_qos_delete.argtypes = [c_void_p]

        self.ddslib.dds_qset_durability.restype = None
        self.ddslib.dds_qset_durability.argtypes = [c_void_p, c_uint32]

        self.ddslib.dds_qset_history.restype = None
        self.ddslib.dds_qset_history.argtypes = [c_void_p, c_uint32, c_uint32]

        self.ddslib.dds_qset_reliability.restype = None
        self.ddslib.dds_qset_reliability.argtypes = [c_void_p, c_uint32, c_uint64]

        self.ddslib.dds_qset_ownership.restype = None
        self.ddslib.dds_qset_ownership.argtypes = [c_void_p, c_uint32]

        self.ddslib.dds_qset_ownership_strength.restype = None
        self.ddslib.dds_qset_ownership_strength.restype = None
        self.ddslib.dds_qset_ownership_strength.argtypes = [c_void_p, c_uint32]

        # -- read / take --
        self.ddslib.dds_read_mask.restype = c_int
        self.ddslib.dds_read_mask.argtypes = [c_void_p, POINTER(c_void_p), POINTER(SampleInfo), c_size_t, c_uint32, c_uint32]

        self.ddslib.dds_take_mask.restype = c_int
        self.ddslib.dds_take_mask.argtypes = [c_void_p, POINTER(c_void_p), POINTER(SampleInfo), c_size_t, c_uint32,
                                              c_uint32]

        # -- read / take with loan--
        self.ddslib.dds_read_mask_wl.restype = c_int
        self.ddslib.dds_read_mask_wl.argtypes = [c_void_p, POINTER(c_void_p), POINTER(SampleInfo), c_uint32, c_uint32]

        self.ddslib.dds_take_mask_wl.restype = c_int
        self.ddslib.dds_take_mask_wl.argtypes = [c_void_p, POINTER(c_void_p), POINTER(SampleInfo), c_uint32, c_uint32]

        self.ddslib.dds_return_loan.restype = c_int
        self.ddslib.dds_return_loan.argtypes = [c_void_p, POINTER(c_void_p), c_size_t]

        # -- dispoase --

        self.ddslib.dds_dispose.restype = c_uint
        self.ddslib.dds_dispose.argtypes = [c_void_p, c_void_p]

        self.ddslib.dds_write.restype = c_uint
        self.ddslib.dds_write.argtypes = [c_void_p, c_void_p]

        # DDS Entity Delete
        self.ddslib.dds_delete.restype = c_uint
        self.ddslib.dds_delete.argtypes = [c_void_p]

        # -- Waitset Operations --
        # create
        self.ddslib.dds_create_waitset.restype = c_void_p
        self.ddslib.dds_create_waitset.argtypes = [c_void_p]


        # attach / detach
        self.ddslib.dds_waitset_attach.restype = c_int
        self.ddslib.dds_waitset_attach.argtypes = [c_void_p, c_void_p, c_void_p]
        self.ddslib.dds_waitset_detach.restype = c_int
        self.ddslib.dds_waitset_detach.argtypes = [c_void_p, c_void_p]

        # wait
        self.ddslib.dds_waitset_wait.restype = c_int
        self.ddslib.dds_waitset_wait.argtypes = [c_void_p, POINTER(c_void_p), c_int, c_int64]

        # -- Condition Operations --
        self.ddslib.dds_create_readcondition.restype = c_void_p
        self.ddslib.dds_create_readcondition.argtypes = [c_void_p, c_uint32]


        global the_runtime
        the_runtime = self

    def register_data_listener(self, handle, fun):
        h = repr(handle)
        self.dataListenerMap[h] = fun

    def register_liveliness_changed_listener(self, handle, fun):
        h = repr(handle)
        self.livelinessChangeListenerMap[h] = fun

    def register_subscription_matched_listener(self, handle, fun):
        h = repr(handle)
        self.subscriptionMatchedListenerMap[h] = fun

    @staticmethod
    def dispatch_data_listener(handle):
        h = repr(handle)
        global the_runtime
        if h in the_runtime.dataListenerMap:
            fun = the_runtime.dataListenerMap[h]
            fun(handle)
        else:
            global logger
            logger.warning('DDSRuntime', 'Trying to dispatch listener for unknown reader {0}'.format(handle))

    @staticmethod
    def dispatch_subscription_matched_listener(handle, s):
        h = repr(handle)
        global the_runtime
        if h in the_runtime.subscriptionMatchedListenerMap:
            fun = the_runtime.subscriptionMatchedListenerMap[h]
            fun(handle, s)

    @staticmethod
    def dispatch_liveliness_changed_listener(handle, s):
        h = repr(handle)
        global the_runtime
        if h in the_runtime.livelinessChangeListenerMap:
            fun = the_runtime.livelinessChangeListenerMap[h]
            fun(handle, s)

    def get_key_value_type_support(self):
        return self.stublib.dds_bit_SKeySValue_desc

    def get_simple_value_type_support(self):
        return self.stublib.dds_bit_SValue_desc

    def to_rw_qos(self, ps):
        if ps is None:
            return None

        qos = self.create_dds_qos()

        for p in ps:
            if p.id == DDS_DURABILITY_QOS_POLICY_ID:
                self.ddslib.dds_qset_durability(qos, p.kind)
            elif p.id == DDS_HISTORY_QOS_POLICY_ID:
                self.ddslib.dds_qset_history(qos, p.kind, p.depth)
            elif p.id == DDS_RELIABILITY_QOS_POLICY_ID:
                self.ddslib.dds_qset_reliability(qos, p.kind, p.max_blocking_time)
            elif p.id == DDS_OWNERSHIP_QOS_POLICY_ID:
                self.ddslib.dds_qset_ownership(qos, p.kind)
                if p.kind == DDS_OWNERSHIP_EXCLUSIVE:
                    self.ddslib.dds_qset_ownership_strength(qos, p.strength)
            elif p.id == DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID:
                self.ddslib.dds_qset_writer_data_lifecycle(qos, p.auto_dispose)
        return qos


    def to_ps_qos(self, ps):
        if ps is None:
            return None

        qos = self.create_dds_qos()
        xs = list(filter(lambda p: p.id == DDS_PARTITION_QOS_POLICY_ID, ps))

        if len(xs) > 0:
            policy = xs[0]
            L = len(policy.partitions)
            vec = (c_char_p * L)()
            sbuf = list(map(lambda s: s.encode(), policy.partitions))
            vec[:] = sbuf
            self.ddslib.dds_qset_partition(qos, c_uint32(L), vec)
        return qos

    def create_dds_qos(self):
        return c_void_p(self.ddslib.dds_qos_create())

    def release_dds_qos(self, qos):
        self.ddslib.dds_qos_delete(qos)

    def close(self):
        self.ddslib.dds_fini()
