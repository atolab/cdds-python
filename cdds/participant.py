from .runtime import Runtime

class Participant:
    def __init__(self, did):
        self.rt = Runtime.get_runtime()
        self.did = did
        self.handle = self.rt.ddslib.dds_create_participant(did, None, None)
        assert (self.handle > 0)
        self.dp = self
