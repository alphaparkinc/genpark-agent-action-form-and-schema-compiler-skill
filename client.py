"""Agent Action Form and Schema Compiler Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import json


class ActionFormCompiler:
    """Compiles autonomous agent JSON schemas and MCP tool specifications into structured,
    human-in-the-loop interactive form field definitions with client-side validation rules."""

    TYPE_TO_FIELD_MAP = {
        "string": "TextInput",
        "integer": "NumberInput",
        "number": "NumberInput",
        "boolean": "Checkbox",
        "array": "TagList",
        "object": "KeyValueEditor",
    }

    @classmethod
    def compile_schema_to_form(cls, tool_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Translates a JSON Schema tool definition into UI form layout metadata."""
        tool_name = tool_schema.get("name", "agent_action")
        description = tool_schema.get("description", "")
        input_schema = tool_schema.get("inputSchema", {})
        properties = input_schema.get("properties", {})
        required_fields = set(input_schema.get("required", []))

        form_fields = []
        for prop_name, prop_spec in properties.items():
            field_type = prop_spec.get("type", "string")
            ui_component = cls.TYPE_TO_FIELD_MAP.get(field_type, "TextInput")

            field_def = {
                "field_name": prop_name,
                "label": prop_name.replace("_", " ").title(),
                "ui_component": ui_component,
                "description": prop_spec.get("description", ""),
                "required": prop_name in required_fields,
                "default_value": prop_spec.get("default", None),
                "validation": {
                    "data_type": field_type,
                    "required": prop_name in required_fields,
                },
            }

            if "enum" in prop_spec:
                field_def["ui_component"] = "SelectDropdown"
                field_def["options"] = prop_spec["enum"]

            if "minimum" in prop_spec:
                field_def["validation"]["min"] = prop_spec["minimum"]
            if "maximum" in prop_spec:
                field_def["validation"]["max"] = prop_spec["maximum"]

            form_fields.append(field_def)

        return {
            "form_id": f"form_{tool_name}",
            "title": f"Review & Authorize: {tool_name.replace('_', ' ').title()}",
            "description": description,
            "fields_count": len(form_fields),
            "fields": form_fields,
            "submit_action": {"type": "EXECUTE_TOOL", "target_tool": tool_name},
        }

    @classmethod
    def validate_form_submission(cls, form_metadata: Dict[str, Any], submission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validates human-submitted form values against the compiled schema constraints."""
        errors = []
        for field in form_metadata.get("fields", []):
            fname = field["field_name"]
            is_required = field["required"]
            val = submission_data.get(fname)

            if is_required and (val is None or val == ""):
                errors.append(f"Field '{fname}' is required.")
                continue

            v_rules = field["validation"]
            dtype = v_rules.get("data_type")
            if val is not None and dtype in ["integer", "number"]:
                try:
                    num_val = float(val)
                    if "min" in v_rules and num_val < v_rules["min"]:
                        errors.append(f"Field '{fname}' must be >= {v_rules['min']}.")
                    if "max" in v_rules and num_val > v_rules["max"]:
                        errors.append(f"Field '{fname}' must be <= {v_rules['max']}.")
                except (ValueError, TypeError):
                    errors.append(f"Field '{fname}' must be a valid number.")

        is_valid = len(errors) == 0
        return {
            "valid": is_valid,
            "errors": errors,
            "sanitized_payload": submission_data if is_valid else None,
        }
