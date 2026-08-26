#!/usr/bin/env bash
# Wave watchdog + wake-pager.
# 1) DETECTION (free): logs DONE <doc> when a worker report lands.
# 2) WAKE (free-ish): injects a message into the MAIN pi session via
#    orca-ide terminal send, so the orchestrator (full context, judgment)
#    handles integration + respawns instead of a stateless automation agent.
# 3) FAILURE ALERT: a report.md starting with "STATUS:" = worker stopped
#    mid-way (resilience protocol) -> wake with a FAILED tag.
# Debounce: max one wake per doc per 30 min. Idle-cost: near zero.
# Start detached:  nohup plans/wave-watch.sh > /tmp/waves/watch.out 2>&1 &
set -u
STATE=/tmp/waves/state
WOKEN=/tmp/waves/woken
LOG=/tmp/waves/LOG
MAIN_TERM=term_371ec29c-6772-4eb5-b7fb-50ea89bdcea5   # main pi pane (verify with terminal list)
mkdir -p "$STATE" "$WOKEN"
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
[ -f "$LOG" ] || : > "$LOG"

wake() {  # wake <label> <doc>
  local label=$1 doc=$2 now
  now=$(date +%s)
  [ -f "$WOKEN/$doc" ] && [ $(( now - $(cat "$WOKEN/$doc") )) -lt 1800 ] && return
  echo "$now" > "$WOKEN/$doc"
  timeout 25 ~/.local/bin/orca-ide terminal send --terminal "$MAIN_TERM" \
    --text "WAKE [$label] $doc — watchdog: report landed. Integrate (or respawn if STATUS)." --enter >/dev/null 2>&1 \
    && log "woke main session: $label $doc" || log "wake send FAILED for $doc (is the main pane up?)"
}

# seed: current dirs are known already
for d in /tmp/twin-*/report.md; do
  [ -e "$d" ] || continue
  doc=${d#/tmp/twin-}; doc=${doc%/report.md}
  stat -c %Y "$d" > "$STATE/$doc" 2>/dev/null
done
log "watchdog+pager up (pid $$) — seeded $(ls "$STATE" | wc -l) dirs, poll 120s, main pane $MAIN_TERM"

while true; do
  for d in /tmp/twin-*/report.md; do
    [ -e "$d" ] || continue
    doc=${d#/tmp/twin-}; doc=${doc%/report.md}
    [ -f "/tmp/twin-$doc/ar.html" ] || continue
    mt=$(stat -c %Y "$d" 2>/dev/null) || continue
    [ -f "$STATE/$doc" ] && [ "$mt" -le "$(cat "$STATE/$doc")" ] && continue
    echo "$mt" > "$STATE/$doc"
    if head -c 40 "$d" 2>/dev/null | grep -q '^STATUS:'; then
      log "FAILED $doc (STATUS line — worker stopped mid-way)"
      wake FAILED "$doc"
    else
      log "DONE $doc (report $(stat -c %y "$d" | cut -d. -f1))"
      wake DONE "$doc"
    fi
  done
  sleep 120
done
