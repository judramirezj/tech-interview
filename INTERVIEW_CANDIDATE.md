# Pair Programming Interview Simulation

**Time:** 20–40 minutes  
**File to work on:** `bad_code.py`

---

## Scenario

You've just joined a team. A colleague wrote a script to fetch weather data for a list of cities and save a summary report. It works, but it's slow and fragile. Your job is to review and improve it.

Set a timer and work through each round in order. Try to write actual code, not just describe changes.

---

## Round 1 — First Impressions (~3 min)

> "Take a minute to read through the code. What's your overall impression? What are the most critical problems?"

---

## Round 2 — Requests & Error Handling (~8 min)

> "The script sometimes crashes silently. Walk me through what happens if the API returns a 500 error or the network drops."

**Follow-up:**
> "How would you add retry logic with exponential backoff? Would you write it yourself or use a library?"

---

## Round 3 — Caching (~8 min)

> "The cache seems to work. Can you spot any problems with it as written?"

**Follow-up:**
> "How would you add a TTL (time-to-live) to the cache without using an external library?"

---

## Round 4 — Async (~10 min)

> "This script fetches 10 cities sequentially. For a dashboard that needs fresh data quickly, this is too slow. How would you make it faster?"

**Follow-up:**
> "What does `asyncio.gather` do vs running them one by one?"

> "What happens if one of the tasks raises an exception inside `gather`?"

> "The API has a rate limit of 5 requests per second. How would you handle that with async code?"

---

## Wrap-up (~5 min)

> "If you had 30 more minutes, what else would you fix or add?"
