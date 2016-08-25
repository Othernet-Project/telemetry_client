from os.path import join, normpath, dirname, abspath
import argparse
from ConfigParser import SafeConfigParser
from HttpLink import HttpLink
from TelemetryClient import TelemetryClient

default_config_file = normpath(join(dirname(abspath(__file__)), "telemetry_config.ini"))

def configure():
    parser = argparse.ArgumentParser(description='Outernet Telemetry Client')
    parser.add_argument('--conf', metavar='PATH',
                        help='Path to configuration file',
                        default=default_config_file)
    args, unknown = parser.parse_known_args()
    config_file = args.conf
    parser = SafeConfigParser()
    parser.read(config_file)
    return parser    
        
def main():
    config = configure()
    src_config = dict(config.items("source"))
    uplink_config = dict(config.items("destination"))
    uplink = HttpLink(uplink_config)
    client = TelemetryClient(uplink, src_config, uplink_config)
    client.start()        


if __name__ == '__main__':
    main()

