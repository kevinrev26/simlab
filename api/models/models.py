from sqlalchemy import (
    Column, String, Integer, Boolean, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

class SimulationParameter(Base):
    __tablename__ = "simulation_parameters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("simulations.uuid"), nullable=False)
    entrypoint_args = Column(ARRAY(String), nullable=True)

    runtime = relationship("SimulationRuntime", back_populates="parameters")


class SimulationEnvVar(Base):
    __tablename__ = "simulation_env_vars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parameter_id = Column(Integer, ForeignKey("simulation_parameters.id"), nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)


class SimulationRuntime(Base):
    __tablename__ = "simulation_runtimes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("simulations.uuid"), nullable=False)
    runs_per_container = Column(Integer, nullable=False)
    image_name = Column(String, nullable=False)
    image_tag = Column(String, nullable=False)
    parameter_id = Column(Integer, ForeignKey("simulation_parameters.id"), nullable=True)

    simulation = relationship("Simulation", back_populates="runtime")
    parameters = relationship("SimulationParameter", back_populates="runtime")


class SimulationResources(Base):
    __tablename__ = "simulation_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("simulations.uuid"), nullable=False)
    cpu_limit = Column(Integer, nullable=False, default=1)
    memory_limit = Column(Integer, nullable=False)
    max_containers = Column(Integer, nullable=False)
    max_duration_seconds = Column(Integer, nullable=False)

    simulation = relationship("Simulation", back_populates="resources")


class SimulationBehavior(Base):
    __tablename__ = "simulation_behaviors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("simulations.uuid"), nullable=False)
    seed = Column(Integer, nullable=True)
    timeout_seconds = Column(Integer, nullable=False, default=30)
    max_attempts = Column(Integer, nullable=False)

    simulation = relationship("Simulation", back_populates="behavior")


class SimulationStorage(Base):
    __tablename__ = "simulation_storages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("simulations.uuid"), nullable=False)
    volume_name = Column(String, nullable=False)
    output_path = Column(String, nullable=False)

    simulation = relationship("Simulation", back_populates="storage")


class SimulationObservability(Base):
    __tablename__ = "simulation_observabilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("simulations.uuid"), nullable=False)
    log_level = Column(String, nullable=False, default="INFO")
    metrics_enabled = Column(Boolean, nullable=False, default=False)
    webhook_url = Column(String, nullable=True)

    simulation = relationship("Simulation", back_populates="observability")


class Simulation(Base):
    __tablename__ = "simulations"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schema_version = Column(String, nullable=False, default="v1")
    name = Column(String, nullable=False)
    label = Column(Text, nullable=True)
    priority = Column(Integer, nullable=False, default=5)
    status = Column(String, nullable=False, default="QUEUED")

    runtime = relationship("SimulationRuntime", back_populates="simulation", uselist=False, cascade="all, delete-orphan")
    resources = relationship("SimulationResources", back_populates="simulation", uselist=False, cascade="all, delete-orphan")
    behavior = relationship("SimulationBehavior", back_populates="simulation", uselist=False, cascade="all, delete-orphan")
    storage = relationship("SimulationStorage", back_populates="simulation", uselist=False, cascade="all, delete-orphan")
    observability = relationship("SimulationObservability", back_populates="simulation", uselist=False, cascade="all, delete-orphan")
