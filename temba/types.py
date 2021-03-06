from __future__ import unicode_literals

from .base import TembaObject, SimpleField, IntegerField, DatetimeField, ObjectListField


class Broadcast(TembaObject):
    id = IntegerField()
    urns = SimpleField()
    contacts = SimpleField()
    groups = SimpleField()
    text = SimpleField()
    status = SimpleField()
    created_on = DatetimeField()


class Contact(TembaObject):
    uuid = SimpleField()
    name = SimpleField()
    urns = SimpleField()
    groups = SimpleField(src='group_uuids')
    fields = SimpleField()
    language = SimpleField()
    modified_on = DatetimeField()


class Group(TembaObject):
    uuid = SimpleField()
    name = SimpleField()
    size = IntegerField()


class Field(TembaObject):
    key = SimpleField()
    label = SimpleField()
    value_type = SimpleField()


class FlowRuleSet(TembaObject):
    uuid = SimpleField(src='node')
    label = SimpleField()


class Flow(TembaObject):
    uuid = SimpleField()
    name = SimpleField()
    archived = SimpleField()
    labels = SimpleField()
    participants = IntegerField()
    runs = IntegerField()
    completed_runs = IntegerField()
    rulesets = ObjectListField(item_class=FlowRuleSet)
    created_on = DatetimeField()


class Message(TembaObject):
    contact = SimpleField()
    urn = SimpleField()
    status = SimpleField()
    type = SimpleField()
    labels = SimpleField()
    direction = SimpleField()
    text = SimpleField()
    created_on = DatetimeField()
    delivered_on = DatetimeField()
    sent_on = DatetimeField()


class RunValueSet(TembaObject):
    node = SimpleField()
    category = SimpleField()
    text = SimpleField()
    rule_value = SimpleField()
    value = SimpleField()
    label = SimpleField()
    time = DatetimeField()


class RunStep(TembaObject):
    node = SimpleField()
    text = SimpleField()
    value = SimpleField()
    type = SimpleField()
    arrived_on = DatetimeField()
    left_on = DatetimeField()


class Run(TembaObject):
    id = IntegerField(src='run')
    flow = SimpleField(src='flow_uuid')
    contact = SimpleField()
    steps = ObjectListField(item_class=RunStep)
    values = ObjectListField(item_class=RunValueSet)
    created_on = DatetimeField()

    @classmethod
    def deserialize(cls, item):
        run = super(Run, cls).deserialize(item)

        # Temba API should only be returning values for the last visit to each step but returns all instead
        last_only = []
        nodes_seen = set()
        for valueset in reversed(run.values):
            if valueset.node not in nodes_seen:
                last_only.append(valueset)
                nodes_seen.add(valueset.node)
        last_only.reverse()
        run.values = last_only

        return run
