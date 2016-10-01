from Collectors import AvgCollector, SumCollector, LastCollector, HistoCollector, Collectors
from ondd_ipc.ipc import ONDDClient
from IntervalTimer import IntervalTimer
from time import sleep

class TelemetryClient:

    default_items = { 
        'ser': AvgCollector, 
        'freq_offset': AvgCollector,
        'snr': AvgCollector, 
        'freq': AvgCollector, 
        'has_lock': HistoCollector, 
        'alg_pk_mn': AvgCollector, 
        'crc_err': LastCollector,
        'crc_ok': LastCollector,
        'state': HistoCollector,
        'set_rs': AvgCollector,
        'rssi': AvgCollector,
        'count': SumCollector,
        'version': LastCollector
    }

    fixed_values = {
        'count': 1,
        'version': 1
    }

    def __init__(self, uplink, src_config, dest_config, items=None):
        self.uplink = uplink
        self.src_config = src_config
        self.dest_config = dest_config

        self.items = TelemetryClient.default_items
        if items is not None:
            self.items = items
        self.collectors = Collectors(self.items)

        self.onddclient = ONDDClient(src_config["endpoint"])
        self.ondd_thread = None
        self.uplink_thread = None

    def ondd_worker(self):
        values = self.onddclient.get_status()
        values.update(TelemetryClient.fixed_values)
        self.collectors.update(values)               

    def uplink_worker(self):
        if not self.ondd_thread or not self.ondd_thread.isAlive():
            self.ondd_thread = IntervalTimer(int(self.src_config["interval"]), self.ondd_worker)
            self.ondd_thread.start()

        self.ondd_thread.pause()
        values = self.collectors.get()
        self.uplink.submit(values)
        self.ondd_thread.unpause()

    def start(self):
        while True:
            if not self.uplink_thread or not self.uplink_thread.isAlive():
                self.uplink_thread = IntervalTimer(int(self.dest_config["interval"]), self.uplink_worker)
                self.uplink_thread.start()
            sleep(10)

