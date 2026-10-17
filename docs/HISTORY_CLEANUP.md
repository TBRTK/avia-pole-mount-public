# History and publication

Audit snapshot: private `TBRTK/avia-pole-mount`, main at `f36eeeb0b89c758d7f15fa709191d412e8e53ff8`. Mixed-content files entered at `746a85a77749fd3d745c87b2d5a24d3b1368932a`. A deletion, cleanup branch, PR merge, squash merge or new tag does not erase original blobs.

## Preferred: preserve private original

Keep the original private. Publish only the separately exported cleaned directory/ZIP into a **new repository with a new root commit**. Do not fork the old repository, copy its `.git`, merge old branches, push old tags or upload private bundles/manufacturer files. The standalone ZIP excludes Git history. A private review PR is not a history-clean public repository.

The owner explicitly requested a separate public repository on 2026-10-17. This edition is published at [TBRTK/avia-pole-mount-public](https://github.com/TBRTK/avia-pole-mount-public) from the cleaned export with a new root commit. No original repository visibility or history is changed. [Publication record](PUBLICATION.md).

## Alternative: rewrite later

Destructive rewriting/force-pushing **has not been performed**. First verify the private full-history bundle/mirror, coordinate collaborators, record ref heads and decide how to handle PRs, releases, artifacts, forks, clones and caches. Commit hashes/signatures/links can change or break; old clones can reintroduce files.

Use an expendable fresh clone and a current history-filtering tool. Replace mixed-content FCStd files across all historical/renamed paths with clean counterparts, or remove them from that clone's history and re-add the retained clean user designs. Include affected manufacturer-derived media and all other affected blobs. Do not delete all CAD/STL/STEP indiscriminately: the user bracket designs must survive.

Check every reachable commit/ref and nested FCStd member; verify bracket equivalence and the exact proposed ref changes. Obtain approval for the final destructive rewrite/force-push plan. Use leases to preserve collaborator work; do not blindly mirror-force-push. Old refs/PRs, non-Git assets, forks and caches need separate handling, with no guarantee of erasing others' copies.

[GitHub's official removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) explains history mechanics/side effects for sensitive-data cases. Manufacturer-CAD rights are a different case; GitHub Support eligibility is not assumed.
