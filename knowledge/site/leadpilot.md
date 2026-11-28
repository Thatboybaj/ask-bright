---
title: LeadPilot  Case Study | Bright Ajiboye
url: https://brightajiboye.com/work/leadpilot
---

# LeadPilot

AI Sales Assistant

Personal product

AI engineering & design

An embeddable AI assistant that answers visitor questions only from a company’s published content, qualifies them one question at a time, and captures contact details only after explicit consent. It comes with an operator dashboard for leads, conversations and knowledge.

© LeadPilot

Full case study

## Overview

LeadPilot sits on a company’s website as a small chat widget. Visitors ask about pricing, features or security, and it answers from approved pages, cites the source, then moves into a short qualification flow. Every lead, transcript and score lands in the dashboard.

## How it works

Knowledge: pages are ingested from a URL, pasted text or a PDF, reviewed, then published. A crawler respects robots.txt and sitemaps.

Retrieval: hybrid search (BM25 plus vectors, fused with RRF). When the evidence is weak, the assistant says so instead of guessing.

Validation: every reply is checked for its schema, citations, numbers and forbidden claims before the visitor sees it.

Qualification: one question at a time, configurable per workspace, and it copes with questions asked mid-flow.

Consent: contact details stay masked in the transcript until the visitor agrees, and the exact consent text is stored with the lead.

## Design decisions

The model writes language, not decisions. Consent, lead creation, scoring and notifications all live in application code.

Deterministic scoring with a visible breakdown, capped at 100, that never penalises missing data.

An offline extractive engine, so the whole product runs with no API keys and cannot invent a price.

Tenant isolation in every query, plus Postgres row-level security in production.

## Dashboard

Overview with grounded-answer rate and unanswered questions, a lead inbox with score breakdowns, full transcripts with human takeover, and a knowledge section to fix the gaps visitors reveal.

## Evaluation

45 automated tests, a 25-case regression set and an 18-case held-out set. The held-out score is reported honestly, and the offline engine produced zero fabricated facts.

## Stack

Python, FastAPI, SQLAlchemy, Postgres with pgvector, React and Vite, Stripe for billing, and a Shadow DOM widget. Deployed on Vercel.

Outcome

A FastAPI backend, a drop-in widget that works on any site and a React dashboard. Answers are grounded and cited, leads are scored by a rules engine you can read, and a person can take over any conversation.

ProspectPilot

Sandline Films
