# Blockchain Quant Lane

This lane handles Solidity smart contracts, token/transaction tracing, and chain analytics.

## Scope
- Smart-contract research and prototyping (Hardhat)
- ERC-20 / DEX flow tracing
- Wallet clustering heuristics
- Event-driven alpha/risk signals from on-chain data

## Structure
- `hardhat/` — Solidity dev environment
- `contracts/` — audited or research contract sources
- `scripts/` — deployment/testing scripts
- `analysis/` — token flow + transaction notebooks/scripts

## Suggested free/open-source tooling
- Hardhat + ethers.js
- Foundry (optional)
- The Graph (self-hosted where applicable)
- Open-source chain indexers / public RPC providers (free tier)

## Immediate next steps
1. Initialize Hardhat project in `hardhat/`.
2. Add contract template + local test.
3. Add first chain-tracing script (ERC20 transfer graph extraction).
