<!-- spd:#:design -->
# Technical Design: Overwork Alert

<!-- spd:##:architecture-overview -->
## 1. Architecture Overview

<!-- spd:###:architectural-vision -->
### Architectural Vision

<!-- spd:architectural-vision-body -->
Overwork Alert is a single-user, local-only macOS tool implemented as a background daemon with a companion CLI. The daemon continuously estimates “active work time” using an idle-aware clock and emits macOS notifications when a configurable limit is exceeded.

The system boundary is the user’s macOS session: the tool does not depend on remote services and does not persist accumulated work time across restarts. Architecture choices prioritize low complexity, low overhead, and predictable behavior (no automatic midnight reset; only explicit manual reset).
<!-- spd:architectural-vision-body -->
<!-- spd:###:architectural-vision -->

<!-- spd:###:architecture-drivers -->
### Architecture drivers

<!-- spd:####:prd-requirements -->
#### Product requirements

<!-- spd:fr-title repeat="many" -->
##### Track active work time (idle-aware)

<!-- spd:id-ref:fr has="priority,task" -->
- [x] `p1` - `spd-overwork-alert-fr-track-active-time`
<!-- spd:id-ref:fr -->

**Solution**: A daemon runs a periodic loop. Each tick reads current idle time from macOS (idle detector) and increments `active_time` only when idle is below the configured threshold and tracking is not paused.
<!-- spd:fr-title repeat="many" -->

<!-- spd:fr-title repeat="many" -->
##### Configure limit and idle threshold

<!-- spd:id-ref:fr has="priority,task" -->
- [x] `p1` - `spd-overwork-alert-fr-configurable-limit`
<!-- spd:id-ref:fr -->

**Solution**: Configuration is read from a local config file with safe defaults. The daemon loads configuration on startup and can be restarted (or later extended to support reload) to apply changes.
<!-- spd:fr-title repeat="many" -->

<!-- spd:fr-title repeat="many" -->
##### Notify when limit is exceeded and repeat reminders

<!-- spd:id-ref:fr has="priority,task" -->
- [x] `p1` - `spd-overwork-alert-fr-notify-on-limit`
<!-- spd:id-ref:fr -->

**Solution**: The daemon transitions into an “over limit” state when `active_time > limit`. A notifier component sends a macOS notification immediately, then repeats at the configured interval while the user remains active and the session is still over limit.
<!-- spd:fr-title repeat="many" -->

<!-- spd:fr-title repeat="many" -->
##### Manual reset (no automatic reset)

<!-- spd:id-ref:fr has="priority,task" -->
- [x] `p2` - `spd-overwork-alert-fr-manual-reset`
<!-- spd:id-ref:fr -->

**Solution**: The daemon exposes a control channel. The CLI sends a `reset` command, which causes the daemon to zero the in-memory accumulated `active_time` and clear over-limit reminder state.
<!-- spd:fr-title repeat="many" -->

<!-- spd:fr-title repeat="many" -->
##### Run continuously in background and support autostart

<!-- spd:id-ref:fr has="priority,task" -->
- [x] `p2` - `spd-overwork-alert-fr-autostart`
<!-- spd:id-ref:fr -->

**Solution**: Provide LaunchAgent installation/uninstallation that starts the daemon at login. The daemon is designed as a long-running process with safe defaults and defensive error handling.
<!-- spd:fr-title repeat="many" -->

<!-- spd:fr-title repeat="many" -->
##### Provide CLI controls (status/pause/resume/reset)

<!-- spd:id-ref:fr has="priority,task" -->
- [x] `p2` - `spd-overwork-alert-fr-cli-controls`
<!-- spd:id-ref:fr -->

**Solution**: A CLI provides user-facing commands and communicates with the daemon via a local-only control interface to query status and issue commands.
<!-- spd:fr-title repeat="many" -->

<!-- spd:nfr-title repeat="many" -->
##### Privacy & Data Handling

<!-- spd:id-ref:nfr has="priority,task" -->
- [x] `p1` - `spd-overwork-alert-nfr-privacy-local-only`
<!-- spd:id-ref:nfr -->

**Solution**: No network I/O is performed. Only minimal local configuration and runtime control artifacts (e.g., a local socket path) are used.
<!-- spd:nfr-title repeat="many" -->

<!-- spd:nfr-title repeat="many" -->
##### Reliability

<!-- spd:id-ref:nfr has="priority,task" -->
- [x] `p2` - `spd-overwork-alert-nfr-reliability`
<!-- spd:id-ref:nfr -->

**Solution**: Notification failures are treated as non-fatal; tracking continues and status remains queryable via CLI. The daemon loop isolates OS integration errors so a single failed tick cannot crash the process.
<!-- spd:nfr-title repeat="many" -->

<!-- spd:nfr-title repeat="many" -->
##### Performance & Resource Usage

<!-- spd:id-ref:nfr has="priority,task" -->
- [x] `p2` - `spd-overwork-alert-nfr-low-overhead`
<!-- spd:id-ref:nfr -->

**Solution**: Use low-frequency polling (seconds-level) for idle detection and accumulation. Avoid heavyweight dependencies and avoid high-frequency sampling.
<!-- spd:nfr-title repeat="many" -->

<!-- spd:####:prd-requirements -->

<!-- spd:####:adr-records -->
#### Architecture Decisions Records

<!-- spd:adr-title repeat="many" -->
##### Use CLI daemon + LaunchAgent (no menubar UI)

<!-- spd:id-ref:adr has="priority,task" -->
- [x] `p1` - `spd-overwork-alert-adr-cli-daemon-launchagent-no-menubar`
<!-- spd:id-ref:adr -->

The implementation is split into a long-running daemon and a short-lived CLI. This keeps v1 small and repository-friendly, enables autostart via LaunchAgent, and avoids UI lifecycle complexity.
<!-- spd:adr-title repeat="many" -->

<!-- spd:####:adr-records -->
<!-- spd:###:architecture-drivers -->

<!-- spd:###:architecture-layers -->
### Architecture Layers

<!-- spd:table:architecture-layers -->
| Layer | Responsibility | Technology |
|-------|---------------|------------|
| CLI / Control | User commands (status/pause/resume/reset), install/uninstall autostart | Python CLI (argparse), local IPC |
| Tracking Core | Idle-aware accumulation, over-limit state, reminder scheduling | Python daemon loop |
| OS Integration | Idle time signal, notification delivery, login autostart | `ioreg` idle time query, `osascript` notification, launchd LaunchAgent |
<!-- spd:table:architecture-layers -->
<!-- spd:###:architecture-layers -->
<!-- spd:##:architecture-overview -->

<!-- spd:##:principles-and-constraints -->
## 2. Principles & Constraints

<!-- spd:###:principles -->
### 2.1: Design Principles

<!-- spd:####:principle-title repeat="many" -->
#### Local-only and minimal state

<!-- spd:id:principle has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-principle-local-only-minimal-state`

<!-- spd:paragraph:principle-body -->
The tool must not require network services and should store only what is necessary to operate. Accumulated active time is kept in-memory only and resets on daemon restart.
<!-- spd:paragraph:principle-body -->
<!-- spd:id:principle -->
<!-- spd:####:principle-title repeat="many" -->

<!-- spd:####:principle-title repeat="many" -->
#### Predictable, explicit user control

<!-- spd:id:principle has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-principle-explicit-control`

<!-- spd:paragraph:principle-body -->
The system should not make time-based policy decisions like automatic midnight resets. Resetting and pausing are explicit user actions via the CLI.
<!-- spd:paragraph:principle-body -->
<!-- spd:id:principle -->
<!-- spd:####:principle-title repeat="many" -->

<!-- spd:####:principle-title repeat="many" -->
#### Low overhead background behavior

<!-- spd:id:principle has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-principle-low-overhead`

<!-- spd:paragraph:principle-body -->
The daemon must be suitable for always-on use: avoid tight loops, prefer coarse polling intervals, and keep OS interactions lightweight.
<!-- spd:paragraph:principle-body -->
<!-- spd:id:principle -->
<!-- spd:####:principle-title repeat="many" -->

<!-- spd:###:principles -->

<!-- spd:###:constraints -->
### 2.2: Constraints

<!-- spd:####:constraint-title repeat="many" -->
#### macOS-only, no custom UI surface

<!-- spd:id:constraint has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-constraint-macos-cli-only`

<!-- spd:paragraph:constraint-body -->
The v1 tool targets macOS only and is delivered as CLI + daemon; there is no menubar application or custom GUI.
<!-- spd:paragraph:constraint-body -->
<!-- spd:id:constraint -->
<!-- spd:####:constraint-title repeat="many" -->

<!-- spd:####:constraint-title repeat="many" -->
#### No automatic reset and no persistence of accumulated time

<!-- spd:id:constraint has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-constraint-no-auto-reset-no-persist`

<!-- spd:paragraph:constraint-body -->
Accumulated active work time is session-scoped: it resets when the daemon restarts and only resets during runtime when the user explicitly invokes manual reset.
<!-- spd:paragraph:constraint-body -->
<!-- spd:id:constraint -->
<!-- spd:####:constraint-title repeat="many" -->

<!-- spd:###:constraints -->
<!-- spd:##:principles-and-constraints -->

<!-- spd:##:technical-architecture -->
## 3. Technical Architecture

<!-- spd:###:domain-model -->
### 3.1: Domain Model

<!-- spd:paragraph:domain-model -->
Core types and invariants:

- `Config`: `limit_seconds`, `idle_threshold_seconds`, `repeat_interval_seconds`, and integration settings (e.g., socket path).
- `TrackerState`: `status` (running/paused), `active_time_seconds`, `over_limit_since`, `last_reminder_at`, `last_tick_at`.
- `IdleSample`: current `idle_seconds` observed from macOS.
- `ControlCommand`: one of `status`, `pause`, `resume`, `reset`, `stop`.

Invariants:

- `active_time_seconds` increases only while `status=running` and `idle_seconds < idle_threshold_seconds`.
- When `active_time_seconds > limit_seconds`, the system is considered “over limit” until a reset occurs.
- `reset` sets `active_time_seconds` to zero and clears over-limit reminder scheduling state.
<!-- spd:paragraph:domain-model -->
<!-- spd:###:domain-model -->

<!-- spd:###:component-model -->
### 3.2: Component Model

<!-- spd:code:component-model -->
```mermaid
graph LR
    U[User] --> CLI[CLI]
    CLI --> IPC[Local Control Channel]
    IPC --> D[Daemon]
    D --> IDLE[Idle Detector]
    D --> NOTIF[Notification Sender]
    D --> CFG[Config Loader]
    CLI --> LA[LaunchAgent Manager]
    LA --> launchd[(launchd)]
```
<!-- spd:code:component-model -->

<!-- spd:####:component-title repeat="many" -->
#### CLI

<!-- spd:id:component has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-component-cli`

<!-- spd:list:component-payload -->
- **Responsibilities**: Parse user commands; display status; send control commands to daemon; manage LaunchAgent installation.
- **Boundaries**: No tracking logic; no accumulation; no background loop.
- **Dependencies**: Control Channel; LaunchAgent Manager.
- **Key interfaces**: `overwork-alert status|pause|resume|reset|start|stop|install-autostart|uninstall-autostart`.
<!-- spd:list:component-payload -->
<!-- spd:id:component -->
<!-- spd:####:component-title repeat="many" -->

<!-- spd:####:component-title repeat="many" -->
#### Daemon / Tracker Loop

<!-- spd:id:component has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-component-daemon`

<!-- spd:list:component-payload -->
- **Responsibilities**: Maintain in-memory `TrackerState`; run periodic tick loop; decide when to notify; respond to control commands.
- **Boundaries**: Does not persist accumulated time; does not render UI; avoids network I/O.
- **Dependencies**: Idle Detector; Notification Sender; Config Loader; Control Channel.
- **Key interfaces**: `tick(state, config, idle_sample) -> state`; `handle_command(cmd) -> response`.
<!-- spd:list:component-payload -->
<!-- spd:id:component -->
<!-- spd:####:component-title repeat="many" -->

<!-- spd:####:component-title repeat="many" -->
#### Local Control Channel

<!-- spd:id:component has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-component-control-channel`

<!-- spd:list:component-payload -->
- **Responsibilities**: Provide local-only communication between CLI and daemon.
- **Boundaries**: Not remotely accessible; does not require privileged ports.
- **Dependencies**: OS sockets.
- **Key interfaces**: Request/response messages for `status`, `pause`, `resume`, `reset`, and `stop`.
<!-- spd:list:component-payload -->
<!-- spd:id:component -->
<!-- spd:####:component-title repeat="many" -->

<!-- spd:####:component-title repeat="many" -->
#### Idle Detector

<!-- spd:id:component has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-component-idle-detector`

<!-- spd:list:component-payload -->
- **Responsibilities**: Query macOS for current idle duration and return an `IdleSample`.
- **Boundaries**: Best-effort; failures return an error that the daemon treats as “unknown idle” and skips accumulation for that tick.
- **Dependencies**: `ioreg` (IOHIDSystem) via subprocess.
- **Key interfaces**: `get_idle_seconds() -> int`.
<!-- spd:list:component-payload -->
<!-- spd:id:component -->
<!-- spd:####:component-title repeat="many" -->

<!-- spd:####:component-title repeat="many" -->
#### Notification Sender

<!-- spd:id:component has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-component-notifier`

<!-- spd:list:component-payload -->
- **Responsibilities**: Deliver a macOS user notification for over-limit alerts.
- **Boundaries**: Best-effort; failures do not stop tracking.
- **Dependencies**: `osascript` (AppleScript) via subprocess.
- **Key interfaces**: `notify(title, message) -> None`.
<!-- spd:list:component-payload -->
<!-- spd:id:component -->
<!-- spd:####:component-title repeat="many" -->

<!-- spd:####:component-title repeat="many" -->
#### Config Loader

<!-- spd:id:component has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-component-config-loader`

<!-- spd:list:component-payload -->
- **Responsibilities**: Load configuration from a local file and apply defaults.
- **Boundaries**: No remote configuration; invalid values result in safe fallback behavior.
- **Dependencies**: Local file system; Python stdlib config parsing.
- **Key interfaces**: `load_config() -> Config`.
<!-- spd:list:component-payload -->
<!-- spd:id:component -->
<!-- spd:####:component-title repeat="many" -->

<!-- spd:####:component-title repeat="many" -->
#### LaunchAgent Manager

<!-- spd:id:component has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-component-launchagent-manager`

<!-- spd:list:component-payload -->
- **Responsibilities**: Install/uninstall a user LaunchAgent plist for autostart; start/stop the LaunchAgent.
- **Boundaries**: User-level LaunchAgent only (no system-wide daemon).
- **Dependencies**: `launchctl` and LaunchAgent plist format.
- **Key interfaces**: `install()`, `uninstall()`, `start()`, `stop()`.
<!-- spd:list:component-payload -->
<!-- spd:id:component -->
<!-- spd:####:component-title repeat="many" -->

<!-- spd:###:component-model -->

<!-- spd:###:api-contracts -->
### 3.3: API Contracts

<!-- spd:paragraph:api-contracts -->
External surface area is the CLI plus a local-only control contract between CLI and daemon.

CLI contract (high level):

- `overwork-alert start`: start daemon (foreground for dev, or as LaunchAgent).
- `overwork-alert status`: show `TrackerState` (active time, limit, paused/running, over-limit flag).
- `overwork-alert pause|resume`: toggle `TrackerState.status`.
- `overwork-alert reset`: clear session accumulation and reminder state.
- `overwork-alert stop`: stop daemon.
- `overwork-alert install-autostart|uninstall-autostart`: manage LaunchAgent.

Control channel contract (high level): request/response messages encoded as JSON. Example request:

`{"cmd":"status"}`

Example response:

`{"status":"running","active_time_seconds":5400,"limit_seconds":10800,"over_limit":false}`
<!-- spd:paragraph:api-contracts -->
<!-- spd:###:api-contracts -->

<!-- spd:###:interactions -->
### 3.4: Interactions & Sequences

<!-- spd:####:sequence-title repeat="many" -->
#### Run tracker and receive an overwork alert

<!-- spd:id:seq has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-seq-run-and-alert`

<!-- spd:code:sequences -->
```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI
    participant D as Daemon
    participant IDLE as Idle Detector
    participant N as Notifier

    U->>CLI: start
    CLI->>D: launch (foreground or via LaunchAgent)
    loop every tick
        D->>IDLE: get_idle_seconds
        IDLE-->>D: idle_seconds
        D->>D: accumulate active_time if idle < threshold
        alt active_time > limit
            D->>N: notify(over-limit)
        end
    end
```
<!-- spd:code:sequences -->

<!-- spd:paragraph:sequence-body -->
The user starts the tracker. The daemon periodically samples idle time and increments active time only when the user is not idle beyond threshold. When the configured limit is exceeded, the daemon sends a macOS notification and schedules repeats at the configured interval while the user remains active and tracking is running.
<!-- spd:paragraph:sequence-body -->
<!-- spd:id:seq -->
<!-- spd:####:sequence-title repeat="many" -->

<!-- spd:####:sequence-title repeat="many" -->
#### Reset a session via CLI

<!-- spd:id:seq has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-seq-cli-reset`

<!-- spd:code:sequences -->
```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI
    participant IPC as Control Channel
    participant D as Daemon

    U->>CLI: reset
    CLI->>IPC: {cmd: "reset"}
    IPC->>D: reset command
    D->>D: clear active_time + reminders
    D-->>IPC: {ok: true}
    IPC-->>CLI: {ok: true}
    CLI-->>U: confirmation
```
<!-- spd:code:sequences -->

<!-- spd:paragraph:sequence-body -->
The user issues a reset command. The CLI sends a local control request to the daemon, which clears the in-memory accumulated active time and reminder scheduling state.
<!-- spd:paragraph:sequence-body -->
<!-- spd:id:seq -->
<!-- spd:####:sequence-title repeat="many" -->

<!-- spd:###:interactions -->

<!-- spd:###:database -->
### 3.5 Database schemas & tables (optional)

No persistent database is used in v1. The following “tables” describe the conceptual runtime data model that is held in memory only.

<!-- spd:####:db-table-title repeat="many" -->
#### Table tracker_state (conceptual; in-memory only)

<!-- spd:id:dbtable has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-dbtable-tracker-state`

**Schema**
<!-- spd:table:db-table-schema -->
| Column | Type | Description |
|--------|------|-------------|
| status | string | `running` or `paused` |
| active_time_seconds | integer | Accumulated active time for the current daemon session |
| limit_seconds | integer | Effective configured limit used for comparisons |
| over_limit_since | string | ISO-8601 timestamp when the session first exceeded the limit, or empty |
| last_reminder_at | string | ISO-8601 timestamp when the last over-limit reminder was sent, or empty |
<!-- spd:table:db-table-schema -->

**PK**: N/A (in-memory struct)

**Constraints**: `active_time_seconds >= 0`, `limit_seconds > 0`

**Additional info**: Resets on daemon restart; `reset` clears `active_time_seconds`, `over_limit_since`, and `last_reminder_at`.

**Example**
<!-- spd:table:db-table-example -->
| status | active_time_seconds | limit_seconds | over_limit_since | last_reminder_at |
|--------|---------------------|--------------|------------------|-----------------|
| running | 5400 | 10800 |  |  |
<!-- spd:table:db-table-example -->
<!-- spd:id:dbtable -->
<!-- spd:####:db-table-title repeat="many" -->

<!-- spd:####:db-table-title repeat="many" -->
#### Table config (conceptual; file-backed)

<!-- spd:id:dbtable has="priority,task" covered_by="DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-dbtable-config`

**Schema**
<!-- spd:table:db-table-schema -->
| Column | Type | Description |
|--------|------|-------------|
| limit_seconds | integer | Work-time limit threshold |
| idle_threshold_seconds | integer | Idle threshold after which accumulation pauses |
| repeat_interval_seconds | integer | Reminder repeat interval after first over-limit alert |
| control_socket_path | string | Filesystem path to local control socket |
<!-- spd:table:db-table-schema -->

**PK**: N/A (single config document)

**Constraints**: All numeric values must be positive. Missing/invalid values fall back to safe defaults.

**Additional info**: Stored as a local configuration file; changes apply after daemon restart (v1).

**Example**
<!-- spd:table:db-table-example -->
| limit_seconds | idle_threshold_seconds | repeat_interval_seconds | control_socket_path |
|--------------|------------------------|------------------------|---------------------|
| 10800 | 300 | 1800 | /tmp/overwork-alert.sock |
<!-- spd:table:db-table-example -->
<!-- spd:id:dbtable -->
<!-- spd:####:db-table-title repeat="many" -->

<!-- spd:###:database -->

<!-- spd:###:topology -->
### 3.6: Topology (optional)

<!-- spd:id:topology has="task" -->
- [x] **ID**: `spd-overwork-alert-topology-single-daemon`

<!-- spd:free:topology-body -->
A single user-level daemon process runs per logged-in user session. The CLI runs as short-lived processes that communicate with the daemon over a local-only control channel. Autostart is provided by a user LaunchAgent.
<!-- spd:free:topology-body -->
<!-- spd:id:topology -->
<!-- spd:###:topology -->

<!-- spd:###:tech-stack -->
### 3.7: Tech stack (optional)

<!-- spd:paragraph:status -->
**Status**: Accepted
<!-- spd:paragraph:status -->

<!-- spd:paragraph:tech-body -->
Python 3.13+ using the standard library for the daemon loop, CLI, IPC, and configuration parsing. macOS integration is done via `launchd` (LaunchAgent plist + `launchctl`), idle time querying via `ioreg`, and Notification Center delivery via `osascript`.
<!-- spd:paragraph:tech-body -->
<!-- spd:###:tech-stack -->
<!-- spd:##:technical-architecture -->

<!-- spd:##:design-context -->
## 4. Additional Context

<!-- spd:free:design-context-body -->
- PRD: `examples/overwork_alert/architecture/PRD.md`
- ADR-0001: `examples/overwork_alert/architecture/ADR/general/0001-spd-overwork-alert-adr-cli-daemon-launchagent-no-menubar-v1.md`
<!-- spd:free:design-context-body -->

<!-- spd:paragraph:date -->
**Date**: 2026-02-06
<!-- spd:paragraph:date -->
<!-- spd:##:design-context -->

<!-- spd:#:design -->
