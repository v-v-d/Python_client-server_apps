import subprocess
import threading
import ipaddress
from tabulate import tabulate


class ParallelHostRangePing:
    def __init__(self, from_ip_addr, to_ip_addr):
        self.from_ip_addr = from_ip_addr
        self.to_ip_addr = to_ip_addr
        self._ping_status_list = []
        self._ping_threads = []

    def is_ip_addrs_valid(self):
        valid_types = (ipaddress.IPv4Address, ipaddress.IPv6Address)
        for ip_addr in (self.from_ip_addr, self.to_ip_addr):
            if type(ip_addr) not in valid_types:
                return False
        return True

    def _add_to_ping_status_list(self, ping_status):
        if ping_status not in self._ping_status_list:
            self._ping_status_list.append(ping_status)

    def _host_ping(self, ip_addr):
        is_unreachable = subprocess.call(['ping', str(ip_addr)], shell=True)
        ping_status = {'Unreachable': ip_addr} if is_unreachable else {'Reachable': ip_addr}
        self._add_to_ping_status_list(ping_status)

    def _parallel_ping(self, ip_addrs):
        for idx, ip_addr in enumerate(ip_addrs):
            ping_thread = threading.Thread(target=self._host_ping, args=(ip_addr,), name=f'ping_thread_{idx}')
            ping_thread.start()
            self._ping_threads.append(ping_thread)

    def _get_valid_ip_addrs_positions(self):
        if self.to_ip_addr < self.from_ip_addr:
            self.from_ip_addr, self.to_ip_addr = self.to_ip_addr, self.from_ip_addr

    def get_ip_addrs_list(self):
        if self.is_ip_addrs_valid():
            self._get_valid_ip_addrs_positions()
            return [self.from_ip_addr + i for i in range(int(self.to_ip_addr) - int(self.from_ip_addr) + 1)]

    def _host_range_ping(self):
        self._parallel_ping(self.get_ip_addrs_list())

    def _wait_for_threads_complete(self):
        for ping_thread in self._ping_threads:
            ping_thread.join()

    def print_host_range_ping_tab(self):
        self._host_range_ping()
        self._wait_for_threads_complete()
        print(tabulate(self._ping_status_list, headers='keys'))


if __name__ == '__main__':
    ip_1 = ipaddress.ip_address('10.0.0.5')
    ip_2 = ipaddress.ip_address('10.0.0.1')

    ping_tab = ParallelHostRangePing(ip_1, ip_2)
    ping_tab.print_host_range_ping_tab()
