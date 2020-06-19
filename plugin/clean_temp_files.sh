#!/bin/sh

rmpo() {
	for file2 in `ls -A $1`
	do
		if [ $file2 == "Blackhole.socket" ]; then
			continue
		elif [ $file2 == "camd.socket" ]; then
			continue
		elif [ $file2 == "ecm.info" ]; then
			continue
		elif [ $file2 == "hotplug.socket" ]; then
			continue
		elif [ $file2 == ".oscam" ]; then
			continue
		elif [ $file2 == ".listen.camd.socket" ]; then
			continue
		elif [ $file2 == ".listen.ciplus.socket" ]; then
			continue
		elif [ $file2 == "mmi.socket" ]; then
			continue
		elif [ $file2 == ".exteplayerterm.socket" ]; then
			continue
		else
			rm -rf $1/$file2 >/dev/null 2>&1
		fi
	done
}

rm -rf /media/hdd/enigma2_crash*.log >/dev/null 2>&1
rm -rf /media/usb/enigma2_crash*.log >/dev/null 2>&1
rm -rf /home/root/enigma2_crash*.log >/dev/null 2>&1
rmpo /var/volatile/tmp
exit 0
