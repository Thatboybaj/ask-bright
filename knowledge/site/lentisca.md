---
title: Lentisca  Case Study | Bright Ajiboye
url: https://brightajiboye.com/work/lentisca
---

# Lentisca

Concept Rebuild

Personal study

Front-end development

A design and development study. I rebuilt an existing farm-shop concept for jams, honey and preserves from Puglia to practise 3D, physics and scroll motion on the web. The original idea is not mine.

© Lentisca

## About this project

Lentisca is a rebuild, not an original concept. I recreated an existing brand idea as a learning project to push my front-end skills: 3D in the browser, physics, and motion that responds to scroll. The design direction comes from the original; the code is my own.

## What I built

Home with a scroll-driven jar carousel and a rotating “From the grove to the table” seal.

Pantry with 10 product pages generated from typed product data.

Harvest, Experience, About, Contact and Privacy pages.

Mobile layouts for every section.

## Technical approach

Astro, Tailwind CSS v4 and TypeScript. Every page is pre-rendered HTML.

GSAP with ScrollTrigger and SplitText for motion, Lenis for smooth scrolling.

Three.js renders the jar labels in the browser from product data, so no label images are needed.

Matter.js powers the fruit physics. Both libraries load lazily after first paint.

Each page loads only the scripts its sections use.

## What I learned

How to keep a motion-heavy site light: split animation into small modules per section, defer anything 3D until the page is usable, and let data drive the visuals instead of exporting dozens of images.

A static Astro site with a pantry of 10 product pages. Jar labels are drawn in the browser from product data with three.js, fruit physics run on Matter.js, and both load only after the first paint.

Verdant

Website Audit Agent
