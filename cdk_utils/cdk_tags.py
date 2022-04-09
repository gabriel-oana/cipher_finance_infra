import aws_cdk as cdk


def add_tags(construct, tags: dict) -> None:
    for tag in tags:
        cdk.Tags.of(construct).add(tag['key'], tag['value'])