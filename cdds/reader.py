from .dds_binding import *
import jsonpickle
from .runtime import Runtime

@LIVELINESS_CHANGED_PROTO
def trampoline_on_liveliness_changed(r, s, a):
    # print("[python-cdds]:>>  Dispatching Liveliness change")
    Runtime.dispatch_liveliness_changed_listener(r, s)

@DATA_AVAILABLE_PROTO
def trampoline_on_data_available(r, a):
    # print("[python-cdds]:>>  Dispatching Data Available ")
    Runtime.dispatch_data_listener(r)

@SUBSCRIPTION_MATCHED_PROTO
def trampoline_on_subscription_matched(e, s, a):
    # print("[python-cdds]:>>  Dispatching Subscription Match")
    Runtime.dispatch_subscription_matched_listener(e, s)

@SAMPLE_LOST_PROTO
def trampoline_on_sample_lost(e, s, a):
    # print("[python-cdds]:>>  Dispatching Sample Lost")
    global logger
    logger.debug('DefaultListener', '>> Sample Lost')


def do_nothing(a):
    return a


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




class FlexyReader:
    def __init__(self, sub, flexy_topic, flexy_data_listener=None, ps=None):
        self.rt = Runtime.get_runtime()
        self.dp = sub.dp
        self.sub = sub
        self.flexy_topic = flexy_topic
        if flexy_data_listener is None:
            self.data_listener = do_nothing
        else:
            self.data_listener = flexy_data_listener

        self.qos = self.rt.to_rw_qos(ps)

        self.subsciption_listener = None
        self._liveliness_listener = None

        self.handle = c_void_p()

        topic = self.flexy_topic.topic

        self.listener_handle = self.rt.ddslib.dds_create_listener(None)
        self.rt.ddslib.dds_lset_data_available(self.listener_handle , trampoline_on_data_available)
        self.rt.ddslib.dds_lset_liveliness_changed(self.listener_handle, trampoline_on_liveliness_changed)
        self.rt.ddslib.dds_lset_subscription_matched(self.listener_handle, trampoline_on_subscription_matched)

        self.handle = self.rt.ddslib.dds_create_reader(sub.handle, topic, self.qos, self.listener_handle)
        assert (self.handle > 0)
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
        return self.rt.ddslib.dds_reader_wait_for_historical_data(self.handle, timeout)


