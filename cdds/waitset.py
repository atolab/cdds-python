from ctypes import *
from .runtime import Runtime

# The current waitset implementation has the limitation that can wait
# on a single condition.
class WaitSet(object):
    def __init__(self, dp, condition):
        self.rt = Runtime.get_runtime()
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