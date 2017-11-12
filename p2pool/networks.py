from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    bitconnect=math.Object(
	PARENT=networks.nets['bitconnect'],
	SHARE_PERIOD=15,
	CHAIN_LENGTH=24*60*60//10,
	REAL_CHAIN_LENGTH=24*60*60//10,
	TARGET_LOOKBEHIND=50,
	SPREAD=6,
	IDENTIFIER='1bfe2ededd90fab1'.decode('hex'),
	PREFIX='1bfe2edc898516b2'.decode('hex'),
	P2P_PORT=2935,
	MIN_TARGET=0,
	MAX_TARGET=2**256//2**20 - 1,
	PERSIST=True,
	WORKER_PORT=2936,
	BOOTSTRAP_ADDRS='p2p-spb.xyz crypto.office-on-the.net '.split(' '),
	ANNOUNCE_CHANNEL='#p2pool-alt',
	VERSION_CHECK=lambda v: True,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
