# SkillPack Studio

A tiny CLI that turns a folder of prompts, scripts, examples, and docs into a polished AI assistant skill pack.

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
skillpack init my-skill
skillpack validate my-skill
skillpack preview my-skill --port 8000
skillpack export my-skill
```

## What it does

- Scaffolds a minimal cross-assistant skill pack
- Validates metadata and required docs
- Serves a local web preview
- Exports simple installer files

## Development

```bash
python -m pip install -e '.[dev]'
pytest
```
