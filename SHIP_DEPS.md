# How Dependencies Are Shipped

This plugin uses vim's compiled Python support to run Python code. However, as
part of this code, external Python modules are required. Namely, requests (for
downloading a WebDriver) and selenium (for rendering the HTML to an image).

An issue that was encountered during development was how to ship these
dependencies. This file was created to document the thought process behind how
to solve this problem.

## Options

1. Ship the packages bundled in a 3rdparty folder.
    - Pros
        - Very simple
    - Cons
        - Rigid
        - Packages may become out of date
        - 3rd party code included in repo

2. Add the relevant Git repos (at specific tags/versions) as submodules to the
project.
    - Pros
        - Moves 3rd party code out of repo
    - Cons
        - Rigid
        - Packages may become out of date
        - Includes irrelevant code (eg Selenium repo contains implementations
          in multiple languages)

3. Require the user to manually install the packages themselves
    - Note that vim Python is independent of any Python distribution installed
      on the host machine.
    - Pros
        - Python packages will be up to date
    - Cons
        - Requires manual installation by the user
        - Requires the user to have Python and pip installed
        - The user's Python version may not match vim Python

4. Automatically install modules if not already installed on local system
    - If packages found on system do nothing, else download packages (from
      either another repo or using pip)

## Chosen Method

Method 1. is currently being used.
I am open to suggestions.
