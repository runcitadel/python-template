from time import sleep
from lib.btc import BtcRPC
from lib.lnd import LndGRPC

# This establishes a connection
locked = True

while locked:
    btc_rpc = BtcRPC()
    try:
        # Test connection to BTC
        locked = btc_rpc.connection_locked()
    except Exception:
        print("Please make sure BITCOIN_RPC_PORT, BITCOIN_RPC_PASS, BITCOIN_IP and BITCOIN_RPC_PORT are set and valid")

    # Wait and restart loop to wait for unlock
    sleep(10)
    continue

lnd_grpc = LndGRPC()
lnd_grpc.check_lnd()

# Insert your own code here

# Hint: Most of the interface (Default LND GRPC interface via grpcio module and Bitcoin interface via bitcoinrpc module) are xposed like this:
# btc_rpc.get_connection()
# lnd_grpc.get_stub()