import sys
import asyncio
from ipaddress import ip_address, IPv4Address, IPv6Address
from itertools import repeat

from tabulate import tabulate


class AsyncPingHosts:
    def __init__(self, addresses: list):
        """
        Initialize cross platform asynchronous host ping machine.
        :param (list) addresses: List of IP addresses.
        """
        self.addresses = addresses
        self.reachable = list()
        self.unreachable = list()

        self._set_addresses_type()

    def _set_addresses_type(self):
        """
        Set addresses type to ipaddress.IPv4Address or ipaddress.IPv6Address
        if addresses argument is list. sys.exit(1) if ValueError exception
        caught.
        """
        try:
            if self._is_addresses_is_list():
                self.addresses = [self._set_address_type(address) for address in self.addresses]
        except ValueError as error:
            print(error)
            sys.exit(1)

    def _is_addresses_is_list(self):
        """
        Validate addresses argument.
        :return (bool) : True if passed addresses argument is list,
        raise ValueError otherwise
        """
        if type(self.addresses) is list:
            return True
        raise ValueError(f'Passed addresses must be a list type. {type(self.addresses)} given.')

    @staticmethod
    def _set_address_type(address):
        """
        Set address type to ipaddress.IPv4Address or ipaddress.IPv6Address
        if it's not yet.
        :param (str, int, IPv4Address, IPv6Address) address: IP address.
        :return (IPv4Address, IPv6Address) : IP address or sys.exit(1)
        if ValueError exception caught.
        """
        if not type(address) in (IPv4Address, IPv6Address):
            try:
                address = ip_address(address)
            except ValueError as error:
                print(error)
                sys.exit(1)
        return address

    def ping_hosts(self):
        """
        Cross platform asynchronous host ping. Push address to
        reachable list if address is reachable and to unreachable
        list otherwise.
        """
        print('Please wait until ping is done. It\'s needed about 5 sec '
              'if all addresses are reachable, about 20 sec or more otherwise, '
              'depending on the passed addresses number.')
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._async_ping())
            loop.close()
        else:
            asyncio.run(self._async_ping())

    async def _async_ping(self):
        """Get tasks and run them concurrently."""
        tasks = (self._ping_host(str(address)) for address in self.addresses)
        await asyncio.gather(*tasks)

    async def _ping_host(self, address):
        """
        Ping host and add it to reachable or unreachable list
        based on return code from subprocess.
        :param (str) address: IP address.
        """
        ping_key = self._get_ping_key()
        proc = await asyncio.create_subprocess_shell(
            f'ping {ping_key} 4 {address}', stdout=asyncio.subprocess.DEVNULL
        )
        await proc.communicate()
        if proc.returncode == 0:
            self.reachable.append(address)
        else:
            self.unreachable.append(address)

    @staticmethod
    def _get_ping_key():
        """
        Get key for ping command which set number of sending
        packets.
        :return:
        """
        key = '-c'
        if sys.platform == 'win32':
            key = '/n'
        return key

    def get_ping_status_table(self):
        """Get table with addresses and their statuses."""
        headers = ['Address', 'Status']
        reachable = list(zip(self.reachable, repeat('reachable')))
        unreachable = list(zip(self.unreachable, repeat('unreachable')))
        return tabulate(reachable + unreachable, headers, tablefmt="github")


if __name__ == '__main__':
    FROM_ADDR = ip_address('10.0.0.1')
    TO_ADDR = ip_address('10.0.0.15')

    ADDRESSES = [FROM_ADDR + i for i in range(int(TO_ADDR) - int(FROM_ADDR) + 1)]

    ping = AsyncPingHosts(ADDRESSES)
    ping.ping_hosts()
    print(ping.get_ping_status_table())
