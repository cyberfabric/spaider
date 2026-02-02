<!-- spd:#:adr -->
# ADR-0001: Use PostgreSQL for Task Storage

<!-- spd:id:adr has="priority,task" covered_by="DESIGN" -->
- [ ] `p1` - **ID**: `spd-taskflow-adr-postgres-storage`

<!-- spd:##:meta -->
## Meta

<!-- spd:paragraph:adr-title -->
**Title**: ADR-0001 Use PostgreSQL for Task Storage
<!-- spd:paragraph:adr-title -->

<!-- spd:paragraph:date -->
**Date**: 2025-01-10
<!-- spd:paragraph:date -->

<!-- spd:paragraph:status -->
**Status**: Accepted
<!-- spd:paragraph:status -->
<!-- spd:##:meta -->

<!-- spd:##:body -->
## Body

<!-- spd:context -->
**Context**:
TaskFlow needs persistent storage for tasks, users, and audit history. We need to choose between SQL and NoSQL databases considering query patterns, data relationships, and team expertise.

The system will handle:
- Task CRUD operations with complex filtering
- User and team relationships
- Assignment history and audit trail
- Real-time updates via change notifications
<!-- spd:context -->

<!-- spd:decision-drivers -->
**Decision Drivers**:
- Strong consistency required for task state transitions
- Relational queries needed for assignments and team structures
- Team has existing PostgreSQL expertise
- Operational maturity and hosting options important
<!-- spd:decision-drivers -->

<!-- spd:options repeat="many" -->
**Considered Options**:
1. **PostgreSQL** — Relational database with strong ACID guarantees, mature ecosystem, team expertise
2. **MongoDB** — Document store with flexible schema, good for rapid iteration, less suited for relational data
3. **SQLite** — Embedded database for simpler deployment, limited concurrent access, no built-in replication
<!-- spd:options -->

<!-- spd:decision-outcome -->
**Decision Outcome**:
Chosen option: **PostgreSQL**, because tasks have relational data (users, assignments, comments) that benefit from joins, strong consistency is needed for status transitions and assignments, team has existing PostgreSQL expertise, and it supports JSON columns for flexible metadata if needed later.
<!-- spd:decision-outcome -->

**Consequences**:
<!-- spd:list:consequences -->
- Positive: ACID transactions ensure data integrity during concurrent updates
- Positive: Efficient queries for filtering tasks by status, assignee, due date
- Negative: Requires separate database server (vs embedded SQLite)
- Negative: Schema migrations needed for model changes
- Follow-up: Set up connection pooling for scalability
<!-- spd:list:consequences -->

**Links**:
<!-- spd:list:links -->
- [`spd-taskflow-fr-task-management`](../PRD.md) — Primary requirement for task storage
- [`spd-taskflow-feature-task-crud`](../features/task-crud/DESIGN.md) — Feature implementing task persistence
<!-- spd:list:links -->
<!-- spd:##:body -->

<!-- spd:id:adr -->
<!-- spd:#:adr -->
