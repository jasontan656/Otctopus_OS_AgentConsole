# Product Iteration Logging

## Purpose

The Git history of this repository should no longer read like a pile of isolated skill patches.

It should progressively become the product iteration log of Octopus OS.

## Commit Semantics

Each commit should ideally answer:

- what new product capability or direction was introduced
- what wrong direction was removed
- what boundary or workflow was tightened
- what known issue was resolved
- which design judgment was formally converged

## Good Commit Shapes

- `product: introduce Octopus OS facade and language surface rules`
- `product: add bilingual wizard flow for local installation`
- `sync: restrict all-scope push to skill roots only`
- `docs: publish English-facing product identity and install model`

## Bad Commit Shapes

- `fix stuff`
- `update files`
- `misc cleanup`

## Value

When other developers inspect the repository history, they should be able to understand how Octopus OS evolved as a product, not just how individual files were patched.
