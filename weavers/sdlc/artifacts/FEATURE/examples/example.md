<!-- spd:#:feature-design -->
# Feature: Task CRUD

<!-- spd:id-ref:feature has="task" -->
[ ] - `spd-taskflow-feature-task-crud`
<!-- spd:id-ref:feature -->

<!-- spd:##:context -->
## A. Feature Context

<!-- spd:overview -->
### 1. Overview
Core task management functionality for creating, viewing, updating, and deleting tasks. This feature provides the foundation for team collaboration by enabling users to track work items through their lifecycle.

Problem: Teams need a central place to track tasks with status, priority, and assignments.
Primary value: Enables organized task tracking with clear ownership.
Key assumptions: Users have accounts and belong to at least one team.
<!-- spd:overview -->

<!-- spd:paragraph:purpose -->
### 2. Purpose
Enable team members to manage their work items with full lifecycle tracking from creation through completion.

Success criteria: Users can create, view, update, and delete tasks within 500ms response time.
<!-- spd:paragraph:purpose -->

### 3. Actors
<!-- spd:id-ref:actor -->
- `spd-taskflow-actor-member`
- `spd-taskflow-actor-lead`
<!-- spd:id-ref:actor -->

### 4. References
<!-- spd:list:references -->
- Overall Design: [DESIGN.md](../../DESIGN.md)
- ADRs: `spd-taskflow-adr-postgres-storage`
- Related feature: `spd-taskflow-feature-notifications`
<!-- spd:list:references -->
<!-- spd:##:context -->

<!-- spd:##:flows -->
## B. Actor Flows

<!-- spd:###:flow-title repeat="many" -->
### Create Task

<!-- spd:id:flow has="priority,task" to_code="true" -->
- [ ] `p1` - **ID**: `spd-taskflow-feature-task-crud-flow-create`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-taskflow-actor-member`
- `spd-taskflow-actor-lead`
<!-- spd:id-ref:actor -->

<!-- spd:fdl:flow-steps -->
1. [x] - `ph-1` - User fills task form (title, description, priority) - `inst-fill-form`
2. [x] - `ph-1` - API: POST /api/tasks (body: title, description, priority, due_date) - `inst-api-create`
3. [x] - `ph-1` - Algorithm: validate task input using `spd-taskflow-feature-task-crud-algo-validate` - `inst-run-validate`
4. [x] - `ph-1` - DB: INSERT tasks(title, description, priority, due_date, status=BACKLOG) - `inst-db-insert`
5. [ ] - `ph-2` - User optionally assigns task to team member - `inst-assign`
6. [ ] - `ph-2` - API: POST /api/tasks/{task_id}/assignees (body: assignee_id) - `inst-api-assign`
7. [ ] - `ph-2` - DB: INSERT task_assignees(task_id, assignee_id) - `inst-db-assign-insert`
8. [x] - `ph-1` - API: RETURN 201 Created (task_id, status=BACKLOG) - `inst-return-created`
<!-- spd:fdl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->
<!-- spd:##:flows -->

<!-- spd:##:algorithms -->
## C. Algorithms

<!-- spd:###:algo-title repeat="many" -->
### Validate Task

<!-- spd:id:algo has="priority,task" to_code="true" -->
- [ ] `p1` - **ID**: `spd-taskflow-feature-task-crud-algo-validate`

<!-- spd:fdl:algo-steps -->
1. [x] - `ph-1` - **IF** title is empty **RETURN** error "Title required" - `inst-check-title`
2. [x] - `ph-1` - **IF** priority not in [LOW, MEDIUM, HIGH] **RETURN** error - `inst-check-priority`
3. [x] - `ph-1` - **IF** due_date is present AND due_date is in the past **RETURN** error - `inst-check-due-date`
4. [x] - `ph-1` - DB: SELECT tasks WHERE title=? AND status!=DONE (dedupe check) - `inst-db-dedupe-check`
5. [ ] - `ph-2` - **IF** duplicate exists **RETURN** error - `inst-return-duplicate`
6. [x] - `ph-1` - **RETURN** valid - `inst-return-valid`
<!-- spd:fdl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->
<!-- spd:##:algorithms -->

<!-- spd:##:states -->
## D. States

<!-- spd:###:state-title repeat="many" -->
### Task Status

<!-- spd:id:state has="priority,task" to_code="true" -->
- [ ] `p1` - **ID**: `spd-taskflow-feature-task-crud-state-status`

<!-- spd:fdl:state-transitions -->
1. [x] - `ph-1` - **FROM** BACKLOG **TO** IN_PROGRESS **WHEN** user starts work - `inst-start`
2. [ ] - `ph-2` - **FROM** IN_PROGRESS **TO** DONE **WHEN** user completes - `inst-complete`
3. [ ] - `ph-2` - **FROM** DONE **TO** BACKLOG **WHEN** user reopens - `inst-reopen`
<!-- spd:fdl:state-transitions -->
<!-- spd:id:state -->
<!-- spd:###:state-title repeat="many" -->
<!-- spd:##:states -->

<!-- spd:##:requirements -->
## E. Requirements

<!-- spd:###:req-title repeat="many" -->
### Task Creation

<!-- spd:id:req has="priority,task" to_code="true" -->
- [ ] `p1` - **ID**: `spd-taskflow-feature-task-crud-req-create`

<!-- spd:paragraph:req-body -->
Users can create tasks with title, description, priority, and due date. The system validates input and stores the task with BACKLOG status.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- API: `POST /api/tasks` with JSON body `{title, description, priority, due_date}`
- DB: insert into `tasks` table (columns: title, description, priority, due_date, status)
- Domain: `Task` entity (id, title, description, priority, due_date, status)
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-taskflow-feature-task-crud-flow-create`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-taskflow-feature-task-crud-algo-validate`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-taskflow-fr-task-management`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-taskflow-nfr-performance`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-taskflow-principle-realtime-first`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-taskflow-constraint-supported-platforms`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-taskflow-component-api-server`
- `spd-taskflow-component-postgresql`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-taskflow-seq-task-creation`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-taskflow-dbtable-tasks`
<!-- spd:id-ref:dbtable -->
<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->
<!-- spd:##:requirements -->

<!-- spd:##:additional-context -->
## F. Additional Context (optional)

<!-- spd:free:context-notes -->
The feature must keep task status transitions consistent with the Task Status state machine in Section D. All state changes should emit events for the notification system.
<!-- spd:free:context-notes -->
<!-- spd:##:additional-context -->

<!-- spd:#:feature-design -->
