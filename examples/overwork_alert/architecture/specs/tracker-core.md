<!-- spd:#:spec -->
# Spec: Tracker Core

<!-- spd:id-ref:spec has="task" -->
- [x] - `spd-overwork-alert-spec-tracker-core`
<!-- spd:id-ref:spec -->

<!-- spd:##:context -->
## 1. Spec Context

<!-- spd:overview -->
### 1. Overview
This spec defines the core background tracking loop: how the daemon measures “active work time” using macOS idle time, how it applies configuration defaults, and how it maintains session-scoped in-memory tracker state.

Key assumptions:
- Idle time is best-effort and may be unavailable on some ticks.
- Accumulated active time is not persisted across daemon restarts.
- Manual reset is implemented via a control command handled in a separate spec.

Configuration parameters (effective defaults in v1):
- limit_seconds: 10800 (3 hours)
- idle_threshold_seconds: 300 (5 minutes)
- repeat_interval_seconds: 1800 (30 minutes)
- tick_interval_seconds: 5
- max_tick_delta_seconds: tick_interval_seconds * 2

Acceptance criteria (timing/behavior):
- When idle exceeds idle_threshold_seconds, accumulation MUST stop within 10 seconds.
- When active work resumes (idle below threshold) and status is RUNNING, accumulation MUST resume on the next tick.

Validation behavior:
- If a configuration value is missing or invalid, the daemon MUST continue using the default.
- The daemon MUST treat time deltas < 0 as 0 seconds.
- The daemon MUST clamp large time deltas to max_tick_delta_seconds (e.g., after sleep/wake) to avoid overcounting.
<!-- spd:overview -->

<!-- spd:paragraph:purpose -->
### 2. Purpose
Provide deterministic, low-overhead, idle-aware active-time accumulation that downstream specs (notifications and control) can rely on.
<!-- spd:paragraph:purpose -->

### 3. Actors
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
- `spd-overwork-alert-actor-macos`
<!-- spd:id-ref:actor -->

### 4. References
<!-- spd:list:references -->
- Overall Design: [DESIGN.md](../DESIGN.md)
- ADRs: `spd-overwork-alert-adr-cli-daemon-launchagent-no-menubar`
- Related spec: notifications.md
<!-- spd:list:references -->
<!-- spd:##:context -->

<!-- spd:##:flows -->
## 2. Actor Flows

<!-- spd:###:flow-title repeat="many" -->
### Run tracking tick loop

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-tracker-core-flow-tick-loop`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-macos`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - Daemon loads effective configuration (defaults + validation) - `inst-load-config`
2. [x] - `p1` - **IF** last_tick_at is not set: set last_tick_at=now and **RETURN** (no accumulation) - `inst-init-first-tick`
3. [x] - `p1` - Daemon reads current idle time sample from macOS - `inst-read-idle`
4. [x] - `p1` - **IF** idle time is unavailable: set last_tick_at=now and **RETURN** (no accumulation) - `inst-handle-idle-unavailable`
5. [x] - `p1` - **IF** idle_seconds >= idle_threshold_seconds: set last_tick_at=now and **RETURN** (paused by idle) - `inst-skip-on-idle`
6. [x] - `p1` - **IF** tracker status is paused: set last_tick_at=now and **RETURN** (no accumulation) - `inst-skip-on-paused`
7. [x] - `p1` - Algorithm: update active_time_seconds using `spd-overwork-alert-spec-tracker-core-algo-accumulate-active-time` - `inst-accumulate`
8. [x] - `p1` - **RETURN** updated TrackerState - `inst-return-state`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:##:flows -->

<!-- spd:##:algorithms -->
## 3. Algorithms

<!-- spd:###:algo-title repeat="many" -->
### Accumulate active time

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-tracker-core-algo-accumulate-active-time`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - Compute raw delta_seconds = now - last_tick_at - `inst-compute-delta`
2. [x] - `p1` - **IF** delta_seconds < 0 set delta_seconds = 0 - `inst-handle-negative-delta`
3. [x] - `p1` - Compute max_tick_delta_seconds = tick_interval_seconds * 2 - `inst-compute-max-delta`
4. [x] - `p1` - Clamp delta_seconds to max_tick_delta_seconds - `inst-clamp-delta`
5. [x] - `p1` - Add delta_seconds to active_time_seconds - `inst-add-delta`
6. [x] - `p1` - Update last_tick_at to now - `inst-update-last-tick`
7. [x] - `p1` - **RETURN** updated TrackerState - `inst-return-updated-state`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->

<!-- spd:##:algorithms -->

<!-- spd:##:states -->
## 4. States

<!-- spd:###:state-title repeat="many" -->
### Tracker runtime status

<!-- spd:id:state has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-tracker-core-state-tracker-status`

<!-- spd:sdsl:state-transitions -->
1. [x] - `p1` - **FROM** RUNNING **TO** PAUSED **WHEN** user sends pause command - `inst-transition-pause`
2. [x] - `p1` - **FROM** PAUSED **TO** RUNNING **WHEN** user sends resume command - `inst-transition-resume`
<!-- spd:sdsl:state-transitions -->
<!-- spd:id:state -->
<!-- spd:###:state-title repeat="many" -->

<!-- spd:##:states -->

<!-- spd:##:requirements -->
## 5. Definition of Done

<!-- spd:###:req-title repeat="many" -->
### Idle-aware active-time accumulation

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-overwork-alert-spec-tracker-core-req-idle-aware-accumulation`

<!-- spd:paragraph:req-body -->
When the daemon is running, active time increases only while the user is not idle beyond the configured threshold. When the user is idle beyond the threshold, accumulation does not increase.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- Component: `spd-overwork-alert-component-daemon`
- Component: `spd-overwork-alert-component-idle-detector`
- Data: `spd-overwork-alert-dbtable-tracker-state`
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-overwork-alert-spec-tracker-core-flow-tick-loop`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-overwork-alert-spec-tracker-core-algo-accumulate-active-time`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-overwork-alert-fr-track-active-time`
- `spd-overwork-alert-fr-configurable-limit`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-overwork-alert-nfr-low-overhead`
- `spd-overwork-alert-nfr-privacy-local-only`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-overwork-alert-principle-local-only-minimal-state`
- `spd-overwork-alert-principle-low-overhead`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-overwork-alert-constraint-no-auto-reset-no-persist`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-overwork-alert-component-daemon`
- `spd-overwork-alert-component-idle-detector`
- `spd-overwork-alert-component-config-loader`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-overwork-alert-seq-run-and-alert`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-overwork-alert-dbtable-tracker-state`
- `spd-overwork-alert-dbtable-config`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->

<!-- spd:###:req-title repeat="many" -->
### Configuration defaults and validation

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-overwork-alert-spec-tracker-core-req-config-defaults`

<!-- spd:paragraph:req-body -->
If no configuration is present or some configuration values are invalid, the daemon continues operating using safe defaults.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- Component: `spd-overwork-alert-component-config-loader`
- Data: `spd-overwork-alert-dbtable-config`
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-overwork-alert-spec-tracker-core-flow-tick-loop`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-overwork-alert-spec-tracker-core-algo-accumulate-active-time`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-overwork-alert-fr-configurable-limit`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-overwork-alert-nfr-privacy-local-only`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-overwork-alert-principle-local-only-minimal-state`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-overwork-alert-constraint-no-auto-reset-no-persist`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-overwork-alert-component-config-loader`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-overwork-alert-seq-run-and-alert`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-overwork-alert-dbtable-config`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->

<!-- spd:##:requirements -->

<!-- spd:##:additional-context -->
## 6. Additional Context (optional)

<!-- spd:free:context-notes -->
This spec intentionally excludes manual reset, pause/resume, and CLI control details; those are defined in cli-control.md.

TrackerState field expectations (high-level):
- status: RUNNING or PAUSED
- active_time_seconds: monotonically non-decreasing within a session except when reset
- last_tick_at: time of most recent tick observation (updated even when skipping accumulation)

This spec does not define notification delivery. The daemon tick loop may pass the updated TrackerState (and the most recent idle sample) to the notification policy defined in notifications.md.

Out of scope / not applicable (v1):
- No persistence of accumulated time across daemon restarts.
- No network I/O and no telemetry.
- No UI beyond macOS notifications (notification policy defined in notifications.md).
<!-- spd:free:context-notes -->
<!-- spd:##:additional-context -->

<!-- spd:#:spec -->
