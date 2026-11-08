---
name: python-performance
description: >-
  Profile and fix Python runtime, memory, or I/O bottlenecks with evidence (cProfile, py-spy, scalene, memray).
  Not for accuracy/F1/quality KPI loops or unmeasured micro-optimizations.
risk: safe
source: local
date_added: "2026-02-27"
---

# Python Performance Optimization Skill

Find and fix real performance problems. Measure first.

Load `references/implementation-playbook.md` **only** for a named profiler recipe (`cProfile`, `py-spy`, `tracemalloc`, `scalene`). Do not load it for process or policy.

## When to Use
- Slow Python execution, high latency, CPU saturation, or excessive memory RSS
- Data-processing, I/O, or database access that is measurably expensive
- Before/after benchmarking of an optimization or container change

## When Not to Use
- No evidence of a performance problem
- Quality KPIs (accuracy, F1, Hit@K) → **algorithm-optimization**
- Standard Polars/DuckDB query authoring → **polars-duckdb**
- Premature micro-optimization off the critical path

## Related Skills
- Use **aw-first** to trace callers, callees, and symbol surroundings around profiled hotspots (`aw callers`, `aw context`).
- Use **polars-duckdb** when migrating slow Pandas/Python loops to vectorized Polars or DuckDB.
- Use **python-concurrency** when the bottleneck is I/O wait or needs multi-core CPU parallelism.
- Use **pyo3-maturin** when a confirmed CPU hotspot cannot be accelerated further in Python.
- Use **algorithm-optimization** for quality KPIs on real cases, not runtime.

## Core Principles
1. Measure first — never optimize from guesses.
2. Fix the actual hotspot, not the whole codebase.
3. Simple readable fixes and container/representation upgrades before rewrites.
4. Re-measure after each meaningful change in a clean process.
5. Stop when the target is met.

## Optimization Process

### 1. Clarify Goals
Latency, CPU, peak RSS memory, or throughput? Numeric target? Constraints (Python version, dependencies, architecture freeze)?

### 2. Profile with Rigor
- **CPU / runtime**: `py-spy` (non-intrusive sampling for live processes), `cProfile` (deterministic), `scalene`
- **Memory**: `memray` (tracks native C and Python heap allocations, generates flamegraphs), `scalene`, `tracemalloc`
- **Line-level**: `line_profiler`

Use `time.perf_counter` / `timeit`, never `time.time()`. Warm lazy caches, time dataset I/O and compute separately on the same bounded rows, then use `cProfile` or `py-spy` to locate hot calls. Re-time a wrapped hotspot without deterministic profiling before quoting its wall-clock share (`cProfile` magnifies call-heavy functions). Disclose if serialization or disk I/O is inside the timed loop.

### 3. Classify the Bottleneck

| Type | Signs | Direction |
| :--- | :--- | :--- |
| **CPU-bound** | High CPU, pure compute | Better algorithm, vectorization (NumPy/Polars), SIMD libraries, concurrency |
| **I/O-bound** | Waiting on net/disk/DB | Async (`asyncio`), batching, caching, connection pooling |
| **Memory-bound** | High RSS, GC pressure, OOM | `memray` flamegraph, generators, `@dataclass(slots=True)`, `memoryview` |
| **Lookup-table RSS** | Large dict survives load, RSS >> on-disk size | Compact trie (`marisa_trie`) or sorted byte arrays + `numpy.searchsorted` |
| **String/Scanner slicing** | Repeated `text[pos:]` copies in loops | Positional indexing (`re.Pattern.match(text, pos)`) and bounded lookahead |
| **Database** | Slow queries, N+1 queries | Indexes, query projection, batch fetching |
| **Algorithmic** | Scales poorly with `n` (`O(n²)`) | Hash lookups (`set`/`dict`), early exit, prefix trees |

### 4. Apply Fixes (in Order of Leverage)
1. **Better algorithm or data structure** (replace linear scan with `dict`/`set`, positional matching over slicing copies).
2. **Do less work** (`@functools.lru_cache`, column projection in Parquet scans, batching).
3. **Drop-in SIMD / Native Accelerators**:
   - JSON serialization: `orjson` (5x–10x faster than stdlib `json`).
   - Fuzzy matching: `rapidfuzz` (10x–50x faster than pure Python).
   - Large text search: `stringzilla` (SIMD AVX2/NEON).
   - Tabular data: `polars` / `duckdb` over Pandas (`polars-duckdb`).
   - Zero-copy slicing: `memoryview` and `bytearray`.
   - Object memory footprint: `@dataclass(slots=True)` (40–60% lower RAM than standard dicts/classes).
   - Large static lookup tables (`>1M` keys): Re-encode `dict[str, int]` (~100 B/entry in RSS) into `marisa_trie.BytesTrie` or sorted arrays + `numpy.searchsorted` (up to 25x RSS reduction with zero accuracy loss; always measure RSS in a fresh process).
4. **Concurrency or parallelism** when workload matches (`python-concurrency`).
5. **Rust native extension** (`pyo3-maturin`) last, only after Python options are exhausted.

### 5. Validate
Run the exact baseline benchmark on the same inputs, verify bit-for-bit or parity correctness, and confirm the speedup or RSS reduction justifies the added code complexity.

#### 5a. Separate the ratio from the absolute number

A single median on a loaded machine is not a result. Report the A/B ratio as the durable
claim and the absolute rate as environment-dependent:

1. **Interleave the two configurations inside one process**, alternating runs, so both see
   the same load. Measure the speedup as a ratio of medians, not as two numbers from two
   separate invocations.
   ```python
   on, off = rate(), rate_with_flag_disabled()   # same process, same inputs
   speedup = median(on) / median(off)
   ```
   A flag or constructor argument that disables the optimisation makes this trivial and
   doubles as the regression test.
2. **Run the sweep, not one point.** Throughput on a shared host varies by +/-15% or more.
   Take 5+ independent runs and report median *and* min-max range. Accuracy should be
   bit-identical across runs; if it varies, that is a bug, not noise.
3. **Check host load before blaming the code.** A load average above core count, or a
   desktop compositor/renderer consuming 30%+ CPU, invalidates absolute throughput
   comparison. Say so in the report rather than quoting the low number as a regression.
4. **Do not force timing with scheduling hacks.** Lowering process priority (`taskpolicy -b`,
   `nice -19`, background QoS) measures the scheduler, not the code — a 4x slowdown under
   background QoS says nothing about the optimisation. Measure at normal priority and
   report the variance instead.
5. **Re-measure after the optimisation changes the shape of the work.** A container swap that
   deletes 20% of a lookup table changes both time and memory; report throughput delta and
   RSS delta together, and do not attribute the whole throughput gain to the algorithmic
   change if part of it came from having less data.

When the measured gain sits below the significance bar you set *before* running (for example
< 0.05 absolute accuracy, or a speedup inside the noise band), report it as not significant
and keep the previous default. A change that is real but too small to matter is a finding,
not a reason to switch.

## Output Expectations
- Bottleneck diagnosis backed by profiler output
- Prioritized changes applied
- Before/after table (wall-clock latency, throughput, peak RSS in a fresh process)
- Explicit trade-offs

## Final Checklist
- [ ] Goal and numeric constraints defined
- [ ] Profiled before changing (`time.perf_counter`, `py-spy`/`cProfile`/`memray`)
- [ ] Bottleneck type classified
- [ ] Changes target the measured hotspot
- [ ] Re-measured in a clean process with correctness preserved
