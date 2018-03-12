from .runtime import Runtime
from .policy import Partition

# class Publisher:
#     def __init__(self, dp, partition):
#         self.rt = Runtime.get_runtime()
#         self.dp = dp
#         self.partition = partition
#         if partition is None:
#             self.handle = self.rt.stublib.s_create_pub(self.dp.handle)
#         else:
#             self.handle = self.rt.stublib.s_create_pub_wp(self.dp.handle, partition.encode())
#
#         assert (self.handle > 0)

class Publisher:
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

        self.handle = self.rt.ddslib.dds_create_publisher(self.dp.handle, qos, None)
        assert (self.handle > 0)
