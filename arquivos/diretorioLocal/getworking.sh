#!/bin/sh
set -eu

LOGDIR="out/" ;

usage () { # {{{
	cat <<-USAGE
usage: $0 -i NODELIST -l SLICE [-t TIMEOUT]

this will print hosts in NODELIST that we can SSH into and run 'hostname' on.
SLICE should be a planetlab slice name, e.g., upmc_ts. TIMEOUT defaults to 5
seconds.
	USAGE
	exit 1
} # }}}

slice=invalid
nodelist=invalid
timeout=5

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

vxargs -pry -t $timeout -a $nodelist -o $LOGDIR/getworking ssh $slice@{} hostname > /dev/null

cd $LOGDIR/getworking
for file in $(ls *.out) ; do 
	name=$(cat $file)
	if [ "$name" = "${file%.out}" ] ; then echo ${file%.out} ; fi
done
cd - > /dev/null
