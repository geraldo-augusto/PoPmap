#!/bin/bash

checkerrors () { # {{{
	$BASECMD -t 20 -o out/ls/ ssh $slice@{} ls
	ls $basedir | sort > base.txt
	echo "# reporting copy errors:"
	for file in $( ls out/ls/*.out ) ; do
		cat $file | sort > tmp
		if ! diff tmp base.txt > /dev/null ; then 
			name=$(basename $file)
		   	echo ${name%.out}
	   	fi
	done
	rm tmp base.txt
} # }}}

usage () { # {{{
	cat <<-USAGE
usage: $0 -i NODELIST -l SLICE -d BASEDIR

BASEDIR will be copied into every node in NODELIST using SLICE.
	USAGE
	exit 1
} # }}}

nodelist=invalid
slice=invalid
basedir=invalid

while getopts "i:l:d:h" OPTNAME ; do # {{{
case $OPTNAME in
i)
	nodelist=$OPTARG
	;;
l)
	slice=$OPTARG
	;;
d)
	basedir=$OPTARG
	;;
h|*)
	usage
	;;
esac
done # }}}

test $nodelist != invalid || usage
test $slice != invalid || usage
test $basedir != invalid || usage

BASECMD="vxargs -pr -a $nodelist -y"

$BASECMD -t 300 -o out/copy/ scp -rqC $basedir/* $slice@{}:

checkerrors
