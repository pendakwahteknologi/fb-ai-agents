# The Business Portfolio mystery

## What happened

The standard Page Access Token tutorial — the one that appears on the first page of every Meta developer guide — does not work for our setup. We followed it carefully. The User Access Token issued correctly. The long-lived exchange succeeded. The call to `/me/accounts` returned an empty list.

The principal Page exists. The operator is an admin. The permissions are correct. The list was empty.

We spent several hours assuming we had configured something wrong. We had not.

## Why it happened

The principal Page (Pendakwah Teknologi) is not held under the operator's personal account. It is held inside a Business Portfolio. Pages held inside a Business Portfolio do not appear under `/me/accounts` unless the access token also has the `business_management` permission.

This is documented. The documentation is several layers deep, in a section that does not appear in any of the standard Page-token tutorials we found. The standard tutorials assume Pages held personally.

## What we learned

- **Meta's documentation layers reflect Meta's product layers.** Personal Pages, Business Portfolio Pages, Multi-Business Portfolio Pages, and Agency-managed Pages all have different code paths.
- **Empty results are not always empty.** A non-error empty list from a permissioned endpoint can mean "you do not have the permission to see what is there."
- **The `business_management` permission has a heavier review surface in App Review.** Because we operate in Development mode against our own assets, this is not a problem. For others pursuing App Review, it is significant.

## What we changed

- The token-acquisition tooling now checks both `/me/accounts` (personal Pages) and the Business Portfolio listing endpoint (Business Pages). It tries both, merges the results, and warns if either path returns empty when expected to return Pages.
- The setup documentation explicitly calls out the Business Portfolio path as the dominant case for production deployments.

## What we did not change

- We did not move the Page out of the Business Portfolio. Business Portfolio is the correct home for a corporate Page; the inconvenience of token discovery is not a reason to relocate it.
- We did not request additional permissions beyond `business_management`. The smallest permission surface is the safest one.

## Outcome

Token discovery now works on the first attempt for any new Page added to the Business Portfolio. The mystery has been documented and embedded in tooling.

## The lesson, in one line

> When a Meta endpoint returns an empty list against an asset you can see in the UI, you are missing a permission, not configuring it wrong.
