---
title: ProspectPilot  Case Study | Bright Ajiboye
url: https://brightajiboye.com/work/prospectpilot
---

# ProspectPilot

AI Prospecting Agent

Personal product

AI engineering & design

An agent that finds companies worth contacting, builds a cited research dossier on each one, scores the fit, and drafts a grounded first email. Every send passes deterministic policy gates, and anything uncertain goes to a human first.

© ProspectPilot

Full case study

## Overview

ProspectPilot follows one rule: research first, evidence second, outreach last. It discovers companies from permitted sources, maps a decision-maker, and drafts an email that refers only to things it actually observed.

## The pipeline

Discover: companies from permitted sources or a CSV, with a source guard that blocks restricted platforms.

Research: a robots-aware crawler builds a dossier. Every observation is labelled as observed or inferred and cites its evidence.

Score: hard gates first, then a weighted 0 to 100 score across ICP fit, problem evidence, service fit, timing and access. A high score never overrides a failed gate.

Write: the model proposes an angle and a draft as validated JSON. The footer and opt-out are added in code.

Send: gates run again inside a locked transaction at send time. Anything unknown goes to the review queue.

## Design decisions

Deterministic policy, probabilistic agents. Models only propose, and the policy package decides.

Postgres is both the system of record and the job queue, with idempotency keys, leases and retries.

Row-level security is the tenant boundary.

Autonomy in three stages: discovery only, then review mode, then autonomous once review quality holds.

A full mock mode (embedded Postgres, mock LLM, sandbox mailbox) so the whole system runs with no keys.

## Evaluation

108 tests cover cross-tenant attacks, the exactly-once send path, every gate failing closed, unsubscribe and bounce handling, and prompt-injection cases. An LLM benchmark gates autonomous sending.

## Stack

TypeScript, Next.js, Postgres on Supabase, DeepSeek with Anthropic and OpenAI adapters, Gmail OAuth, Vercel and a containerised worker.

Outcome

A TypeScript monorepo with a Next.js dashboard and a background worker. It researches, scores, writes and sends in controlled sequences. I use it for my own prospecting in architecture and real estate.

LeadPilot
