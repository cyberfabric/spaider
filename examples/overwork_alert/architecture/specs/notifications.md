<!-- spd:#:spec -->
# Spec: Notifications

<!-- spd:id-ref:spec has="task" -->
- [x] - `spd-overwork-alert-spec-notifications`
<!-- spd:id-ref:spec -->

<!-- spd:##:context -->
## 1. Spec Context

<!-- spd:overview -->
### 1. Overview
This spec defines when and how the daemon notifies the user after exceeding the configured active-time limit. It covers the first alert and repeat reminders while the user remains active and tracking is running.

Key assumptions:
- Notification delivery is best-effort and may be suppressed by system settings.
- Notification scheduling state is held in memory and resets on daemon restart.

Configuration parameters (effective defaults in v1):
- limit_seconds: 10800 (3 hours)
- idle_threshold_seconds: 300 (5 minutes)
- repeat_interval_seconds: 1800 (30 minutes)

Acceptance criteria (timing):
- After the tracker first becomes over limit while RUNNING and user is active, the first notification MUST be delivered within 5 seconds.
- Repeat reminders MUST NOT occur more frequently than repeat_interval_seconds.
<!-- spd:overview -->

<!-- spd:paragraph:purpose -->
### 2. Purpose
Ensure the user receives timely, repeatable overwork alerts once the active-time limit is exceeded.
<!-- spd:paragraph:purpose -->

### 3. Actors
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
- `spd-overwork-alert-actor-macos`
<!-- spd:id-ref:actor -->

### 4. References
<!-- spd:list:references -->
- Overall Design: [DESIGN.md](../DESIGN.md)
- Related spec: tracker-core.md
<!-- spd:list:references -->
<!-- spd:##:context -->

<!-- spd:##:flows -->
## 2. Actor Flows

<!-- spd:###:flow-title repeat="many" -->
### Send first over-limit alert

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-notifications-flow-first-alert`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - Daemon observes active_time_seconds > limit_seconds - `inst-detect-over-limit`
2. [x] - `p1` - **IF** tracker status is not RUNNING **RETURN** do_not_notify - `inst-skip-on-not-running`
3. [x] - `p1` - **IF** current idle_seconds >= idle_threshold_seconds **RETURN** do_not_notify - `inst-skip-on-idle`
4. [x] - `p1` - **IF** over-limit has not been notified yet: - `inst-check-first-alert`
5. [x] - `p1` - Notification Sender delivers macOS notification (title + message) - `inst-send-notification`
6. [x] - `p1` - Daemon records over_limit_since and last_reminder_at - `inst-record-notify-state`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Send repeat reminder while still over limit

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-notifications-flow-repeat-reminder`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - Daemon is over limit and user remains active - `inst-still-over-limit`
2. [x] - `p1` - **IF** tracker status is not RUNNING **RETURN** do_not_notify - `inst-skip-repeat-on-not-running`
3. [x] - `p1` - **IF** current idle_seconds >= idle_threshold_seconds **RETURN** do_not_notify - `inst-skip-repeat-on-idle`
4. [x] - `p1` - **IF** now - last_reminder_at >= repeat_interval_seconds: - `inst-check-interval`
5. [x] - `p1` - Notification Sender delivers macOS reminder notification - `inst-send-reminder`
6. [x] - `p1` - Daemon updates last_reminder_at - `inst-update-last-reminder`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:##:flows -->

<!-- spd:##:algorithms -->
## 3. Algorithms

<!-- spd:###:algo-title repeat="many" -->
### Determine whether to send a notification

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-notifications-algo-should-notify`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - **IF** tracker status is not RUNNING **RETURN** do_not_notify - `inst-not-running`
2. [x] - `p1` - **IF** current idle_seconds >= idle_threshold_seconds **RETURN** do_not_notify - `inst-currently-idle`
3. [x] - `p1` - **IF** active_time_seconds <= limit_seconds **RETURN** do_not_notify - `inst-not-over-limit`
4. [x] - `p1` - **IF** first alert not sent yet **RETURN** notify_now - `inst-first-alert`
5. [x] - `p1` - **IF** now - last_reminder_at >= repeat_interval_seconds **RETURN** notify_now - `inst-repeat-alert`
6. [x] - `p1` - **RETURN** do_not_notify - `inst-default-no`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->

<!-- spd:##:algorithms -->

<!-- spd:##:states -->
## 4. States

<!-- spd:###:state-title repeat="many" -->
### Over-limit notification state

<!-- spd:id:state has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-notifications-state-over-limit`

<!-- spd:sdsl:state-transitions -->
1. [x] - `p1` - **FROM** UNDER_LIMIT **TO** OVER_LIMIT_FIRST_SENT **WHEN** first alert is delivered - `inst-transition-first`
2. [x] - `p1` - **FROM** OVER_LIMIT_FIRST_SENT **TO** OVER_LIMIT_REMINDING **WHEN** reminder is delivered - `inst-transition-remind`
3. [x] - `p1` - **FROM** OVER_LIMIT_REMINDING **TO** UNDER_LIMIT **WHEN** session is reset - `inst-transition-reset`
<!-- spd:sdsl:state-transitions -->
<!-- spd:id:state -->
<!-- spd:###:state-title repeat="many" -->

<!-- spd:##:states -->

<!-- spd:##:requirements -->
## 5. Definition of Done

<!-- spd:###:req-title repeat="many" -->
### Over-limit notifications and repeat reminders

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-overwork-alert-spec-notifications-req-alert-and-repeat`

<!-- spd:paragraph:req-body -->
When active time exceeds the configured limit while tracking is RUNNING and the user is active (idle below threshold), the system sends a macOS notification within 5 seconds. While the user remains active and over limit, the system repeats notifications at the configured repeat interval.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- Component: `spd-overwork-alert-component-notifier`
- Data: `spd-overwork-alert-dbtable-tracker-state`
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-overwork-alert-spec-notifications-flow-first-alert`
- `p1` - `spd-overwork-alert-spec-notifications-flow-repeat-reminder`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-overwork-alert-spec-notifications-algo-should-notify`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-overwork-alert-fr-notify-on-limit`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-overwork-alert-nfr-reliability`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-overwork-alert-principle-explicit-control`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-overwork-alert-constraint-no-auto-reset-no-persist`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-overwork-alert-component-notifier`
- `spd-overwork-alert-component-daemon`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-overwork-alert-seq-run-and-alert`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-overwork-alert-dbtable-tracker-state`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->

<!-- spd:##:requirements -->

<!-- spd:##:additional-context -->
## 6. Additional Context (optional)

<!-- spd:free:context-notes -->
If notifications cannot be delivered (suppressed by system settings or subprocess failures), tracking continues and the user can still query status via the CLI.

Out of scope / not applicable (v1):
- No persistence of notification scheduling state across daemon restarts.
- No escalation policy beyond repeat reminders (no sounds, no focus-mode overrides).
- No network calls; no remote push notifications.
<!-- spd:free:context-notes -->
<!-- spd:##:additional-context -->

<!-- spd:#:spec -->
