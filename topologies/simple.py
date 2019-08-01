from mininet.net import Containernet
from mininet.node import Controller, UserSwitch, IVSSwitch, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

import importlib

import utils

def ip_from_int(i):
    return '10.{0:d}.{1:d}.{2:d}'.format(i/(2**16),(i%(2**16))/(2**8),i%(2**8))

def setup(service, n=3):
    n = int(n)
    #- Core setup -------

    net = Containernet(controller=Controller, switch=OVSSwitch)
    info('*** Adding controller\n')
    net.addController('c0')
    
    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    
    info('*** Adding docker containers and adding links\n')
    cluster_ips = [ip_from_int(i+2) for i in range(n)]
    dimage = "cjj39_dks28/"+service
    print("*** Using image: " + dimage)
    dockers = [
            net.addDocker(
                'd' + str(i+1), 
                ip    = cluster_ips[i], 
                dimage=dimage
                ) 
            for i in range(n)
            ]

    for d in dockers:
        net.addLink(d,s1, cls=TCLink, delay='50ms', bw=1, max_queue_size=200)

    microclient = utils.addClient(net, service, 'mc', ip='10.0.0.1')

    net.addLink(microclient, s1) 

    net.start()

    system_setup_func = (
            importlib.import_module(
                "systems.{0}.scripts.setup".format(service)
                )
            ).setup
    restarters = system_setup_func(dockers, cluster_ips)

    return (net, cluster_ips, [microclient], restarters)
