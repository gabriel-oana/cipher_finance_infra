from aws_cdk import core


def add_tags(construct, tags: dict) -> None:
    for tag in tags:
        core.Tags.of(construct).add(tag['key'], tag['value'])