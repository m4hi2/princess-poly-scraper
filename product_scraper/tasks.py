from dataclasses import dataclass, field

@dataclass
class Task():
    uuid: str
    link: str
    errors: list = field(default_factory=list)
    failed_times: int = 0