NAME=$1

C504_URL=caelum-504.cl.cam.ac.uk
C504_IP=`dig +short caelum-504.cl.cam.ac.uk`
C505_URL=caelum-505.cl.cam.ac.uk
C505_IP=`dig +short caelum-505.cl.cam.ac.uk`
C506_URL=caelum-506.cl.cam.ac.uk
C506_IP=`dig +short caelum-506.cl.cam.ac.uk`

case $NAME in
	c504)
		URL=${C504_URL}
		IP=${C504_IP}
		;;
	c505)
		URL=${C505_URL}
		IP=${C505_IP}
		;;
	c506)
		URL=${C506_URL}
		IP=${C506_IP}
		;;
	*)
		echo "No machine of that name"
		;;
esac	

echo $IP
echo $URL
echo $C504_IP
echo $C505_IP
echo $C506_IP


#etcd --name ${NAME} \
#	--initial-advertise-peer-urls http://${IP}:2380 \
#	--listen-peer-urls http://${IP}:2380 \
#	--listen-client-urls http://${IP}:2380 \
#	--advertise-client-urls http://${IP}:2380 \
#	--initial-cluster-token etcd-cluster-1 \
#	--initial-cluster C504=http://${C504_IP}:2380,C505=http://${C505_IP}:2380,C506=http://${C506_IP}:2380 \
#	--initial-cluster-state new
	
