# (just)[https://just.systems/]
# (just github)[https://github.com/casey/just]
# (just manual)[https://just.systems/man/en/]
# 

alias r := run

# Set the working directory for all recipes in this justfile
# set working-directory := "patterns/workflows/Gemini-api-integration"

# Automatically load the .env file found in the working directory
set dotenv-load
set dotenv-filename := ".env"

set dotenv-required

set shell := ["/home/mwoodpatrick/.nix-profile/bin/bash", "-cu"]

# --- Recipes ---

[working-directory: 'patterns/workflows/Gemini-api-integration']
foo:
  echo "hello $PWD"
  ls **/*.txt

[working-directory: 'patterns/workflows/Gemini-api-integration']
hello:
  echo "hello world"

# Usage: just run "your command here"
# Example: just run simple.py, just run list_models.py
[working-directory: 'patterns/workflows/Gemini-api-integration']
run command:
    ./{{command}}
