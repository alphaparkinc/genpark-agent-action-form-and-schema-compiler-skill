"""Example usage for Agent Action Form & Schema Compiler."""
from client import ActionFormCompiler

if __name__ == "__main__":
    mcp_tool = {
        "name": "refund_order",
        "description": "Issues customer credit card refund.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Order reference code"},
                "amount": {"type": "number", "minimum": 1.0, "maximum": 500.0},
                "reason": {"type": "string", "enum": ["defective", "delayed", "customer_request"]},
            },
            "required": ["order_id", "amount"],
        },
    }

    form = ActionFormCompiler.compile_schema_to_form(mcp_tool)
    print("Form Generated:", form["title"])
    for f in form["fields"]:
        print(f"  Field: {f['field_name']} -> Component: {f['ui_component']} (Required: {f['required']})")

    # Validation check
    val_res = ActionFormCompiler.validate_form_submission(form, {"order_id": "ord_99", "amount": 600.0})
    print("\nValidation Result:", val_res["valid"], "Errors:", val_res["errors"])
