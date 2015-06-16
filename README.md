# pyzfslib - zfs interaction from python.

This is mainly developed on a need to have basis for my work.

## Features

This list of features are things that I would like to implement in the future, and also things that you are welcome to implement! I will gladly merge code :)

- [-] zfs
  - [x] Snapshot creation, listing and destruction
  - [ ] Filesystem creation, listing and destruction
  - [ ] Filesystem modification (change settings)
  - [ ] Mounting and unmounting
  - [ ] List size/stats information
- [ ] zpool
  - [ ] Create and delete pools
  - [ ] ARC stats (sysctl -q kstat.zfs.misc.arcstats)
  - [ ] I/O stats

## Examples

(more and better documentation will come Soon™)

```python

from pyzfslib import zfs

snap = zfs.Snapshot()

try:
	snap.create('storage/users/llp', 'test_snap1')
except zfs.ZfsCommandException as e:
	print(e)

snaps = snap.list_sort(sort='used', filters=[('snapname', 'eq', 'test_snap1')])

print("{:>20}{:>40}{:>20}{:>20}{:>20}{:>20}{:>20}".format('vol', 'snapname', 'creation', 'used', 'avail', 'refer', 'mountpoint'))

for v in snaps:
	print("{:>20}{:>40}{:>20}{:>20}{:>20}{:>20}{:>20}".format(v['vol'], v['snapname'], v['creation'], v['used'], str(v['avail']), str(v['refer']), str(v['mountpoint'])))

try:
	snap.destroy('storage/users/llp', 'test_snap1')
except zfs.ZfsCommandException as e:
	print(e)

```

