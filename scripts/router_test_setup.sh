cat > /tmp/m05_net_setup.sh <<'EOF'
#!/bin/sh

echo "===== set root password ====="
printf 'bpir4pro8x\nbpir4pro8x\n' | passwd root

echo
echo "===== configure LAN management 192.168.8.1 ====="
uci set network.lan='interface'
uci set network.lan.device='br-lan'
uci set network.lan.proto='static'
uci set network.lan.ipaddr='192.168.8.1'
uci set network.lan.netmask='255.255.255.0'
uci delete network.lan.gateway 2>/dev/null
uci delete network.lan.dns 2>/dev/null
uci delete network.lan.ip6assign 2>/dev/null

echo
echo "===== configure WAN RJ45 eth1 test address 192.168.9.1 ====="
uci set network.m05wan='interface'
uci set network.m05wan.device='eth1'
uci set network.m05wan.proto='static'
uci set network.m05wan.ipaddr='192.168.9.1'
uci set network.m05wan.netmask='255.255.255.0'
uci delete network.m05wan.gateway 2>/dev/null
uci delete network.m05wan.dns 2>/dev/null

echo
echo "===== enable ssh password login ====="
uci set dropbear.@dropbear[0].PasswordAuth='on'
uci set dropbear.@dropbear[0].RootPasswordAuth='on'
uci set dropbear.@dropbear[0].RootLogin='1'
uci set dropbear.@dropbear[0].Interface='lan'

echo
echo "===== commit uci ====="
uci commit network
uci commit dropbear

echo
echo "===== restart services ====="
/etc/init.d/network restart
sleep 5
/etc/init.d/dropbear enable
/etc/init.d/dropbear restart

echo
echo "===== bring eth1 up explicitly ====="
ip link set eth1 up 2>/dev/null
ip addr add 192.168.9.1/24 dev eth1 2>/dev/null
sleep 3

echo
echo "===== current network config ====="
uci show network.lan
uci show network.m05wan
uci show dropbear

echo
echo "===== link states ====="
for d in br-lan eth1 lan1 lan2 lan3 lan4 lan5 fpc; do
	[ -d "/sys/class/net/$d" ] || continue
	state="$(cat /sys/class/net/$d/operstate 2>/dev/null)"
	carrier="$(cat /sys/class/net/$d/carrier 2>/dev/null)"
	addr="$(cat /sys/class/net/$d/address 2>/dev/null)"
	echo "$d state=$state carrier=$carrier addr=$addr"
done

echo
echo "===== addresses ====="
ip addr show br-lan
ip addr show eth1

echo
echo "===== done ====="
echo "LAN5/br-lan management: 192.168.8.1"
echo "WAN RJ45 eth1 test:    192.168.9.1"
echo "root password:         bpir4pro8x"
EOF

sh /tmp/m05_net_setup.sh 2>&1
