# Pair Programming Interview Simulation

**Time:** 20–40 minutes  
**File to work on:** `bad_code.py`

---

## Scenario

You've just joined a team. A colleague wrote a script to fetch weather data for a list of cities and save a summary report. It works, but it's slow and fragile. Your job is to review and improve it together with the interviewer.

The interviewer will drive the conversation with questions, but you're expected to identify problems, explain tradeoffs, and write improved code.

---

## Interviewer Script (read these one at a time, give ~5 min per section)

### Warm-up (~3 min)
> "Take a minute to read through the code. What's your overall impression? What stands out as the most critical problems?"

**What to listen for:**
- Mentions performance (sequential requests)
- Mentions the broken cache (no TTL)
- Notices the bare `except:` clauses
- Spots the hardcoded API key

---

### Round 1 — Requests & Error Handling (~8 min)

> "The script sometimes crashes silently. Walk me through what happens if the API returns a 500 error or the network drops."

**Key issues in the code:**
- `r.json()` will raise if the response body isn't JSON (e.g., on a 500)
- `r` is never checked for `.status_code` — no `.raise_for_status()`
- `except:` in `get_temperature` and `process_cities` swallows everything, including `KeyboardInterrupt`
- No retry logic

**Follow-up if they get it easily:**
> "How would you add retry logic with exponential backoff? Would you write it yourself or use a library?"

**Expected answer direction:** `requests` + `urllib3.util.retry` or `tenacity`. Should know the concept of jitter.

---

### Round 2 — Caching (~8 min)

> "The cache seems to work. Can you spot any problems with it as written?"

**Key issues:**
- Cache never expires — stale data forever
- Cache is a module-level global dict — not thread-safe
- No max size — unbounded memory growth
- `get_all_weather` calls the cache, but `get_all_forecasts` does NOT — inconsistent
- Re-fetches weather a second time in `get_hottest_city` (via `get_temperature` → `get_weather_cached`) even though results are already in memory

**Follow-up:**
> "How would you add a TTL (time-to-live) to the cache without using an external library?"

**Expected answer direction:** Store `(value, timestamp)` tuples; compare `time.time()` on read. Or use `functools.lru_cache` with a wrapper. Or `cachetools.TTLCache`.

---

### Round 3 — Async (~10 min)

> "This script fetches 10 cities sequentially. For a dashboard that needs fresh data quickly, this is too slow. How would you make it faster?"

**Key issues:**
- `get_all_weather` and `get_all_forecasts` are both sequential loops — 20 serial HTTP calls
- The `time.sleep(0.5)` in `get_all_forecasts` makes it even worse (artificial, but blocking)
- Two separate loops fetch current + forecast for each city — could batch them

**What you want to see them write (or sketch):**

```python
import asyncio
import aiohttp

async def get_weather_async(session, city):
    url = f"{BASE_URL}/current.json"
    params = {"key": API_KEY, "q": city}
    async with session.get(url, params=params) as r:
        r.raise_for_status()
        return await r.json()

async def get_all_weather_async(cities):
    async with aiohttp.ClientSession() as session:
        tasks = [get_weather_async(session, city) for city in cities]
        return await asyncio.gather(*tasks)
```

**Follow-up questions:**
> "What does `asyncio.gather` do vs running them one by one?"
> "What happens if one of the tasks raises an exception inside `gather`?"

**Expected:** By default `gather` raises on first exception. Mention `return_exceptions=True` to get all results/errors.

> "The API has a rate limit of 5 requests per second. How would you handle that with async code?"

**Expected answer direction:** Semaphore (`asyncio.Semaphore(5)`), or a rate-limiter like `aiolimiter`.

---

### Wrap-up (~5 min)

> "If you had 30 more minutes, what else would you fix or add?"

**Things that could be mentioned:**
- Config management (env vars / `.env` file for the API key)
- Separate concerns — split fetching, processing, and I/O into distinct functions/classes
- Type hints
- Logging instead of `print`
- Unit tests (mock the HTTP calls)
- The function `process_cities` is a god function — split it up

---

## Scoring Rubric

| Area | Weak | Strong |
|---|---|---|
| Error handling | Mentions it vaguely | Specific: `.raise_for_status()`, typed exceptions, retry |
| Caching | Notices it works | Identifies TTL, thread-safety, and memory issues |
| Async | "Use threads" or vague | Writes `asyncio`/`aiohttp` code, explains `gather` semantics |
| Code quality | Lists problems | Prioritizes, proposes concrete fixes, discusses tradeoffs |
| Communication | Thinks silently | Narrates reasoning, asks clarifying questions |

---

## Tips for the Candidate

- Don't try to fix everything — **prioritize out loud**
- It's fine to say "I'd use a library for X" — just name it and explain why
- For async, you don't need to remember exact syntax; explaining the model (event loop, coroutines, gather) matters more
- Ask clarifying questions: "Is this a single-process app? Are we okay adding dependencies?"
