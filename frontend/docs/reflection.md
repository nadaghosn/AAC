Reflection - Tag

## 1. AI tools	
The 4 tools were used: ChatGPT, Claude, Cursor IDE and VS code with GitHub copilot.

With ChatGPT and Claude, we need to specify the role, the context, the needed tasks, the requirements and constraints. 
ChatGPT was used to create user stories. Claude was used for generation of skeletons, and revision of structured prompts.  

Using Cursor IDE and VS Code/GitHub Copilot, we benefit from the ability of these programs to read the application and files. Here the agent is able to read, summarize the content of the application and suggest solutions. The prompts are usually inline prompt.
Cursor IDE was used for the backend. VS Code/GitHub Copilot was used for the frontend.

## 2. AI helped	
AI helped in the following:
-	Creation of user stories
-	Reading my file and application
-	Updating the structured prompts and inline prompts
-	Generation of new tests
-	Checking for errors and suggesting solutions
-	Preparing the backend and the frontend
-	Updating the modal form

The most help was in updating the application files to integrate the new features, and in creating the tests (the py files).

## 3. AI failed	
AI had some failure in the following:
-	Creation of redundant scenarios
-	Suggestion of solutions that are not solving the errors…

For tag fature: 
One moment AI slowed it down, is when I couldnot update the task in frontend. The error mentioned that status transitions in same status was not valid. I have tried to add manually the needed status transitions in the business_rules.py (todo -> todo inprogress -> inprogress, done -> done). I have asked the VS Code agent to find the error. But it failed. He was suggesting removing the added transitions (todo -> todo inprogress -> inprogress, done -> done). Finally, I moved to Claude and provided me with the needed solutions including the needed status transitions.

## 4. My review
For tag feature:
One place where my review changed the result is when asking for more tests from VS Code. It provided me with scenarios already present in the test_tasks.py. Here, I rejected the agent scenarios and focused on the tests from test_tasks.py 


