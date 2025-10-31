NEXT STEPS (for candidates)

Use this file to document:
- Trade-offs you made due to timebox.
- Known limitations or TODOs you would address next.
- Ideas for tests, performance, design layering, or CI enhancements.

Initial plan:
- Create WaterModel class containing core functions from the run method().
- Create DatasetIO class containing the main read and write functions for the input data and final simulation results.
- Check where to incorporate the application configuration.
- Evaluate where to locate each class.

Template
- What I finished:
  - Refactored the run_all() method where the simulation occurs into a class.
  - During refactoring, fixed two bugs:
    * Unit conversion + evaluated its correctness with the testsuite.
    * Mixing implementation + evaluated its correctness with the testsuite.
- What I would do next if I had more time:
  - Correctly use poetry. I lost around 30-45 minutes trying to understand this tool and how to use it.
- Risks/assumptions:
  - 
- Notes for reviewers:
  - ...
