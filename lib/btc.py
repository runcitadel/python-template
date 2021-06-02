# A few basic helper functions for interfacing with Bitcoin Core

from os import getenv
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

class BtcRPC:
    def __init__(self):
        btcurl = "http://%s:%s@%s:%s" % (getenv('BITCOIN_RPC_USER'), getenv(
            'BITCOIN_RPC_PASS'), getenv('BITCOIN_IP'), getenv('BITCOIN_RPC_PORT'))
        self.connection = AuthServiceProxy(btcurl)

    def connection_locked(self):
        try:
            self.get_blockchain_info()
            return True
        except JSONRPCException:
            return False

    def get_blockchain_info(self):
        response = self.connection.getblockchaininfo()
        return response

    def get_sync_progress(self):
        response = self.connection.getblockchaininfo()
        return response["verificationprogress"] * 100

    def get_connection(self):
        return self.connection
