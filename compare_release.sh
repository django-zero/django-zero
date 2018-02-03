DIR=.release-compare
REV=`git rev-parse HEAD`

rm -rf $DIR; mkdir $DIR
git archive $REV | tar xf - -C $DIR;
(cd $DIR; python setup.py bdist >/dev/null 2>&1)

find $DIR/build/lib/django_zero -type f  | cut -d/ -f4- | sort > .files-dist
find $DIR/django_zero -type f  | cut -d/ -f2- | sort > .files-repo

diff .files-repo .files-dist
rm -rf $DIR .files-repo .files-dist


