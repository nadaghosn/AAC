# AI Suggestions the User Rejected or Corrected

**1. Rejected the proposed "Running in a container" README section.**
When drafting new README sections, I proposed a full standalone "Running in a container" section (port mapping, health status checks, logs, shell access, env vars, no-orchestration note) as a suggested addition alongside the "API quick reference" table. The user rejected it outright: *"For the running in container, it is already in the 'run in docker'. No need to add it."* — correctly identifying that this content would have duplicated the existing "Run with Docker" section rather than adding new value. Nothing from that draft was added to the README.

**2. Trimmed the "API quick reference" section down to just the table.**
My original draft for the API quick reference included the endpoint table plus additional prose underneath — a caveat about 404 responses not being declared in the OpenAPI schema, and a note on PATCH/PUT comment parity — framed as "judgment calls you may want to weigh in on." The user corrected the scope directly: *"For the section on API Quick reference: i need only the table."* The extra caveats were dropped; only the bare method/path/description table was added to the README.
