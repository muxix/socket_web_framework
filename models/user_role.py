import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()
    admin = auto()


class JSONEncoderExtend(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def json_decode_extend(d):
    if JSONEncoderExtend.prefix in d:
        name = d[JSONEncoderExtend.prefix]
        return UserRole[name]
    else:
        return d
