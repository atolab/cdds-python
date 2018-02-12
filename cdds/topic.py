from .runtime import Runtime
from .dds_binding import DDSKeyValue

class TopicType(object):
    def gen_key(self): None


class FlexyTopic:
    def __init__(self, dp, name, keygen=None, qos=None):
        self.rt = Runtime.get_runtime()
        if keygen is None:
            self.keygen = lambda x: x.gen_key()
        else:
            self.keygen = keygen

        self.topic = self.rt.stublib.s_create_topic_sksv(dp.handle, name.encode())
        assert (self.topic > 0)
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

