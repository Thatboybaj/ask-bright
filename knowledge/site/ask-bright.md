---
title: Ask Bright  Case Study | Bright Ajiboye
url: https://brightajiboye.com/work/ask-bright
---

# Ask Bright

AI Portfolio Assistant

Year

'26

Client

Personal project

Role

AI engineering & design

An AI assistant that answers questions about my work, grounded only in my own case studies. Built with Google ADK, Gemini and retrieval-augmented generation, deployed on Vercel.

Try it live

© Ask Bright

Full case study

## Overview

Ask Bright lets visitors ask questions about my projects, skills and services. Every answer is drawn from my real project write-ups, with links to the sources it used.

## How it works

Indexing: each case study is split into section-sized chunks and embedded with Gemini embeddings, then saved to a JSON index.

Retrieval: the question is embedded and compared against every chunk with cosine similarity. Weak matches are dropped.

Generation: an ADK agent with one tool, search_portfolio, retrieves passages and Gemini writes the answer from them, citing its sources.

## Design decisions

A JSON file instead of a vector database. Under 50 chunks, brute-force search is fast and removes a dependency.

Chunks split by section, with the project title attached, so retrieval knows which project a detail belongs to.

A relevance threshold, so the agent refuses out-of-scope questions instead of guessing.

Retrieval exposed as a tool, so the model can search more than once for multi-part questions.

## Evaluation

An eval script runs 15 test questions and checks whether retrieval returns the right case study, including two questions that should return nothing.

## Stack

Python, Google ADK, Gemini, FastAPI and Vercel, with a Framer code component for the embedded chat.

Outcome

A RAG agent that answers from my case studies, links the sources it used, and says so when the answer isn’t in my work. It runs as a FastAPI app on Vercel and can be embedded in Framer.

Read full casestudy

Previous project

Website Audit Agent

Next project

Sable Records
