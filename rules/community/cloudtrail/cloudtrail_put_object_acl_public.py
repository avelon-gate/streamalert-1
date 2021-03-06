"""Identifies new S3 object ACLs that grant access to the public."""
from helpers.base import data_has_value_from_substring_list, in_set
from stream_alert.rule_processor.rules_engine import StreamRules

rule = StreamRules.rule


@rule(
    logs=['cloudwatch:events'],
    outputs=['aws-firehose:alerts'],
    req_subkeys={
        'detail': ['requestParameters']
    })
def cloudtrail_put_object_acl_public(rec):
    """
    author:         @mimeframe
    description:    Identifies a change to an S3 object ACL that grants access
                    to AllUsers (anyone on the internet) or AuthenticatedUsers
                    (any user with an AWS account).
    reference:      http://amzn.to/2yfRxzp
    playbook:       (a) Verify if the object should be publicly accessible
                    (b) If not, modify the object ACL
    """
    public_acls = {
        'http://acs.amazonaws.com/groups/global/AuthenticatedUsers',
        'http://acs.amazonaws.com/groups/global/AllUsers'
    }

    # s3 buckets that are expected to have public objects
    public_buckets = {'example-bucket-to-ignore'}

    request_params = rec['detail']['requestParameters']
    return (
        rec['detail']['eventName'] == 'PutObjectAcl' and
        # note: substring is used because it can exist as:
        # "http://acs.amazonaws.com/groups/global/AllUsers" or
        # "uri=http://acs.amazonaws.com/groups/global/AllUsers"
        data_has_value_from_substring_list(request_params, public_acls)
        and not in_set(request_params.get('bucketName'), public_buckets))
