import grpc
import codecs
import os
from time import sleep

import lib.rpc_pb2 as lnrpc
import lib.rpc_pb2_grpc as rpc_stub

from lib.utils import human_format

class LndGRPC:
    def __init__(self):
        self.stub = self.get_stub()
        self.metadata = [('macaroon', self._get_macaroon())]

    def get_stub(self):
        cert = open(os.path.expanduser('./lnd/tls.cert'), 'rb').read()
        creds = grpc.ssl_channel_credentials(cert)
        lnurl = "%s:%s" % (os.getenv('LND_IP'), os.getenv('LND_GRPC_PORT'))
        channel = grpc.secure_channel(lnurl, creds)
        stub = rpc_stub.LightningStub(channel)
        return stub

    def _get_macaroon(self):
        f = open('./lnd/data/chain/bitcoin/' + os.getenv("BTC_NETWORK") + '/admin.macaroon', 'rb')
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')
        return macaroon

    def get_active_channels(self):
        response = self.stub.ListChannels(
            lnrpc.ListChannelsRequest(
                active_only=True
            ),
            metadata=self.metadata
        )
        try:
            return str(len(response.channels))
        except:
            return "0"

    # Returns the forwarding events of the last 24H

    def get_forwarding_events(self):
        response = self.stub.ForwardingHistory(
            lnrpc.ForwardingHistoryRequest(), metadata=self.metadata)
        try:
            return str(len(response.forwarding_events))
        except:
            return "0"

    def get_max_send(self):
        response = self.stub.ChannelBalance(
            lnrpc.ChannelBalanceRequest(), metadata=self.metadata)
        sats = "0"
        try:
            sats = human_format(response.local_balance)
        except:
            sats = "0"
        return sats + " Sats"

    def get_max_receive(self):
        response = self.stub.ChannelBalance(
            lnrpc.ChannelBalanceRequest(), metadata=self.metadata)
        sats = "0"
        try:
            sats = human_format(response.remote_balance)
        except:
            sats = "0"
        return sats + " Sats"

    def check_lnd(self):
        try:
            response = self.stub.GetInfo(lnrpc.GetInfoRequest(),metadata=self.metadata)
            response.num_active_channels
        except grpc._channel._InactiveRpcError:
            # Try again until lnd is unlocked
            sleep(2)
            self.check_lnd()
