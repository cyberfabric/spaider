<!-- spd:#:prd -->
# PRD

<!-- spd:##:overview -->
## 1. Overview

<!-- spd:paragraph:purpose -->
**Purpose**: Overwork Alert is a small macOS background tool that tracks your active work time and notifies you when you exceed a configurable limit. It exists to help you notice overwork early and take breaks before fatigue builds up.
<!-- spd:paragraph:purpose -->

<!-- spd:paragraph:context -->
Overwork Alert is a local-first, single-user productivity helper intended for developers and knowledge workers who regularly lose track of time during deep work.

It measures “work time” as **active time**: when you are idle longer than a configurable threshold, the timer pauses automatically and resumes when activity returns.
<!-- spd:paragraph:context -->

**Target Users**:
<!-- spd:list:target-users required="true" -->
- Developers who often work long focused sessions and want a clear “stop” reminder.
- Knowledge workers who want a simple session cap without a full time-tracking product.
- People practicing break routines (e.g., Pomodoro) who still need a long-session safety net.
<!-- spd:list:target-users -->

**Key Problems Solved**:
<!-- spd:list:key-problems required="true" -->
- Losing track of time during deep work, leading to skipped breaks and fatigue.
- Inconsistent break discipline because there is no reliable, automated reminder.
- Miscounting “work time” when stepping away, because idle time is not excluded.
<!-- spd:list:key-problems -->

**Success Criteria**:
<!-- spd:list:success-criteria required="true" -->
- Install and first-run setup completed in 10 minutes or less on macOS (baseline: N/A, target: v1.0).
- After exceeding the configured limit while active, the first alert appears within 5 seconds (baseline: N/A, target: v1.0).
- When idle exceeds the configured threshold, active-time accumulation pauses within 10 seconds (baseline: N/A, target: v1.0).
- Users can verify current status (active time, limit, paused state) via CLI in under 5 seconds (baseline: N/A, target: v1.0).
<!-- spd:list:success-criteria -->

**Capabilities**:
<!-- spd:list:capabilities required="true" -->
- Track active work time with idle-aware pausing.
- Configure work limit, idle threshold, and reminder repetition.
- Deliver macOS notifications when the limit is exceeded.
- Provide simple CLI controls to view status and control tracking.
- Optionally start automatically on user login.
<!-- spd:list:capabilities -->
<!-- spd:##:overview -->

<!-- spd:##:actors -->
## 2. Actors

<!-- spd:###:actor-title repeat="many" -->
### User

<!-- spd:id:actor has="task" -->
- [x] **ID**: `spd-overwork-alert-actor-user`

<!-- spd:paragraph:actor-role -->
**Role**: Wants to be notified when they have worked too long, adjust configuration, and control the tracker (status/pause/resume/reset).
<!-- spd:paragraph:actor-role -->
<!-- spd:id:actor -->
<!-- spd:###:actor-title repeat="many" -->

<!-- spd:###:actor-title repeat="many" -->
### macOS System

<!-- spd:id:actor has="task" -->
- [x] **ID**: `spd-overwork-alert-actor-macos`

<!-- spd:paragraph:actor-role -->
**Role**: Provides the runtime environment, surfaces user notifications, and exposes signals needed to estimate user idleness.
<!-- spd:paragraph:actor-role -->
<!-- spd:id:actor -->
<!-- spd:###:actor-title repeat="many" -->

<!-- spd:###:actor-title repeat="many" -->
### Login Background Runner

<!-- spd:id:actor has="task" -->
- [x] **ID**: `spd-overwork-alert-actor-login-runner`

<!-- spd:paragraph:actor-role -->
**Role**: Starts the tool automatically on login and keeps it running in the background for continuous tracking.
<!-- spd:paragraph:actor-role -->
<!-- spd:id:actor -->
<!-- spd:###:actor-title repeat="many" -->

<!-- spd:##:actors -->

<!-- spd:##:frs -->
## 3. Functional Requirements

<!-- spd:###:fr-title repeat="many" -->
### FR-001 Track active work time (idle-aware)

<!-- spd:id:fr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-fr-track-active-time`

<!-- spd:free:fr-summary -->
The system MUST track “active work time” for the user.

Active work time MUST pause when the user has been idle longer than the configured idle threshold, and MUST resume when activity returns.
<!-- spd:free:fr-summary -->

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
`spd-overwork-alert-actor-macos`
<!-- spd:id-ref:actor -->
<!-- spd:id:fr -->
<!-- spd:###:fr-title repeat="many" -->

<!-- spd:###:fr-title repeat="many" -->
### FR-002 Configure limit and idle threshold

<!-- spd:id:fr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-fr-configurable-limit`

<!-- spd:free:fr-summary -->
The system MUST allow the user to configure:

- A daily/session work-time limit (default: 3 hours).
- An idle threshold used to pause active time (default: 5 minutes).
- A repeat reminder interval after the first over-limit alert (default: 30 minutes).

Configuration MUST have safe defaults if no configuration is present.
<!-- spd:free:fr-summary -->

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->
<!-- spd:id:fr -->
<!-- spd:###:fr-title repeat="many" -->

<!-- spd:###:fr-title repeat="many" -->
### FR-003 Notify when limit is exceeded and repeat reminders

<!-- spd:id:fr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-fr-notify-on-limit`

<!-- spd:free:fr-summary -->
When the tracked active work time exceeds the configured limit, the system MUST notify the user.

If the user continues working while over the limit, the system MUST repeat notifications at the configured repeat interval until the user stops working (becomes idle) or manually pauses/resets tracking.
<!-- spd:free:fr-summary -->

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
`spd-overwork-alert-actor-macos`
<!-- spd:id-ref:actor -->
<!-- spd:id:fr -->
<!-- spd:###:fr-title repeat="many" -->

<!-- spd:###:fr-title repeat="many" -->
### FR-004 Manual reset (no automatic reset)

<!-- spd:id:fr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-fr-manual-reset`

<!-- spd:free:fr-summary -->
The system MUST provide a manual reset capability so the user can restart tracking on demand.

The system MUST NOT automatically reset accumulated work time based on time-of-day in v1.
<!-- spd:free:fr-summary -->

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->
<!-- spd:id:fr -->
<!-- spd:###:fr-title repeat="many" -->

<!-- spd:###:fr-title repeat="many" -->
### FR-005 Run continuously in background and support autostart

<!-- spd:id:fr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-fr-autostart`

<!-- spd:free:fr-summary -->
The system MUST be able to run continuously in the background.

The system SHOULD support starting automatically at user login.
<!-- spd:free:fr-summary -->

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
`spd-overwork-alert-actor-login-runner`
<!-- spd:id-ref:actor -->
<!-- spd:id:fr -->
<!-- spd:###:fr-title repeat="many" -->

<!-- spd:###:fr-title repeat="many" -->
### FR-006 Provide CLI controls (status/pause/resume/reset)

<!-- spd:id:fr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-fr-cli-controls`

<!-- spd:free:fr-summary -->
The system MUST provide a CLI interface that allows the user to:

- Start the tracker.
- View current status (active time, limit, paused/active state).
- Pause and resume tracking.
- Reset the current day/session accumulation.
<!-- spd:free:fr-summary -->

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->
<!-- spd:id:fr -->
<!-- spd:###:fr-title repeat="many" -->

<!-- spd:##:frs -->

<!-- spd:##:usecases -->
## 4. Use Cases

<!-- spd:###:uc-title repeat="many" -->
### UC-001 Run tracker and receive an overwork alert

<!-- spd:id:usecase -->
**ID**: `spd-overwork-alert-usecase-run-and-alert`

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
`spd-overwork-alert-actor-macos`
<!-- spd:id-ref:actor -->

<!-- spd:paragraph:preconditions -->
**Preconditions**: The user has a running tracker session (started manually or via autostart).
<!-- spd:paragraph:preconditions -->

<!-- spd:paragraph:flow -->
**Flow**: Over-limit notification
<!-- spd:paragraph:flow -->

<!-- spd:numbered-list:flow-steps -->
1. The user works normally while the system accumulates active work time.
2. The user becomes idle longer than the idle threshold; the system pauses active-time accumulation.
3. The user returns to activity; the system resumes active-time accumulation.
4. The accumulated active work time exceeds the configured limit; the system sends an overwork notification.
5. If the user continues working while still over the limit, the system repeats notifications at the configured interval.
<!-- spd:numbered-list:flow-steps -->

<!-- spd:paragraph:postconditions -->
**Postconditions**: The user has been notified that the work-time limit was exceeded.
<!-- spd:paragraph:postconditions -->

**Alternative Flows**:
<!-- spd:list:alternative-flows -->
- **Configuration missing/invalid**: The system continues with safe defaults and the user can still receive alerts.
- **Notifications suppressed by system settings**: The system continues tracking and status remains available via CLI.
<!-- spd:list:alternative-flows -->
<!-- spd:id:usecase -->
<!-- spd:###:uc-title repeat="many" -->

<!-- spd:###:uc-title repeat="many" -->
### UC-002 Configure the limit

<!-- spd:id:usecase -->
**ID**: `spd-overwork-alert-usecase-configure-limit`

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:paragraph:preconditions -->
**Preconditions**: The user has access to the tool’s configuration mechanism.
<!-- spd:paragraph:preconditions -->

<!-- spd:paragraph:flow -->
**Flow**: Adjust configuration
<!-- spd:paragraph:flow -->

<!-- spd:numbered-list:flow-steps -->
1. The user updates the configured limit and/or idle threshold.
2. The user restarts the tracker or triggers a configuration reload (as supported by the CLI).
3. The system uses the new configuration for subsequent tracking and alerts.
<!-- spd:numbered-list:flow-steps -->

<!-- spd:paragraph:postconditions -->
**Postconditions**: The updated configuration is in effect for tracking and notifications.
<!-- spd:paragraph:postconditions -->

**Alternative Flows**:
<!-- spd:list:alternative-flows -->
- **Invalid values**: The system rejects invalid configuration and continues using the last known good configuration.
<!-- spd:list:alternative-flows -->
<!-- spd:id:usecase -->
<!-- spd:###:uc-title repeat="many" -->

<!-- spd:###:uc-title repeat="many" -->
### UC-003 Pause, resume, and reset a session

<!-- spd:id:usecase -->
**ID**: `spd-overwork-alert-usecase-control-session`

**Actors**:
<!-- spd:id-ref:actor -->
`spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:paragraph:preconditions -->
**Preconditions**: The tracker is running.
<!-- spd:paragraph:preconditions -->

<!-- spd:paragraph:flow -->
**Flow**: Control the tracker
<!-- spd:paragraph:flow -->

<!-- spd:numbered-list:flow-steps -->
1. The user checks current status via CLI.
2. The user pauses tracking (e.g., during meetings or non-work time).
3. The user resumes tracking when ready.
4. The user resets tracking to restart accumulation for the day/session.
<!-- spd:numbered-list:flow-steps -->

<!-- spd:paragraph:postconditions -->
**Postconditions**: The tracker state reflects the user’s control actions (paused/resumed/reset).
<!-- spd:paragraph:postconditions -->

**Alternative Flows**:
<!-- spd:list:alternative-flows -->
- **Tracker not running**: The CLI reports the tracker is not active and provides guidance to start it.
<!-- spd:list:alternative-flows -->
<!-- spd:id:usecase -->
<!-- spd:###:uc-title repeat="many" -->

<!-- spd:##:usecases -->

<!-- spd:##:nfrs -->
## 5. Non-functional requirements

<!-- spd:###:nfr-title repeat="many" -->
### Privacy & Data Handling

<!-- spd:id:nfr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p1` - **ID**: `spd-overwork-alert-nfr-privacy-local-only`

<!-- spd:list:nfr-statements -->
- The system MUST be local-first and MUST NOT send tracking data over the network by default.
- The system MUST store only minimal local state required to implement tracking and alerting.
<!-- spd:list:nfr-statements -->
<!-- spd:id:nfr -->
<!-- spd:###:nfr-title repeat="many" -->

<!-- spd:###:nfr-title repeat="many" -->
### Reliability

<!-- spd:id:nfr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-nfr-reliability`

<!-- spd:list:nfr-statements -->
- The system SHOULD degrade gracefully if notifications cannot be delivered (tracking continues, CLI status remains available).
<!-- spd:list:nfr-statements -->
<!-- spd:id:nfr -->
<!-- spd:###:nfr-title repeat="many" -->

<!-- spd:###:nfr-title repeat="many" -->
### Performance & Resource Usage

<!-- spd:id:nfr has="priority,task" covered_by="DESIGN,DECOMPOSITION,SPEC" -->
- [x] `p2` - **ID**: `spd-overwork-alert-nfr-low-overhead`

<!-- spd:list:nfr-statements -->
- The system SHOULD be low-overhead and suitable for always-on background usage.
- The system SHOULD avoid high-frequency polling that would noticeably impact CPU or battery.
<!-- spd:list:nfr-statements -->
<!-- spd:id:nfr -->
<!-- spd:###:nfr-title repeat="many" -->

<!-- spd:###:intentional-exclusions -->
### Intentional Exclusions

<!-- spd:list:exclusions -->
- **Accessibility** (UX-PRD-002): Not applicable — there is no custom UI surface in v1 beyond CLI and system notifications.
- **Internationalization** (UX-PRD-003): Not applicable — this is an example tool with English-only messages in v1.
- **Regulatory compliance** (COMPL-PRD-001): Not applicable — the tool does not process user-provided PII beyond local timestamps for tracking.
<!-- spd:list:exclusions -->
<!-- spd:###:intentional-exclusions -->
<!-- spd:##:nfrs -->

<!-- spd:##:nongoals -->
## 6. Non-Goals & Risks

<!-- spd:###:nongoals-title -->
### Non-Goals

<!-- spd:list:nongoals -->
- Not a full-featured time tracking or billing product.
- Not a cross-platform tool in v1.
- Not a menubar UI application in v1.
<!-- spd:list:nongoals -->
<!-- spd:###:nongoals-title -->

<!-- spd:###:risks-title -->
### Risks

<!-- spd:list:risks -->
- **Notification suppression**: macOS Focus modes or notification permissions may suppress alerts; mitigation is to provide clear setup guidance and always keep CLI status available.
- **Idle signal variability**: Idle measurement behavior may vary across macOS versions; mitigation is to test and document supported versions and known limitations.
<!-- spd:list:risks -->
<!-- spd:###:risks-title -->
<!-- spd:##:nongoals -->

<!-- spd:##:assumptions -->
## 7. Assumptions & Open Questions

<!-- spd:###:assumptions-title -->
### Assumptions

<!-- spd:list:assumptions -->
- The user is running macOS and permits notifications for this tool; if not, the tool still provides status via CLI.
- The user accepts a background process that runs continuously when enabled.
<!-- spd:list:assumptions -->
<!-- spd:###:assumptions-title -->

<!-- spd:###:open-questions-title -->
### Open Questions

<!-- spd:list:open-questions -->
- Should screen lock be treated as immediate idle regardless of the idle threshold? — Owner: User, Target: next iteration
- Should notifications include sound by default, or be notification-only? — Owner: User, Target: next iteration
<!-- spd:list:open-questions -->
<!-- spd:###:open-questions-title -->
<!-- spd:##:assumptions -->

<!-- spd:##:context -->
## 8. Additional context

<!-- spd:###:context-title repeat="many" -->
### Example Scope Notes

<!-- spd:free:prd-context-notes -->
This PRD is intentionally scoped as a minimal “end-to-end Spaider SDLC” example within the Spaider repository.
<!-- spd:free:prd-context-notes -->
<!-- spd:###:context-title repeat="many" -->

<!-- spd:##:context -->
<!-- spd:#:prd -->
