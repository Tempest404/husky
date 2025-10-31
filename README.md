Deltares Python Developer Take‑Home Test

##### Running the model:
- The simulation can be executed similar to the initial description: `python3 -m water_model.run_legacy`.
- The testSuite can be executed using: `PYTHONPATH="." python3 tests/test_legacy_bug.py`.

##### Main changes made:
- Performed a minor refactor in the main simulation function (run_all).
- Fixed two bugs:
  * Bug in the conversion from mm/day -> m3/s.
  * Bug in the mixing functionality.
- Changed the structure of the test suite using unittest.

##### What I wanted to do more (als described briefly in the NEXT_STEPS.md):
- Create DatasetIO class containing the main read and write functions for the input data and final simulation results.
- Check where to incorporate the application configuration.
- Evaluate the location of each class.
- Learn more about Poetry and properly integrate that into the project.

