"""Github setting 'Protect this branch' was disabled for a repo."""
from stream_alert.rule_processor.rules_engine import StreamRules

rule = StreamRules.rule


@rule(logs=['ghe:general'], outputs=['aws-firehose:alerts'])
def github_disable_protect_this_branch(rec):
    """
    author:       @mimeframe
    description:  Github setting 'Protect this branch' was disabled for a repo.
                  When unchecking this top-level option, it also disables
                  'Require pull request reviews before merging',
                  'Require review from Code Owners', and all other branch protections
                  like status checks.
    repro_steps:  (a) Visit /<org>/<repo>/settings/branches/<branch>
                  (b) Uncheck 'Protect this branch'
                  (c) Click 'Save Changes'
    reference:    https://help.github.com/articles/configuring-protected-branches/
    """
    return rec['action'] == 'protected_branch.destroy'
