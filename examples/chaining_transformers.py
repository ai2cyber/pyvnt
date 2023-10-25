from typing import List
from uuid import UUID, uuid4

from pyvnt import Entity, descriptor
from pyvnt.transformer import Transformer
from pyvnt.transformers.common import uuid_transformer
from pyvnt.transformers.sequence import list_transformer


def join_list_transformer(separator: str = ";") -> Transformer[List[str], str]:
    def serializer(value: List[str], property_name: str) -> str:
        return separator.join(value)

    def deserializer(value: str, property_name: str) -> List[str]:
        return value.split(separator)

    return Transformer("join_list_transformer", serializer, deserializer)


list_uuid_transformer: Transformer[List[UUID], List[str]] = list_transformer(uuid_transformer())
list_str_transformer: Transformer[List[str], str] = join_list_transformer()
chained_transformer: Transformer[List[UUID], str] = list_uuid_transformer.chain(list_str_transformer)
# Notice the types of each transformer. The static analysis recognizes that the chained transformer is of type
# Transformer[List[UUID], str]. Internally it follows the path:
# List[UUID] -> list_uuid_transformer -> List[str] -> join_list_transformer -> str


class Sample(Entity):
    property_one: List[UUID] = descriptor(transformations=[chained_transformer])


uuids = [uuid4(), uuid4(), uuid4()]
sample = Sample(uuids)
serialized_sample = sample.serialize()

print(serialized_sample)
assert serialized_sample["property_one"] == ";".join(str(uuid) for uuid in uuids)
