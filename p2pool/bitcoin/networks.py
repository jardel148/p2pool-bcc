import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

@defer.inlineCallbacks
def get_subsidy(bitcoind, target):
    res = yield bitcoind.rpc_getblock(target)

    defer.returnValue(res)

nets = dict(
    bitconnect=math.Object(
	P2P_PREFIX = '325e6f86'.decode('hex'),
	P2P_PORT = 9239,
	ADDRESS_VERSION = 18,
	RPC_PORT = 9240,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            0 == (yield bitcoind.rpc_getblock('d3bd95c47fa17c47e1e2732d7072a6c4014a2fa93873124418a8fd9a300'))['height'] and
            not (yield bitcoind.rpc_getinfo())['testnet']
	)),
	SUBSIDY_FUNC = lambda height: 10*100000000,
	POW_FUNC = lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
	BLOCK_PERIOD = 120,
	SYMBOL = 'BCC',
	CONF_FILE_FUNC = lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'bitconnect') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/bitconnect/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bitconnect'), 'bitconnect.conf'),
	BLOCK_EXPLORER_URL_PREFIX = 'https://chainz.cryptoid.info/bcc/block.dws?',
	ADDRESS_EXPLORER_URL_PREFIX = 'https://chainz.cryptoid.info/bcc/address.dws?',
	TX_EXPLORER_URL_PREFIX = 'https://chainz.cryptoid.info/bcc/tx.dws?',
	SANE_TARGET_RANGE = (2**256//2**33 - 1, 2**256//2**31 - 1),
	DUMB_SCRYPT_DIFF = 2**16,
	DUST_THRESHOLD = 0.03e8,
   ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
