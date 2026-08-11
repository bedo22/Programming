#!/usr/bin/env bash
# Wave watchdog — detects worker completions without user polling.
# For each /tmp/twin-<doc>/ with report.md + ar.html: logs a DONE line when the
# report is newer than the last-seen state. Startup seeds state for all
# pre-existing dirs (old-wave leftovers produce no spam). Idle-cost: near zero.
# Start detached:  nohup plans/wave-watch.sh > /tmp/waves/watch.out 2>&1 &
set -u
STATE=/tmp/waves/state
LOG=/tmp/waves/LOG
mkdir -p "$STATE"
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
[ -f "$LOG" ] || : > "$LOG"

# seed: current dirs are known already
for d in /tmp/twin-*/report.md; do
  [ -e "$d" ] || continue
  doc=${d#/tmp/twin-}; doc=${doc%/report.md}
  stat -c %Y "$d" > "$STATE/$doc" 2>/dev/null
done
log "watchdog up (pid $$) — seeded $(ls "$STATE" | wc -l) existing dirs, poll 120s"

while true; do
  for d in /tmp/twin-*/report.md; do
    [ -e "$d" ] || continue
    doc=${d#/tmp/twin-}; doc=${doc%/report.md}
    [ -f "/tmp/twin-$doc/ar.html" ] || continue
    mt=$(stat -c %Y "$d" 2>/dev/null) || continue
    [ -f "$STATE/$doc" ] && [ "$mt" -le "$(cat "$STATE/$doc")" ] && continue
    log "DONE $doc (report $(stat -c %y "$d" | cut -d. -f1))"
    echo "$mt" > "$STATE/$doc"
  done
  sleep 120
done
