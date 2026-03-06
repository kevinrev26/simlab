from pydantic import BaseModel, UUID4, HttpUrl, Field, field_validator
from typing import Optional, List, Literal

class Parameters(BaseModel):
    entrypoint_args: Optional[List[str]] = None
    env_vars: Optional[dict[str, str]] = None

class Runtime(BaseModel):
    runs_per_container: int
    image_name: str
    image_tag: str
    parameters: Optional[Parameters] = None

class Resources(BaseModel):
    cpu_limit: int = Field(default=1, gt=0, description="The number of cpu limit field should be greater than zero")
    memory_limit: int #Validate somehow power of 2 number
    max_containers: int = Field(gt=0, description="The number of max containers field should be greater than zero")
    max_duration_seconds: int = Field(gt=0, description="The number of max duration seconds field should be greater than zero")

    @field_validator('memory_limit')
    @classmethod
    def validate_memory_limit(cls, value):
        if value <= 0 or (value & (value - 1)) != 0:
            raise ValueError("Memory limit should be power of 2.")
        return value

class Behavior(BaseModel):
    seed: Optional[int] = None
    timeout_seconds: int = 30
    max_attempts: int = Field(gt=0, description="Max attemtps should be greater than zero.")

class Storage(BaseModel):
    volume_name: str
    output_path: str

class Observability(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    metrics_enabled: bool = False
    webhook_url: Optional[HttpUrl] = None

class SimulationModel(BaseModel):
    schema_version: str = "v1"
    uuid: UUID4
    name: str
    label: Optional[str] = None
    priority: int =  Field(default=5, ge=1, le=15)
    status: Literal['QUEUED', 'IN PROCESS', 'DONE']
    runtime: Runtime
    resources: Resources
    behavior: Behavior
    storage: Storage
    observability: Observability

class SimulationResponse(BaseModel):
    uuid: UUID4
    schema_version: str
    name: str
    label: Optional[str]
    priority: int
    status: str

    model_config = {"from_attributes": True}
