<!-- spd:#:spec -->
# Spec: LaunchAgent Autostart

<!-- spd:id-ref:spec has="task" -->
- [x] - `spd-overwork-alert-spec-launchagent-autostart`
<!-- spd:id-ref:spec -->

<!-- spd:##:context -->
## 1. Spec Context

<!-- spd:overview -->
### 1. Overview
This spec defines how the tool is started automatically on user login using a macOS user LaunchAgent, and how the CLI installs and uninstalls that LaunchAgent.

Key assumptions:
- Autostart is implemented using user-level LaunchAgents only.
- The daemon remains a CLI-launched process; there is no custom UI.

Acceptance criteria:
- Installing autostart MUST be idempotent (running install twice results in a single installed LaunchAgent).
- Uninstalling autostart MUST be idempotent (running uninstall when not installed succeeds with a clear message).
- After a successful install, the daemon MUST start automatically at the next user login.
<!-- spd:overview -->

<!-- spd:paragraph:purpose -->
### 2. Purpose
Allow the user to opt into login-time autostart so tracking can run continuously in the background.
<!-- spd:paragraph:purpose -->

### 3. Actors
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
- `spd-overwork-alert-actor-login-runner`
- `spd-overwork-alert-actor-macos`
<!-- spd:id-ref:actor -->

### 4. References
<!-- spd:list:references -->
- Overall Design: [DESIGN.md](../DESIGN.md)
- ADRs: `spd-overwork-alert-adr-cli-daemon-launchagent-no-menubar`
<!-- spd:list:references -->
<!-- spd:##:context -->

<!-- spd:##:flows -->
## 2. Actor Flows

<!-- spd:###:flow-title repeat="many" -->
### Install autostart

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-launchagent-autostart-flow-install`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - User runs `overwork-alert install-autostart` - `inst-run-install`
2. [x] - `p1` - **IF** LaunchAgent already installed: ensure it matches expected content and continue - `inst-install-idempotent`
3. [x] - `p1` - CLI builds LaunchAgent plist content using `spd-overwork-alert-spec-launchagent-autostart-algo-build-plist` - `inst-build-plist`
4. [x] - `p1` - CLI writes plist to the user LaunchAgents directory - `inst-write-plist`
5. [x] - `p1` - **IF** plist cannot be written: **RETURN** error - `inst-write-plist-error`
6. [x] - `p1` - CLI loads/starts LaunchAgent via launchctl - `inst-launchctl-load`
7. [x] - `p1` - **IF** launchctl fails: **RETURN** error - `inst-launchctl-load-error`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Uninstall autostart

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-launchagent-autostart-flow-uninstall`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-overwork-alert-actor-user`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - User runs `overwork-alert uninstall-autostart` - `inst-run-uninstall`
2. [x] - `p1` - **IF** LaunchAgent is not installed: **RETURN** ok (idempotent) - `inst-uninstall-idempotent`
3. [x] - `p1` - CLI stops/unloads LaunchAgent via launchctl - `inst-launchctl-unload`
4. [x] - `p1` - **IF** launchctl fails: continue to plist deletion and **RETURN** warning - `inst-launchctl-unload-warn`
5. [x] - `p1` - CLI deletes the LaunchAgent plist - `inst-delete-plist`
6. [x] - `p1` - **IF** plist cannot be deleted: **RETURN** error - `inst-delete-plist-error`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:##:flows -->

<!-- spd:##:algorithms -->
## 3. Algorithms

<!-- spd:###:algo-title repeat="many" -->
### Build LaunchAgent plist

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-launchagent-autostart-algo-build-plist`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - Choose a stable LaunchAgent label for the tool - `inst-choose-label`
2. [x] - `p1` - Set ProgramArguments to run the daemon start command - `inst-set-args`
3. [x] - `p1` - Set RunAtLoad=true and KeepAlive=true - `inst-set-options`
4. [x] - `p1` - Set launchd restart throttling options to avoid rapid crash loops - `inst-set-throttle`
5. [x] - `p1` - **RETURN** plist text content - `inst-return-plist`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->

<!-- spd:##:algorithms -->

<!-- spd:##:states -->
## 4. States

<!-- spd:###:state-title repeat="many" -->
### LaunchAgent installation state

<!-- spd:id:state has="task" to_code="true" -->
- [x] **ID**: `spd-overwork-alert-spec-launchagent-autostart-state-installation`

<!-- spd:sdsl:state-transitions -->
1. [x] - `p1` - **FROM** NOT_INSTALLED **TO** INSTALLED **WHEN** plist is written and launchctl load succeeds - `inst-transition-installed`
2. [x] - `p1` - **FROM** INSTALLED **TO** NOT_INSTALLED **WHEN** launchctl unload succeeds and plist is removed - `inst-transition-removed`
<!-- spd:sdsl:state-transitions -->
<!-- spd:id:state -->
<!-- spd:###:state-title repeat="many" -->

<!-- spd:##:states -->

<!-- spd:##:requirements -->
## 5. Definition of Done

<!-- spd:###:req-title repeat="many" -->
### Login autostart via user LaunchAgent

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-overwork-alert-spec-launchagent-autostart-req-install-and-run`

<!-- spd:paragraph:req-body -->
The user can install a LaunchAgent that starts the daemon at login. The user can also uninstall the LaunchAgent to disable autostart.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- Component: `spd-overwork-alert-component-launchagent-manager`
- Component: `spd-overwork-alert-component-cli`
- Data: `spd-overwork-alert-dbtable-config`
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-overwork-alert-spec-launchagent-autostart-flow-install`
- `p1` - `spd-overwork-alert-spec-launchagent-autostart-flow-uninstall`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-overwork-alert-spec-launchagent-autostart-algo-build-plist`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-overwork-alert-fr-autostart`
<!-- spd:id-ref:fr -->
 
<!-- spd:id-ref:nfr -->
- `spd-overwork-alert-nfr-privacy-local-only`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-overwork-alert-principle-local-only-minimal-state`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-overwork-alert-constraint-macos-cli-only`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-overwork-alert-component-launchagent-manager`
- `spd-overwork-alert-component-cli`
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
The exact LaunchAgent label and ProgramArguments are implementation details; they must remain stable so install/uninstall behaves predictably.

Out of scope / not applicable (v1):
- No system-wide (root) daemon installation.
- No automatic self-update or signed installer packaging.
- No network access and no privileged escalation.
<!-- spd:free:context-notes -->
<!-- spd:##:additional-context -->

<!-- spd:#:spec -->
