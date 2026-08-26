# Task Tracker code review summary

| Number ID | Claim | Evidence summary | Assumption to verify | Grade | Decision | Verification or decision |
|---:|---|---|---|---|---|---|
| 1 | The repo implements a task-management REST API with task CRUD, filters, and task-comment endpoints. | Routes cover task creation, listing, retrieval, partial update, deletion, and comments; listing accepts status, priority, and tag filters. | Endpoint behavior matches the handlers. | Useful | Retain | Run the existing API tests. |
| 2 | Task data is process-local and non-persistent. | Storage uses the module-level `_tasks` dictionary directly. | No startup code repopulates it. | Useful | Retain | Inspect startup/import paths if persistence is later added. |
| 3 | The API validates and normalizes task inputs. | Extra fields are forbidden; titles are trimmed and constrained; tags are normalized and de-duplicated. | Clients receive the intended validation-error responses. | Useful | Retain | Test invalid request payloads. |
| 4 | Workflow status changes are constrained. | Only the defined forward/backward and unchanged status pairs are allowed; PATCH invokes the validator. | The permitted transitions match product requirements. | Useful | Retain | Confirm workflow rules with the product owner. |
| 5 | A single-file browser Kanban UI consumes the API. | The frontend has three status columns and sends load/create/update/delete task requests. | Its API endpoint configuration fits the target environment. | Useful | Retain | Check frontend configuration in the intended deployment. |
