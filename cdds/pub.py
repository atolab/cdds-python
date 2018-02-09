from .runtime import Runtime

class Publisher:
    def __init__(self, dp, partition):
        self.rt = Runtime.get_runtime()
        self.dp = dp
        self.partition = partition
        if partition is None:
            self.handle = self.rt.stublib.s_create_pub(self.dp.handle)
        else:
            self.handle = self.rt.stublib.s_create_pub_wp(self.dp.handle, partition.encode())
