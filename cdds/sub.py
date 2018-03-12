from .runtime import Runtime

class Subscriber:
    def __init__(self, dp, partition):
        self.rt = Runtime.get_runtime()
        self.dp = dp
        self.partition = partition
        if partition is None:
            self.handle = self.rt.stublib.s_create_sub(self.dp.handle)
        else:
            self.handle = self.rt.stublib.s_create_sub_wp(self.dp.handle, partition.encode())

        assert (self.handle  > 0)

