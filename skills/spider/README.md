# Spider Tool

Unified Spider tool for artifact validation, search, and traceability.

## Commands

| Command | Description |
|---------|-------------|
| `validate` | Validate Spider artifacts against templates |
| `validate-weavers` | Validate weaver configuration and templates |
| `validate-code` | Validate Spider traceability markers in code |
| `list-ids` | List all Spider IDs from artifacts |
| `list-id-kinds` | List ID kinds that exist in artifacts |
| `get-content` | Get content block for a specific Spider ID |
| `where-defined` | Find where an Spider ID is defined |
| `where-used` | Find all references to an Spider ID |
| `adapter-info` | Discover Spider adapter configuration |
| `init` | Initialize Spider config and adapter |
| `agents` | Generate agent-specific workflow proxies and skill outputs |
| `self-check` | Validate examples against templates |

## Usage

```bash
# Validate all registered artifacts
python3 scripts/spider.py validate

# Validate specific artifact
python3 scripts/spider.py validate --artifact architecture/PRD.md

# Validate code traceability
python3 scripts/spider.py validate-code

# List all IDs
python3 scripts/spider.py list-ids

# Find where ID is defined
python3 scripts/spider.py where-defined --id spd-myapp-req-auth

# Initialize project
python3 scripts/spider.py init --yes
```

## Testing

```bash
make test
```

## Documentation

See `SKILL.md` for complete command reference and `spider.clispec` for CLI specification.
