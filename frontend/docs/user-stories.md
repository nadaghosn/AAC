## Feature 1: Selected feature: Tags/labels

## prompt to generate stories using ChatGPT
Generate user stories related to tags for the mid-course-project for Task Tracker in the same format and quality as this example.

Example:
Story: As a team member, I want to add a tag to a task so that I can filter tasks. 

Acceptance Criteria:
-	Tags as list or normalized comma-separated field. 
-	Tags are mandatory; missing or blank title returns HTTP 422.
-	A created task appears in the task list with title, id, status, priority, description, assignee, and tags. 
Now generate five more stories in the same format.

Constraints:
-	Use "team member" as the user role.
-	Do not mention login, authentication, user accounts, admin roles, notifications, mobile, or real-time updates.
-	Include at least one failure case across the generated stories.


Output format:
Return each story with ID, Story and Acceptance Criteria headings.


## initial user stories (generated from ChatGPT)
Here are five tag-focused user stories with IDs, matching the requested format and level of detail.
ID: TAG-002
Story:
As a team member, I want to edit the tags on a task so that I can keep task categories accurate.
Acceptance Criteria:
•	A team member can add, remove, or replace tags on an existing task.
•	Tags are stored as a list or normalized comma-separated field.
•	Updated tags are persisted and displayed with the task.
•	Updating tags for a task that does not exist returns HTTP 404.
________________________________________
ID: TAG-003
Story:
As a team member, I want to filter tasks by tag so that I can quickly find related tasks.
Acceptance Criteria:
•	A team member can filter the task list using a tag.
•	Only tasks containing the selected tag are returned.
•	The filtered task list includes title, id, status, priority, description, assignee, and tags.
•	Filtering by a tag that does not exist returns an empty task list.
________________________________________
ID: TAG-004
Story:
As a team member, I want to remove a tag from a task so that outdated categories are no longer associated with it.
Acceptance Criteria:
•	A team member can remove an existing tag from a task.
•	The removed tag no longer appears in the task's tag list.
•	Other task tags remain unchanged.
•	Removing a tag from a task that does not exist returns HTTP 404.
________________________________________
ID: TAG-005
Story:
As a team member, I want to prevent duplicate tags on a task so that task categorization remains consistent.
Acceptance Criteria:
•	A task cannot contain the same tag more than once.
•	Adding an existing tag does not create a duplicate entry.
•	Tags are compared consistently when checking for duplicates.
•	A blank tag value returns HTTP 422.
________________________________________
ID: TAG-006
Story:
As a team member, I want to search tasks by tag so that I can find tasks belonging to a specific category.
Acceptance Criteria:
•	A team member can search for tasks using a tag value.
•	Search results include title, id, status, priority, description, assignee, and tags.
•	Tasks containing the requested tag are included in the results.
•	A blank tag search returns HTTP 422.

## correction
TAG-004: to correct
In story TAG-004, you mentioned that team member can remove a tag from a task. But we cannot have empty field in the tag field. There is need to have at least one tag per task.
Rewrite the story TAG-004 with the above needs


TAG-006: to remove
Similar to story TAG-003 

## user-stories after correction
ID: TAG-002
Story:
As a team member, I want to edit the tags on a task so that I can keep task categories accurate.
Acceptance Criteria:
•	A team member can add, remove, or replace tags on an existing task.
•	Tags are stored as a list or normalized comma-separated field.
•	Updated tags are persisted and displayed with the task.
•	Updating tags for a task that does not exist returns HTTP 404.
________________________________________
ID: TAG-003
Story:
As a team member, I want to filter tasks by tag so that I can quickly find related tasks.
Acceptance Criteria:
•	A team member can filter the task list using a tag.
•	Only tasks containing the selected tag are returned.
•	The filtered task list includes title, id, status, priority, description, assignee, and tags.
•	Filtering by a tag that does not exist returns an empty task list.
________________________________________
ID: TAG-004 
Story:
As a team member, I want to replace or remove a tag from a task so that I can keep its categorization accurate while ensuring every task has at least one tag.
Acceptance Criteria:
•	A team member can remove an existing tag from a task only when at least one other tag remains.
•	A team member can replace an existing tag with another valid tag.
•	The tags field must contain at least one non-blank tag for every task.
•	Attempting to remove the only tag from a task returns HTTP 422.
•	Other tas
•	k information remains unchanged when a tag is removed or replaced.
________________________________________
ID: TAG-005
Story:
As a team member, I want to prevent duplicate tags on a task so that task categorization remains consistent.
Acceptance Criteria:
•	A task cannot contain the same tag more than once.
•	Adding an existing tag does not create a duplicate entry.
•	Tags are compared consistently when checking for duplicates.
•	A blank tag value returns HTTP 422.

