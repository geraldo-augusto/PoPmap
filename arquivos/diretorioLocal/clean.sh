#!/bin/sh
set -eu

LOGDIR="out/"

usage () { # {{{
	cat <<-USAGE
usage: $0 -i NODELIST -l SLICE [-t TIMEOUT]

this script will delete all files and reset crontab entries in monitors listed
in NODELIST. NODELIST should contain one monitor per line. SLICE should be a 
planetlab slice (e.g., upmc_ts). TIMEOUT defaults to 300 seconds.

	USAGE
	exit 1
} # }}}

nodelist=invalid
slice=invalid
timeout=300

while getopts "i:l:t:h" OPTNAME ; do # {{{
case $OPTNAME in
i)
	nodelist=$OPTARG
	;;
l)
	slice=$OPTARG
	;;
t)
	timeout=$OPTARG
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
if [ ! -f $nodelist ] ; then echo "nodelist not found." ; exit 1 ; fi

BASECMD="vxargs -pry -a $nodelist -t $timeout -o $LOGDIR/clean" ;

$BASECMD ssh $slice@{} crontab -r > /dev/null
$BASECMD ssh $slice@{} sudo find /home/$slice/ -type f -delete > /dev/null
$BASECMD ssh $slice@{} sudo rm -rf /home/$slice/* > /dev/null

$BASECMD ssh $slice@{} ls > /dev/null
echo "# listing monitors with errors:"
for file in $( ls $LOGDIR/clean/*.out ) ; do
	test -s $file && echo "$(basename ${file%%.out})"
done
