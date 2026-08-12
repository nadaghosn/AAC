## Mini ADR

## Selected feature: Tags/labels (required feature)

## Implementation of the features:

-	Starting with the user-stories and correction with ChatGPT
-	Asking for 2 light weight architecture proposals from ChatGPT. Option A: json file local storage. Option B: SQLite local database. The selected option was A as simpler and less complex. Option A requires limited set up, no need to external database, query can be done with python, no need for SQL knowledge. 
-	Selecting one proposal: option A
-	Asking for ADR from ChatGPT. It included the context, the decision, the tree of files, the reasoning, the consequences.
-	Asking for skeleton from Claude. But this step did not add new items compared to the previous skeleton. The comparison between initial skeleton and later one shows no difference: same folders, same files. 
-	Asking Claude to revise the initial prompts related to models.py, storage.py, verify_a.py, conftest.py, test_task.py and to integrate the code needed for the new feature (tag). Here I updated my prompts. 
-	Working the application with Cursor IDE. First, I asked the agent to summarize application. Then I used the prompts updated by Claude to update the files: models.py, storage.py, verify_a.py, conftest.py, test_task.py
-	Testing the application from the backend using curl command lines. Adding a task with tag: passed. Adding a task without a tag: failed. Testing the test_tasks.py. 
-	Testing the application with test_tasks.py. All passed. Then selecting one test (tests/test_tasks.py -k test_patch_blank_tag_returns_422): passed. Then changing the models to have the tag optional. Retesting with the modification: failed. Restoration: passed.
-	Then working the application with VS code. With the agent I updated the kanban board to make visible the “tag” and later the “search”. There was no need to update the fetch url, render logic, UI states. Then I run the application from the frontend.
-	Testing the frontend using curl command lines. Adding a new task. I had some errors corrected by the agent (adding the tag in the frontend payload).
-	Then asking the agent to update the modal form. 
-	Testing the modal form. I had errors initially when updating the tasks in same status: an error when updating a task and keeping it in same status. I tried to fix the valid transitions to include (todo -> todo, inprogress -> inprogress, done-> done in the business_rules.py). With VS code, the errors remained. I asked Claude to correct the files, the code was fixed and the application worked. 
-	Testing again: new task, empty tag, preserve tag after unrelated update, filter. For filtering, Claude suggesting several options, I selected the simplest one “text search box”.
-	Refactoring. I prepared a repo for the application (before refactoting) in github under mid-course-project (add, commit, push). I asked the agent to write a kanban behavior contract. Then I focused on style, asking the agent to improve the style and use the green color instead of blue. Runing after refactor, the kanban turned green.
-	Then testing and debugging.  I asked the agent for 5 edge cases. There were very similar to each other, and similar to the ones in the test_tasks.py. I selected two tests from the test_tasks.py: they passed. I changed the code (breaking it). The tests failed. Then the tests were restored. I tried one test after one test. 
-	Then I updated the application on github. 
