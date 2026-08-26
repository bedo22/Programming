#!/usr/bin/env bash
# Precheck for the wave-integrate automation: exit 0 iff any /tmp/twin-<doc>/
# has a report.md newer than its last-seen state (i.e. unintegrated work).
set -u
for f in /tmp/waves/state/*; do
  [ -f "$f" ] || continue
  d=${f##*/}
  [ -f "/tmp/twin-$d/report.md" ] || continue
  [ "$(stat -c %Y "/tmp/twin-$d/report.md")" -gt "$(cat "$f")" ] && exit 0
done
exit 1
