"""Core schema definitions for early tool contracts."""

from pydantic import BaseModel, Field


class ToolDescriptor(BaseModel):
    """Basic metadata describing an MCP tool."""

    name: str
    title: str
    description: str
    input_schema: dict[str, object] = Field(
        default_factory=dict,
        description="JSON Schema describing tool arguments.",
    )
    category: str = Field(default="core", description="Rough grouping (core, lens, chaos, spec).")
    prerequisites: list[str] = Field(
        default_factory=list,
        description="Adapter names that must be available for the tool to succeed.",
    )
    expected_duration: str = Field(
        default="fast", description="Rough duration hint: instant, fast, or slow."
    )
    mutates_session: bool = Field(
        default=False, description="Whether the call writes to the in-memory session store."
    )


class ResourceDescriptor(BaseModel):
    """Basic metadata describing an MCP resource."""

    uri: str
    name: str
    kind: str = Field(description="Broad classification for the resource payload.")


class PromptDescriptor(BaseModel):
    """Basic metadata describing an MCP prompt."""

    name: str
    description: str
    arguments: list[dict[str, object]] = Field(
        default_factory=list,
        description="MCP PromptArgument-shaped entries (name, description, required).",
    )
