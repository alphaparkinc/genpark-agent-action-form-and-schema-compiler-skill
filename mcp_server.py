"""MCP server for Agent Action Form & Schema Compiler."""
import sys
import json
from client import ActionFormCompiler


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "compile_tool_schema_to_form",
                    "description": "Compiles an agent MCP tool definition into a structured human-in-the-loop interactive form schema",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "tool_schema": {
                                "type": "object",
                                "description": "MCP tool definition with name, description, and inputSchema",
                            }
                        },
                        "required": ["tool_schema"],
                    },
                },
                {
                    "name": "validate_action_form_submission",
                    "description": "Validates human-submitted form values against compiled schema constraints",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "form_metadata": {"type": "object"},
                            "submission_data": {"type": "object"},
                        },
                        "required": ["form_metadata", "submission_data"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "compile_tool_schema_to_form":
            res = ActionFormCompiler.compile_schema_to_form(args.get("tool_schema", {}))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "validate_action_form_submission":
            res = ActionFormCompiler.validate_form_submission(
                args.get("form_metadata", {}),
                args.get("submission_data", {}),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
