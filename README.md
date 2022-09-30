[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![testing: nose](https://img.shields.io/badge/testing-nose-blue.svg)](https://nose.readthedocs.io/en/latest/)

#  [Element Finance](https://element.fi) market simulation and analysis repository
This project is a work-in-progress. All code is provided as is and without guarantee.


## Testing
Testing is done with [nose](https://nose.readthedocs.io/en/latest). Install with `python3 -m pip install nose`; run from the repository root directory with `python3 -m nose`.

## Analysis repo git workflow:

We will follow the Rebase workflow that is used by the Element frontend team.
Commits to `main` should only be made in the form of squash merges from pull requests.
For example,

```
git checkout feature-branch
git add [files to be committed]
git commit -m 'Complete change summary'
```
_later, some new commits show up in main, so we rebase our branch_
```
git pull --rebase origin main
git push feature-branch
```
_now, we have completed our feature, so we create a PR to merge the branch into main_

Once the PR is approved, we perform a final rebase, if necessary, and then a *squash merge*. This means each PR results in a single commit to `main`.

If two people are working in a branch then you should `git pull --rebase origin feature-branch`  *before* `git push origin feature-branch`. We also recommend that you start each working session with a `pull` and end it with a `push`, so that your colleagues can work asynchronously while you are not.
