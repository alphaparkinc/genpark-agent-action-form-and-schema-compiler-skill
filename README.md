# genpark-agent-action-form-and-schema-compiler-skill

Agent tool-to-UI schema compiler, human-in-the-loop action form generator, and parameter validation enforcer.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Autonomous Tool-to-UI Form Synthesis**: Automatically maps JSON Schema tool definitions into typed UI form components (TextInput, NumberInput, SelectDropdown, TagList).
- **Human-in-the-Loop Safeguards**: Generates clean review-and-authorize modal definitions for high-consequence agent actions.
- **Client-Side Form Validation**: Validates submitted inputs against numeric boundaries, required keys, and enum options before triggering backend execution.

## Architecture

```
[Agent Tool JSON Schema (MCP)]
                │
                ▼
┌──────────────────────────────────────────────┐
│           ActionFormCompiler                 │
│  - JSON Schema Property Mapper               │
│  - Form Component Layout Synthesizer         │
│  - Validation Rule Enforcer (Min/Max/Enum)   │
└──────────────────────────────────────────────┘
                │
                ▼
[Interactive Human Review Form + Validated Payload]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `compile_tool_schema_to_form`: Compiles an agent MCP tool definition into a structured human-in-the-loop interactive form schema.
- `validate_action_form_submission`: Validates human-submitted form values against compiled schema constraints.

## Quickstart (Python API)

```python
from client import ActionFormCompiler

tool = {"name": "pay", "inputSchema": {"properties": {"amt": {"type": "number", "minimum": 1}}}}
form = ActionFormCompiler.compile_schema_to_form(tool)
print("Form title:", form["title"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
