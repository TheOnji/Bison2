Bison2 - A FFXIV gear optimizer

Things to do:
- Create user interface with Streamlit
    - Setup the I/O interface
    - Create formatting style for UI
- Streamline and optimize functions
    - Implement multiprocessing to speed up calcs
    - Add spec input for GCD
    - Add spec input for substat targets
    - Add spec input for Gear choices

- Add functionality for all jobs and classes
    - Add in UI (done)
    - Add in core

- Add Class stat generator

- Add unit testing for modules

Grand idea
Instead of generating all possible materia combinations and check each and
every one of them. Why not generate only the allowed materia combinations
directly. This can be done by backtracking from the materia matrix of
each gearset.



Finished optimization
- Callable Food object
