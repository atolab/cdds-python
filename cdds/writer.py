from .runtime import Runtime
from .dds_binding import *
import jsonpickle

class FlexyWriter:
    def __init__(self, pub, flexy_topic, ps = None):
        self.rt = Runtime.get_runtime()
        self.dp = pub.dp
        self.qos = self.rt.to_rw_qos(ps)
        self.handle = self.rt.ddslib.dds_create_writer(pub.handle, flexy_topic.topic, self.qos, None)
        # if (kind is None) or (kind == DDS_State):
        #     self.handle = self.rt.stublib.s_create_state_writer(pub.handle, flexy_topic.topic)
        # else:
        #     self.handle = self.rt.stublib.s_create_event_writer(pub.handle, flexy_topic.topic)

        assert (self.handle > 0)
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


