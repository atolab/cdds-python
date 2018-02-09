from .runtime import Runtime

class Participant:
    def __init__(self, did):
        self.rt = Runtime.get_runtime()
        self.did = did
        self.handle = self.rt.stublib.s_create_participant(did)
        self.dp = self