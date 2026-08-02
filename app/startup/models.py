from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Literal

ComponentState = Literal["pending", "starting", "ready", "degraded", "failed", "stopped"]

@dataclass(frozen=True)
class Problem:
    code: str
    message: str
    component: str
    fatal: bool = False
    detail: str | None = None

@dataclass
class ComponentStatus:
    name: str
    required: bool
    state: ComponentState = "pending"
    detail: str | None = None
    pid: int | None = None
    url: str | None = None

@dataclass
class StartupSnapshot:
    schema: str = "ApplicationStartupSupervisor.v1"
    overall_status: str = "starting"
    components: dict[str, ComponentStatus] = field(default_factory=dict)
    problems: list[Problem] = field(default_factory=list)
    launcher_instance_id: str | None = None
    def to_dict(self) -> dict:
        return asdict(self)
