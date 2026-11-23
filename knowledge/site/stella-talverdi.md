---
title: Stella Talverdi
url: https://brightajiboye.com/work/stella-talverdi
---

# Stella Talverdi

Writer Platform

Web design & dev

A permanent digital archive for a writer and systems thinker, housing 75 essays behind a custom email gate.

Live website

© Stella Talverdi

## Overview

Stella Talverdi is a chemical engineer, attorney, and writer with twelve years inside energy infrastructure. She needed a permanent digital home for 74 published essays spanning systems theory, power, desire, grief, law, and cognition. Not a portfolio. Not a blog. A serious intellectual archive built to last.

The brief was unusually precise. Stella knew exactly what the site was, what it wasn't, and what quality of thinking it needed to reflect. That clarity shaped every decision from the first conversation.

## The Challenge

The project had three distinct layers of complexity.

The first was design. The aesthetic brief was specific and uncompromising — warm charcoal background, aged parchment tones, oxblood accent, typography as the primary design tool. The site needed to feel inhabited, not decorated. That kind of restraint is harder to execute than visual complexity.

The second was content scale. 74 essays across four categories, each requiring its own CMS page. One template had to serve all of them while preserving typographic quality. Category navigation needed to filter content dynamically from the top navigation links, not just from the sidebar.

The third was technical specificity. The brief called for features that don't exist natively in Framer: an email verification gate with 30-day session memory, bypass URLs for targeted sharing with employers and press, content protection across all essay pages, AI crawler blocking while preserving search engine indexing, and automatic Google Sheets logging of every submission.

## What Was Built

6 main pages — Homepage, Essays, About, Work, Thinking in Progress, and Contact. The homepage is a full-screen static image with zero scroll. Four-corner navigation carries the name, tagline, four essay category links, utility links, and a single footer line. Nothing else.

75 essay pages — 74 essays across four categories plus a standalone Rules of Engagement piece, all built on a single CMS template. A toggle in the CMS lets Stella mark any essay as free or gated directly from her dashboard with no developer involvement.

Email gate system — Visitors who click a locked essay see an overlay with a simple email form. On submission, a 30-day cookie is set and the visitor is redirected directly to the essay they came from. Returning visitors with a valid cookie see all essays unlocked immediately with no prompt.

Bypass URL system — Owner-controlled access codes embedded in URLs allow Stella to share specific essays with employers, press, and collaborators without requiring gate completion. Bypass visitors land directly on the essay with a 30-day cookie set silently.

Content protection — Right-click disabled, text selection disabled, and copy keyboard shortcuts blocked across all essay pages and Rules of Engagement.

Google reCAPTCHA v3 — Invisible bot verification on the essay gate form. Runs silently in the background. Real visitors are never interrupted or asked to complete a challenge.

Google Sheets integration — Every email submitted through the gate logs automatically to a spreadsheet in Stella's Google account with a timestamp. No third-party tools, no maintenance required.

robots.txt — 14 known AI training crawlers blocked including GPTBot, CCBot, Anthropic, Perplexity, and Cohere. Google and Bing indexing fully preserved.

Domain connection — stellatalverdi.com transferred from Wix to Framer via DNS update.

## Key Decisions

Replaced Framer Auth with a custom gate. Framer Auth's default flow requires full account creation — first name, email, password. That didn't match the brief. It was replaced with a native Framer form plus custom code overrides, giving exact control over the gate experience and eliminating an ongoing monthly fee.

One template for 74 essays. A single CMS template kept the build lean and maintenance simple. The CMS toggle for gating individual essays means Stella can change any essay's access status without developer involvement.

Cookie timing solved a blank page issue. Setting the cookie on mousedown rather than on click or form submit ensures the cookie is written before Framer's redirect fires — preventing the detail page from loading blank.

Preserve URL Parameters was off by default. Framer's native setting to preserve URL parameters across navigation is disabled by default. Enabling it was critical to making the category filter and redirect system work correctly.

## Outcome

Full scope delivered within the agreed budget and two-week timeline. Six pages, 75 essay pages, email gate, bypass URLs, content protection, reCAPTCHA, Google Sheets integration, robots.txt, and domain connection — all in.

The site feels exactly as the brief described. Warm, serious, unhurried. The gate protects the work without creating friction for returning readers. The bypass system gives Stella precise control over targeted sharing. Content decisions require no developer involvement.

Where a tool couldn't deliver what was specified, it was replaced with one that could — and the client was told why.

75 essay pages. 14 AI crawlers blocked. One system that works exactly as specified.

Full scope delivered on budget in two weeks: 75 essay pages, a custom email gate, bypass URLs and 14 AI crawlers blocked, all manageable without a developer.

C.Black

Tenuta Palmeri
