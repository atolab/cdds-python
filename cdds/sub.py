from .runtime import Runtime
from .policy import  Partition

class Subscriber:
    @staticmethod
    def partitions(ps):
        return [Partition(ps)]

    @staticmethod
    def partition(p):
        return [Partition([p])]

    def __init__(self, dp, ps = None):
        self.rt = Runtime.get_runtime()
        self.dp = dp
        qos = None
        if ps is not None:
            qos = self.rt.to_ps_qos(ps)

        self.handle = self.rt.ddslib.dds_create_subscriber(self.dp.handle, qos, None)
        assert (self.handle > 0)
