from enum import Enum
from turtle import st
from typing import Literal, Optional

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field, ValidationError

from .prompt import FINALIZE_RESPONSE_FORMATTER_AGENT


class FormField(BaseModel):
    id: str = Field(description="The id of the form field.")
    label: str = Field(description="The label of the form field.")
    placeholder: str = Field(description="The placeholder of the form field.")
    field_type: Literal[
        "text",
        "number",
        "date",
        "boolean",
        "slider",
        "calendar",
        "dropdown",
        "multi_select",
        "file_upload",
        "rating",
        "range",
        "color_picker",
        "email",
    ]
    required: bool = Field(description="Whether the form field is required.")
    options: list[str] = Field(
        default_factory=list, description="The options of the form field."
    )
    min_value: Optional[int] = Field(
        default=None, description="The minimum value of the form field."
    )
    max_value: Optional[int] = Field(
        default=None, description="The maximum value of the form field."
    )
    step: Optional[int] = Field(default=None, description="The step of the form field.")
    default_value: Optional[str] = Field(
        default=None, description="The default value of the form field."
    )
    is_disabled: Optional[bool] = Field(
        default=None, description="Whether the form field is disabled."
    )
    is_readonly: Optional[bool] = Field(
        default=None, description="Whether the form field is readonly."
    )


class DynamicFormData(BaseModel):
    form_name: str = Field(description="The name of the form.")
    form_description: str = Field(description="The description of the form.")
    form_fields: list[FormField] = Field(description="The fields of the form.")


def dynamic_form_tool(form: DynamicFormData):
    """
    Use this tool to create a dynamic form for the user to fill in.
    """
    try:
        DynamicFormData.model_validate(form, strict=False)
        return {
            "success": True,
            "message": "Form created successfully.",
            "form": form,
        }
    except ValidationError as e:
        return {
            "success": False,
            "error": str(e) + "Please try again with the correct format.",
        }


class ChartTool(BaseModel):
    chart_type: str
    chart_data: dict
    chart_description: str


def chart_tool(chart: ChartTool):
    """
    Use this tool to create a chart for the user to view.
    """
    return chart


class TableTool(BaseModel):
    table_headers: list[str]
    table_data: dict
    table_description: str


def table_tool(table: TableTool):
    """
    Use this tool to create a table for the user to view.
    """
    return table


agent = LlmAgent(
    model="gemini-2.5-flash",
    name="finalise_response_agent",
    description="You are a helpful assistant that helps the user to get a formatted response from the other agents.",
    instruction=FINALIZE_RESPONSE_FORMATTER_AGENT,
    tools=[dynamic_form_tool, chart_tool, table_tool],
)
