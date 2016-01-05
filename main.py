#!/usr/bin/env python

import sys, time
import ConfigParser
from daemon import Daemon
from dnsproxy import DNSProxyServer

class DNSServerDaemon(Daemon):
    def __init__(self, pidfile, dns_server, host):
        Daemon.__init__(self, pidfile,stderr='/tmp/dnsserver.log')
        self.dns_server = dns_server
        self.host = host
        self.port = 53
        self.host_file = '/etc/hosts'

    def run(self):
        dnsserver = DNSProxyServer(dns_server=self.dns_server, host=self.host, port=self.port, hosts_file=self.host_file)
        dnsserver.serve_forever()

def main():
    config = ConfigParser.RawConfigParser()
    config.read('dnsserver.conf')
    host = config.get('GENERAL', 'host')
    dns_server = config.get('GENERAL', 'dns_server')

    daemon = DNSServerDaemon('/tmp/daemon-dns.pid', dns_server, host)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("Starting daemon...")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

if __name__ == "__main__":
    main()
    
