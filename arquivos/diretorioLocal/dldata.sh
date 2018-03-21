#!/bin/sh
set -u
set -x

usage () { # {{{
	cat <<-USAGE
usage: $0 -i NODELIST -l SLICE -d REMOTEDIR
       -s DOWNLOADDIR -k RSAKEY -L LOGDIR [-t TIMEOUT]

this will download ctrack-measured data on directory REMOTEDIR in all PlanetLab
nodes in the NODELIST file at DOWNLOADDIR. SLICE should be a slice name, e.g.,
upmc_ts. RSAKEY should be a RSA key that the planetlab nodes accept (e.g.,
~/.ssh/id_rsa_everywhere). TIMEOUT defaults to 300 seconds.

this script will download all data files created more than 6 hours ago. also,
we assume files are named /REMOTEDIR/prefix.%Y%m%d%H%M%S on the remote hosts.


	USAGE
	exit 1
} # }}}

slice=invalid
nodelist=invalid
remotedir=invalid
dldir=invalid
rsakey=invalid
logdir=invalid
timeout=300

while getopts "i:l:d:s:t:k:L:h" OPTNAME ; do # {{{
case $OPTNAME in
i)
	nodelist=$OPTARG
	;;
l)
	slice=$OPTARG
	;;
d)
	remotedir=$OPTARG
	;;
s)
	dldir=$OPTARG
	;;
t)
	timeout=$OPTARG
	;;
k)
	rsakey=$OPTARG
	;;
L)
	logdir=$OPTARG
	;;
h|*)
	usage
	;;
esac
done
shift $(expr $OPTIND - 1)
OPTIND=1 # }}}

test $slice != invalid || usage
test $nodelist != invalid || usage
test $remotedir != invalid || usage
test $dldir != invalid || usage
test $logdir != invalid || usage
if [ ! -f $rsakey ] ; then echo "RSA key not found." ; exit 1 ; fi
if [ ! -f $nodelist ] ; then echo "nodelist not found." ; exit 1 ; fi
mkdir -p $dldir

BASECMD="vxargs -pr -a $nodelist -y" ;

$BASECMD -t 10 mkdir -p $dldir/{}
$BASECMD -t 20 ssh -i $rsakey $slice@{} sudo chmod 777 -R $remotedir
$BASECMD -t 20 -o $logdir/dllist/ ssh -i $rsakey $slice@{} \
		find $remotedir -type f

basedate=$(\date -u +"%Y%m%d%H%M%S")
#basedate=$(\date -u -d "-6 hours" +"%Y%m%d%H%M%S")
cat $nodelist | while read hostname ; do
	rm -f $logdir/dllist/$hostname.list
	cat $logdir/dllist/$hostname.out | while read filename ; do
		filedate=$(basename $filename)
		filedate=${filedate##*.}	
                echo $filedate $basedate
		if [ $filedate -lt $basedate ] ; then
			echo $filename >> $logdir/dllist/$hostname.list
		fi
	done
done

$BASECMD -P 10 -t $timeout -o $logdir/dl/ rsync -auvz --append \
                --remove-source-files \
		--no-relative --files-from $logdir/dllist/{}.list \
		--rsh "ssh -i $rsakey" $slice@{}:/ $dldir/{}/

