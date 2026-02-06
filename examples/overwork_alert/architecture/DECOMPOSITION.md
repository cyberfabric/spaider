<!-- spd:#:decomposition -->
# Decomposition: Overwork Alert

<!-- spd:##:overview -->
## 1. Overview

Overwork Alert is decomposed into a small set of specs aligned to the system’s major responsibilities: tracking core (idle-aware accumulation and configuration), notification policy and delivery, CLI control + local IPC, and launchd autostart.

**Decomposition Strategy**:
- Group by functional cohesion (each spec implements a coherent responsibility)
- Keep dependencies minimal and explicit (tracker core is the foundation)
- Ensure 100% coverage of DESIGN elements (components, sequences, and data model items assigned)
- Maintain mutual exclusivity (each component/sequence/data element is owned by a single spec)

<!-- spd:##:overview -->

<!-- spd:##:entries -->
## 2. Entries

**Overall implementation status:**
<!-- spd:id:status has="priority,task" -->
- [x] `p1` - **ID**: `spd-overwork-alert-status-overall`

<!-- spd:###:spec-title repeat="many" -->
### 1. [Tracking Core](specs/tracker-core.md) - HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-overwork-alert-spec-tracker-core`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Implement the daemon tracking loop and the idle-aware active-time accumulation model with safe configuration defaults.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: None
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Load configuration with safe defaults and validation
  - Sample macOS idle time and determine active vs idle
  - Maintain session-scoped in-memory tracker state (no persistence)
  - Accumulate active time only when running and not idle
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Persisting accumulated time across restarts
  - Automatic time-of-day resets
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-fr-track-active-time`
  - [x] `p1` - `spd-overwork-alert-fr-configurable-limit`
  - [x] `p1` - `spd-overwork-alert-nfr-privacy-local-only`
  - [x] `p2` - `spd-overwork-alert-nfr-low-overhead`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-principle-local-only-minimal-state`
  - [x] `p2` - `spd-overwork-alert-principle-low-overhead`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-constraint-no-auto-reset-no-persist`
  - [x] `p1` - `spd-overwork-alert-constraint-macos-cli-only`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - Config
  - TrackerState
  - IdleSample
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-component-daemon`
  - [x] `p2` - `spd-overwork-alert-component-idle-detector`
  - [x] `p2` - `spd-overwork-alert-component-config-loader`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `overwork-alert start`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-seq-run-and-alert`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-dbtable-tracker-state`
  - [x] `p2` - `spd-overwork-alert-dbtable-config`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 2. [Notifications](specs/notifications.md) - HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-overwork-alert-spec-notifications`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Send macOS notifications when the limit is exceeded and repeat reminders at the configured interval while over limit.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-overwork-alert-spec-tracker-core`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Determine over-limit condition from tracker state
  - Deliver macOS notification for first over-limit event
  - Repeat reminders while still over limit and user is active
  - Degrade gracefully if notifications fail
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Custom UI beyond system notifications
  - Persisting reminder history across restarts
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-fr-notify-on-limit`
  - [x] `p2` - `spd-overwork-alert-nfr-reliability`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-principle-explicit-control`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-constraint-no-auto-reset-no-persist`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - TrackerState
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-component-notifier`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - (none)
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-seq-run-and-alert`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-dbtable-tracker-state`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 3. [CLI Control + Local IPC](specs/cli-control.md) - MEDIUM

<!-- spd:id:spec has="priority,task" -->
- [x] `p2` - **ID**: `spd-overwork-alert-spec-cli-control`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Provide CLI commands for status/pause/resume/reset/stop and implement the local-only control channel between CLI and daemon.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-overwork-alert-spec-tracker-core`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - CLI command parsing and output formatting
  - Local IPC request/response protocol for control commands
  - Pause/resume/reset/stop control semantics
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Network-accessible API
  - Multi-user support
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-fr-cli-controls`
  - [x] `p2` - `spd-overwork-alert-fr-manual-reset`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-principle-explicit-control`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-constraint-macos-cli-only`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - TrackerState
  - ControlCommand
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-component-cli`
  - [x] `p2` - `spd-overwork-alert-component-control-channel`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `overwork-alert status`
  - `overwork-alert pause`
  - `overwork-alert resume`
  - `overwork-alert reset`
  - `overwork-alert stop`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-seq-cli-reset`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-dbtable-tracker-state`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 4. [Autostart (LaunchAgent)](specs/launchagent-autostart.md) - MEDIUM

<!-- spd:id:spec has="priority,task" -->
- [x] `p2` - **ID**: `spd-overwork-alert-spec-launchagent-autostart`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Allow the tool to start automatically at login via a user LaunchAgent and provide CLI commands to install/uninstall autostart.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-overwork-alert-spec-cli-control`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Generate LaunchAgent plist content for the daemon
  - Install/uninstall/start/stop the LaunchAgent using launchctl
  - Ensure user-level (not system-level) installation
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - System-wide daemon installation
  - Menubar UI integration
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-fr-autostart`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-principle-local-only-minimal-state`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-overwork-alert-constraint-macos-cli-only`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - Config
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-component-launchagent-manager`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `overwork-alert install-autostart`
  - `overwork-alert uninstall-autostart`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-seq-run-and-alert`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p2` - `spd-overwork-alert-dbtable-config`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:id:status -->
<!-- spd:##:entries -->
<!-- spd:#:decomposition -->
