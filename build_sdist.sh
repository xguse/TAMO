#!/bin/bash


DISTDIR="TAMO-`cat VERSION`"
mkdir -p build/$DISTDIR

DISTFN="$DISTDIR.tgz"

find * -wholename '*build*' -or -wholename '*.git*' -prune -o -print | xargs -t -n 1 -I {} cp -r {} build/$DISTDIR/{}
(cd build; tar czf $DISTFN $DISTDIR)
