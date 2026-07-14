"""Core schema definitions for early tool contracts."""

from pydantic import BaseModel, Field


class ToolDescriptor(BaseModel):
    """Basic metadata describing an MCP tool."""

    name: str
    title: str
    description: str


class ResourceDescriptor(BaseModel):
    """Basic metadata describing an MCP resource."""

    uri: str
    name: str
    kind: str = Field(description="Broad classification for the resource payload.")


class PromptDescriptor(BaseModel):
    """Basic metadata describing an MCP prompt."""

    name: str
    description: str
