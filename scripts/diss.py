from util import run_test
import itertools as it

def tests(folder_path):
    params = []

    debug = False

    fd_timeouts = [0.06, 0.11, 0.21, 0.31] if not debug else [0.31]

    low_repeat = range(3) if not debug else range(1)
    high_repeat = range(50) if not debug else range(1)

    def client_map(system):
        if 'ocons' in system:
            return 'ocaml'
        if 'etcd' in system:
            return 'go'
        if 'zookeeper' in system:
            return 'java'

    def low_jitter_topo(system):
        return {
            'topo':'wan',
            'nn': 5,
            'delay':50,
            'system':system,
            'client': client_map(system),
            'tag':'low_jitter',
            }

    def high_jitter_topo(system):
        return low_jitter_topo(system) | {
                'jitter':0.1,
                'loss':0.01,
                'tag':'high_jitter',
                }

    # etcd stability
    for system, repeat, fd_timeout in it.product(
            ['etcd', 'zookeeper'],
            high_repeat,
            fd_timeouts
            ):
        params.append(
                low_jitter_topo(system) | {
                    'rate' : 5000,
                    'repeat': repeat,
                    'duration': 10,
                    'failure' : "none",
                    'failure_timeout': fd_timeout,
                    })
        params.append(
                high_jitter_topo(system) | {
                    'rate' : 5000,
                    'repeat': repeat,
                    'duration': 10,
                    'failure' : "none",
                    'failure_timeout': fd_timeout,
                    })

    # etcd failure analysis
    for system, repeat, fd_timeout in it.product(
            ['etcd', 'etcd-pre-vote', 'etcd+sbn', 'etcd-pre-vote+sbn'],
            high_repeat,
            fd_timeouts,
            ):
        params.append(
                low_jitter_topo(system) | {
                    'rate' : 1000,
                    'repeat': repeat,
                    'duration': 10,
                    'failure' : "leader",
                    'failure_timeout': fd_timeout,
                    })
        params.append(
                high_jitter_topo(system) | {
                    'rate' : 1000,
                    'repeat': repeat,
                    'duration': 10,
                    'failure' : "leader",
                    'failure_timeout': fd_timeout,
                    })

    # ocons failure bulk
    for system, fd_timeout, repeat in it.product(
            ['ocons-paxos', 'ocons-raft', 'ocons-raft-pre-vote', 'ocons-raft+sbn', 'ocons-raft-pre-vote+sbn'],
            fd_timeouts,
            high_repeat,
            ):
        params.append(
                low_jitter_topo(system) | {
                    'rate' : 1000,
                    'repeat': repeat,
                    'duration': 10,
                    'failure': "leader",
                    'failure_timeout': fd_timeout,
                    })

    # typical failure graphs
    for system, repeat in it.product(
        ['ocons-paxos', 'ocons-raft', 'ocons-raft-pre-vote', 'ocons-raft+sbn', 'ocons-raft-pre-vote+sbn'] +
          ['etcd', 'etcd-pre-vote'],
        low_repeat
        ):
        params.append(
                low_jitter_topo(system) | {
                    'rate': 1000,
                    'repeat': repeat,
                    'duration': 10,
                    'failure':'leader',
                    'failure_timeout': 1,
                    'tcpdump': True,
                    'duration': 20,
                    })

    # TTR varying rate
    for rate, system, repeat in it.product(
        [1000, 2000, 4000, 8000],
        ['ocons-paxos', 'ocons-raft'] +
          ['etcd', 'zookeeper'],
        high_repeat,
        ):
        params.append(
                low_jitter_topo(system) | {
                    'rate': rate,
                    'repeat': repeat,
                    'failure': 'leader',
                    'failure_timeout': 0.5,
                    'duration': 10,
                    })

#    # TTR varying rate with restriction
#    for rate, system, repeat in it.product(
#        [1000, 2000, 4000, 8000],
#        ['ocons-paxos', 'ocons-raft', 'ocons-raft-pre-vote', 'ocons-raft+sbn', 'ocons-raft-pre-vote+sbn'],
#        high_repeat,
#        ):
#        params.append(
#                low_jitter_topo(system) | {
#                    'rate': rate,
#                    'repeat': repeat,
#                    'failure': 'leader',
#                    'failure_timeout': 0.5,
#                    'duration': 10,
#                    }
#                )

    for p in params:
        print(p)

    return [lambda p=p: run_test(folder_path, p) for p in params ]
