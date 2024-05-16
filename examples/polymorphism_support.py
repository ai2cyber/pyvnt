from typing import List
from uuid import UUID, uuid4

from pyvnt import Entity, descriptor
from pyvnt.transformers.common import uuid_transformer
from pyvnt.transformers.sequence import list_transformer


class Sample(Entity):
    property_one: List[UUID] = descriptor(transformations=[list_transformer(uuid_transformer())])


class InheritedSample(Sample):
    property_two: int = descriptor()


uuids = [uuid4(), uuid4(), uuid4()]
sample = Sample(uuids)
inherited_sample = InheritedSample(sample.property_one, 10)
serialized_inherited_sample = inherited_sample.serialize()

assert inherited_sample == Sample.deserialize(serialized_inherited_sample)
# Notice that you called the deserialize method from the Sample class and yet it returned an Inherited sample instance.
