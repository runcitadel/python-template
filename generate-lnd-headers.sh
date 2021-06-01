#!/usr/bin/env bash

VERSION="${1:-master}"

echo "Downloading LND's rpc.proto"
wget -q "https://raw.githubusercontent.com/lightningnetwork/lnd/${VERSION}/lnrpc/rpc.proto"
echo "Generating files"
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=lib --grpc_python_out=lib rpc.proto
# Fix an import path
sed -i 's/import rpc_pb2 as rpc__pb2/from . import rpc_pb2 as rpc__pb2/g' lib/rpc_pb2_grpc.py
echo "Cleaning up"
rm rpc.proto