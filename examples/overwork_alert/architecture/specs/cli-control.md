<!-- spd:#:spec -->
# Spec: CLI Control

<!-- spd:id-ref:spec has="task" -->
- [x] - `spd-overwork-alert-spec-cli-control`
<!-- spd:id-ref:spec -->

<!-- spd:##:context -->
## 1. Spec Context

<!-- spd:overview -->
### 1. Overview
This spec defines user-facing CLI controls and the local-only control channel contract between the CLI and the daemon. It covers status reporting, pause/resume, manual reset, and stop.

Key assumptions:
- Control communication is local-only.
- Reset is explicit and does not happen automatically.

Control channel contract (v1):
- Transport: Unix domain socket at control_socket_path (default: /tmp/overwork-alert.sock)
- Encoding: JSON request/response
- Commands: status, pause, resume, reset, stop
- CLI timeout: 2 seconds

Error handling expectations:
- If the daemon is not running or the socket is unreachable, the CLI MUST return a clear error and non-zero exit.
- If a request times out or the response is invalid JSON, the CLI MUST return a clear error and non-zero exit.

Acceptance criteria (timing):
- status MUST return within 2 seconds when the daemon is healthy.
- reset MUST complete within 2 seconds when the daemon is healthy.
<!-- spd:overview -->

<!-- spd:paragraph:purpose -->
### 2. Purpose
Allow the user to inspect and control the tracker in a predictable, explicit manner using CLI commands.
<!-- spd:paragraph:purpose -->

### 3. Actors
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
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
### View status

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-cli-control-flow-status`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - User runs `overwork-alert status` - `inst-run-status`
2. [x] - `p1` - CLI sends local control request {cmd:"status"} - `inst-send-status-request`
3. [x] - `p1` - **IF** CLI cannot connect to daemon within timeout: **RETURN** error - `inst-status-daemon-unreachable`
4. [x] - `p1` - Daemon returns current TrackerState snapshot - `inst-return-status`
5. [x] - `p1` - **IF** response is invalid: **RETURN** error - `inst-status-invalid-response`
6. [x] - `p1` - CLI prints active time, limit, and paused/running state - `inst-print-status`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Reset session

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-cli-control-flow-reset`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - User runs `overwork-alert reset` - `inst-run-reset`
2. [x] - `p1` - CLI sends local control request {cmd:"reset"} - `inst-send-reset-request`
3. [x] - `p1` - **IF** CLI cannot connect to daemon within timeout: **RETURN** error - `inst-reset-daemon-unreachable`
4. [x] - `p1` - Daemon clears active_time_seconds and over-limit reminder state - `inst-clear-state`
5. [x] - `p1` - CLI prints confirmation - `inst-print-confirm`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Pause tracking

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-cli-control-flow-pause`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - User runs `overwork-alert pause` - `inst-run-pause`
2. [x] - `p1` - CLI sends local control request {cmd:"pause"} - `inst-send-pause-request`
3. [x] - `p1` - **IF** CLI cannot connect to daemon within timeout: **RETURN** error - `inst-pause-daemon-unreachable`
4. [x] - `p1` - Daemon sets TrackerState.status=PAUSED and **RETURN** ok - `inst-daemon-pause`
5. [x] - `p1` - CLI prints confirmation - `inst-print-pause-confirm`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Resume tracking

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-cli-control-flow-resume`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - User runs `overwork-alert resume` - `inst-run-resume`
2. [x] - `p1` - CLI sends local control request {cmd:"resume"} - `inst-send-resume-request`
3. [x] - `p1` - **IF** CLI cannot connect to daemon within timeout: **RETURN** error - `inst-resume-daemon-unreachable`
4. [x] - `p1` - Daemon sets TrackerState.status=RUNNING and **RETURN** ok - `inst-daemon-resume`
5. [x] - `p1` - CLI prints confirmation - `inst-print-resume-confirm`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Stop daemon

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-cli-control-flow-stop`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - User runs `overwork-alert stop` - `inst-run-stop`
2. [x] - `p1` - CLI sends local control request {cmd:"stop"} - `inst-send-stop-request`
3. [x] - `p1` - **IF** CLI cannot connect to daemon within timeout: **RETURN** error - `inst-stop-daemon-unreachable`
4. [x] - `p1` - Daemon begins graceful shutdown and **RETURN** ok - `inst-daemon-stop`
5. [x] - `p1` - CLI prints confirmation - `inst-print-stop-confirm`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:##:flows -->

<!-- spd:##:algorithms -->
## 3. Algorithms

<!-- spd:###:algo-title repeat="many" -->
### Handle control command

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-cli-control-algo-handle-command`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - Parse command from request payload - `inst-parse-cmd`
2. [x] - `p1` - **IF** cmd is missing or not recognized **RETURN** error - `inst-handle-invalid-cmd`
3. [x] - `p1` - **IF** cmd="status" **RETURN** current state snapshot - `inst-handle-status`
4. [x] - `p1` - **IF** cmd="pause" set status=PAUSED and **RETURN** ok - `inst-handle-pause`
5. [x] - `p1` - **IF** cmd="resume" set status=RUNNING and **RETURN** ok - `inst-handle-resume`
6. [x] - `p1` - **IF** cmd="reset" clear accumulation and **RETURN** ok - `inst-handle-reset`
7. [x] - `p1` - **IF** cmd="stop" request daemon shutdown and **RETURN** ok - `inst-handle-stop`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->

<!-- spd:##:algorithms -->

<!-- spd:##:states -->
## 4. States

<!-- spd:###:state-title repeat="many" -->
### Control channel request lifecycle

<!-- spd:id:state has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-cli-control-state-request-lifecycle`

<!-- spd:sdsl:state-transitions -->
1. [x] - `p1` - **FROM** RECEIVED **TO** VALIDATED **WHEN** request payload is parsed - `inst-transition-validated`
2. [x] - `p1` - **FROM** VALIDATED **TO** RESPONDED **WHEN** daemon sends response - `inst-transition-responded`
<!-- spd:sdsl:state-transitions -->
<!-- spd:id:state -->
<!-- spd:###:state-title repeat="many" -->

<!-- spd:##:states -->

<!-- spd:##:requirements -->
## 5. Definition of Done

<!-- spd:###:req-title repeat="many" -->
### Manual reset and CLI control semantics

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-overwork-alert-spec-cli-control-req-reset-and-controls`

<!-- spd:paragraph:req-body -->
The CLI must provide status, pause, resume, reset, and stop commands. Reset clears the in-memory accumulated active time and over-limit reminder state, and there is no automatic reset.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- Component: `spd-overwork-alert-component-cli`
- Component: `spd-overwork-alert-component-control-channel`
- Data: `spd-overwork-alert-dbtable-tracker-state`
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-overwork-alert-spec-cli-control-flow-status`
- `p1` - `spd-overwork-alert-spec-cli-control-flow-reset`
- `p1` - `spd-overwork-alert-spec-cli-control-flow-pause`
- `p1` - `spd-overwork-alert-spec-cli-control-flow-resume`
- `p1` - `spd-overwork-alert-spec-cli-control-flow-stop`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-overwork-alert-spec-cli-control-algo-handle-command`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-overwork-alert-fr-cli-controls`
- `spd-overwork-alert-fr-manual-reset`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-overwork-alert-nfr-privacy-local-only`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-overwork-alert-principle-explicit-control`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-overwork-alert-constraint-macos-cli-only`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-overwork-alert-component-cli`
- `spd-overwork-alert-component-control-channel`
- `spd-overwork-alert-component-daemon`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-overwork-alert-seq-cli-reset`
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
Pause/resume flows follow the same control channel pattern as reset/status and are handled by the same command handler algorithm.

Out of scope / not applicable (v1):
- No authentication/authorization beyond local-only transport and filesystem permissions on the Unix socket.
- No remote control interface; no TCP listener.
- No encryption in transit (local-only).
<!-- spd:free:context-notes -->
<!-- spd:##:additional-context -->

<!-- spd:#:spec -->
