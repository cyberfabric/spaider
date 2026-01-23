# CLISPEC - CLI Command Specification Format

**Version**: 1.0  
**Purpose**: Human and machine-readable format for CLI command documentation

---

## Overview

CLISPEC is a simple, structured text format for documenting CLI commands. It is designed to be:
- **Human-readable**: Easy to write and read in plain text
- **Machine-parseable**: Structured format for tooling and AI agents
- **Expressive**: Captures all essential CLI command information
- **Minimal**: No complex syntax, just clear sections

**Primary audience**: AI agents implementing or using CLI tools

**Use cases**:
- CLI tool documentation
- Command validation
- AI agent command understanding
- Auto-completion generation
- Help text generation

---

## Format Specification

### Basic Structure

```
COMMAND <command-name>
SYNOPSIS: <tool> <command> [options] [arguments]
DESCRIPTION: <brief description>
WORKFLOW: <workflow-reference> (optional)

ARGUMENTS:
  <arg-name>  <type>  [required|optional]  <description>

OPTIONS:
  --long-name, -s  <type>  [default: value]  <description>

EXIT CODES:
  <code>  <description>

EXAMPLE:
  $ <example-usage>

RELATED: (optional)
  - @CLI.other-command
  - @Workflow.workflow-name
---
```

**Separator**: Commands separated by `---` on its own line

---

## Sections

### Required Sections

**COMMAND**: Command name (kebab-case)
```
COMMAND init-feature
```

**SYNOPSIS**: Command usage pattern
```
SYNOPSIS: fdd init-feature <slug> [options]
```

**DESCRIPTION**: Brief description (1-2 sentences)
```
DESCRIPTION: Initialize a new feature with DESIGN.md template
```

**ARGUMENTS**: Positional arguments (one per line)
```
ARGUMENTS:
  slug  <slug>  required  Feature identifier (lowercase-with-dashes)
  name  <string>  optional  Human-readable feature name
```

**OPTIONS**: Named options/flags (one per line)
```
OPTIONS:
  --template, -t  <string>  [default: standard]  Template to use
  --skip-validation  <boolean>  Skip architecture validation
  --verbose, -v  <boolean>  Enable verbose output
```

**EXIT CODES**: Exit codes and their meanings
```
EXIT CODES:
  0  Success
  1  General error
  2  Validation failure
  3  Workflow error
```

**EXAMPLE**: Usage examples (one or more)
```
EXAMPLE:
  $ fdd init-feature user-authentication
  $ fdd init-feature data-export --template minimal
  $ fdd init-feature payment --skip-validation
```

### Optional Sections

**WORKFLOW**: Reference to FDD workflow
```
WORKFLOW: 05-init-feature
```

**RELATED**: Related commands/workflows
```
RELATED:
  - @CLI.validate-feature
  - @CLI.init-features
  - @Workflow.05-init-feature
```

---

## Type System

### Supported Types

- `<string>` - Any text value
- `<number>` - Numeric value (integer or float)
- `<boolean>` - True/false flag
- `<path>` - File system path
- `<slug>` - Kebab-case identifier (lowercase-with-dashes)
- `<url>` - URL/URI
- `<email>` - Email address
- `<json>` - JSON string

### Type Constraints

Types can have constraints in description:
```
ARGUMENTS:
  port  <number>  required  Port number (1-65535)
  count  <number>  optional  Item count (positive integer)
```

---

## Syntax Rules

### Formatting Rules

1. **Command names**: kebab-case (e.g., `init-feature`, `validate-architecture`)
2. **Section headers**: UPPERCASE followed by colon
3. **One item per line**: Arguments and options on separate lines
4. **Indentation**: 2 spaces for items under sections
5. **Separator**: `---` on its own line between commands
6. **Required/optional**: Explicitly mark with keywords
7. **Defaults**: In square brackets `[default: value]`

### Option Format

```
--long-name, -s  <type>  [default: value]  <description>
```

- Long form: `--long-name` (required)
- Short form: `-s` (optional)
- Type: `<type>` (required)
- Default: `[default: value]` (optional)
- Description: text (required)

### Argument Format

```
<arg-name>  <type>  [required|optional]  <description>
```

- Name: lowercase, hyphens allowed
- Type: from supported types
- Required/optional: explicit keyword
- Description: text

---

## Linking Syntax

Reference other commands, workflows, or entities:

### Command References

```
@CLI.command-name              # Reference to another command
@CLI.command-name.--option     # Reference to specific option
@CLI.command-name.<arg-name>   # Reference to specific argument
```

### Workflow References

```
@Workflow.NN-workflow-name     # Reference to FDD workflow
@Workflow.adapter-config       # Reference to workflow file
```

### Feature References

```
@Feature.{slug}                # Reference to feature
@DomainModel.{TypeName}        # Reference to domain type
```

---

## Complete Example

```
COMMAND validate-feature
SYNOPSIS: fdd validate-feature <slug> [options]
DESCRIPTION: Validate feature design completeness and FDD compliance
WORKFLOW: 06-validate-feature

ARGUMENTS:
  slug  <slug>  required  Feature identifier to validate

OPTIONS:
  --strict  <boolean>  Enable strict validation mode
  --fix, -f  <boolean>  Auto-fix common issues
  --output, -o  <path>  [default: stdout]  Output file for report

EXIT CODES:
  0  Feature design valid (score 100/100)
  1  File system error or feature not found
  2  Validation failed (score < 100/100)
  3  Workflow execution error

EXAMPLE:
  $ fdd validate-feature user-authentication
  $ fdd validate-feature data-export --strict
  $ fdd validate-feature payment --output report.txt

RELATED:
  - @CLI.init-feature
  - @CLI.fix-design
  - @Workflow.06-validate-feature
---

COMMAND init-feature
SYNOPSIS: fdd init-feature <slug> [options]
DESCRIPTION: Initialize a new feature with DESIGN.md template
WORKFLOW: 05-init-feature

ARGUMENTS:
  slug  <slug>  required  Feature identifier (lowercase-with-dashes)

OPTIONS:
  --template, -t  <string>  [default: standard]  Template to use (standard|minimal|full)
  --skip-validation  <boolean>  Skip architecture validation check
  --force  <boolean>  Overwrite existing feature directory

EXIT CODES:
  0  Feature initialized successfully
  1  File system error or invalid slug
  2  Architecture validation failed
  3  Feature directory already exists

EXAMPLE:
  $ fdd init-feature user-authentication
  $ fdd init-feature data-export --template minimal
  $ fdd init-feature payment --skip-validation

RELATED:
  - @CLI.validate-feature
  - @CLI.init-features
  - @Workflow.05-init-feature
---
```

---

## Validation Rules

### Required Elements

- ✅ COMMAND section with valid command name
- ✅ SYNOPSIS section with usage pattern
- ✅ DESCRIPTION section (non-empty)
- ✅ ARGUMENTS section (can be empty if no arguments)
- ✅ OPTIONS section (can be empty if no options)
- ✅ EXIT CODES section with at least code 0
- ✅ EXAMPLE section with at least one example

### Content Rules

- ✅ Command names must be kebab-case
- ✅ Types must be from supported types list
- ✅ Exit codes must be numeric (0-255)
- ✅ Examples must start with `$ `
- ✅ Required/optional keywords for arguments
- ✅ Defaults in square brackets format
- ✅ One argument/option per line

### Style Rules

- ✅ Section headers in UPPERCASE
- ✅ 2-space indentation for items
- ✅ Separator `---` between commands
- ✅ No trailing whitespace
- ✅ Consistent spacing

---

## Benefits for AI Agents

### Easy Parsing

Simple structure with clear sections:
```python
def parse_clispec(text):
    commands = text.split('---')
    for cmd_block in commands:
        sections = parse_sections(cmd_block)
        # sections['COMMAND'], sections['ARGUMENTS'], etc.
```

### Clear Semantics

- Explicit required/optional markers
- Type information for validation
- Exit codes for error handling
- Examples for understanding usage

### Workflow Integration

- Direct workflow references
- Command relationships via RELATED
- Integration with FDD methodology

### Tool Generation

From CLISPEC, generate:
- Help text (`--help`)
- Argument parsers
- Validation logic
- Auto-completion
- Documentation

---

## Usage in FDD

### In Adapter Configuration

CLISPEC is a built-in option for CLI API contracts:

```
Q4: API Contract Technology
Options:
  ...
  4. CLISPEC (for CLI tools)
  ...
```

### File Location

Standard location: `architecture/cli-specs/commands.clispec`

### Validation

```bash
# Validate CLISPEC format
fdd validate-cli-specs

# Or custom validator
your-tool validate-clispec architecture/cli-specs/commands.clispec
```

### Linking from DESIGN.md

```markdown
## API Contracts

**Format**: CLISPEC
**Location**: `architecture/cli-specs/commands.clispec`

**Commands**:
- @CLI.init-feature - Initialize feature
- @CLI.validate-feature - Validate feature design
```

---

## Comparison with Alternatives

### vs. OpenAPI

- ✅ Simpler format (text vs. YAML/JSON)
- ✅ CLI-specific (not REST API)
- ✅ Human-readable in plain text
- ❌ Less tooling ecosystem

### vs. man pages

- ✅ Structured format (parseable)
- ✅ Machine-readable
- ✅ Workflow integration
- ❌ Not Unix standard

### vs. Markdown

- ✅ More structured
- ✅ Enforced sections
- ✅ Type system
- ❌ Less flexible

**Best for**: CLI tools in FDD projects where agent-readability is priority

---

## Implementation Notes

### Parser Implementation

Recommended approach:
1. Split by `---` separator
2. Parse each command block
3. Extract sections by header pattern
4. Parse arguments/options line by line
5. Validate structure

### Generator Implementation

From code to CLISPEC:
1. Extract command metadata
2. Format sections
3. Add examples
4. Generate separator

### Editor Support

Syntax highlighting:
- Section headers as keywords
- Types as types
- Commands as functions
- Comments with `#` prefix

---

## Version History

- **v1.0** (2026-01): Initial specification
  - Basic structure
  - Type system
  - Linking syntax
  - Validation rules

---

## References

- **FDD Methodology**: `AGENTS.md`
- **Adapter Guide**: `guides/ADAPTER.md`
- **Example Usage**: See `../fdd-cli-adapter/AGENTS.md` for real-world CLISPEC

---

## License

This specification is part of the FDD (Feature-Driven Development) methodology.
