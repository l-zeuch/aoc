import math
import statistics
import timeit

from typing import Any, Dict, Iterable

def bench_func(func, arg, repeat=10):
    # create a callable wrapper for timeit
    wrapper = lambda: func(arg)
    timer = timeit.Timer(wrapper)
    number, _ = timer.autorange()  # determine a reasonable loop count
    raw = timer.repeat(repeat=repeat, number=number)
    per_iter = [t / number for t in raw]

    mean = statistics.mean(per_iter)
    stdev = statistics.stdev(per_iter) if len(per_iter) > 1 else 0.0
    minimum = min(per_iter)
    maximum = max(per_iter)

    return {
        "func": getattr(func, "__name__", str(func)),
        "number": number,
        "repeat": repeat,
        "mean": mean,
        "std_dev": stdev,
        "min": minimum,
        "max": maximum,
        "per_iter": per_iter,
    }

def print_stats(r: Dict[str, Any]) -> None:
    print(f"{r['func']}:")
    print(f"  loops per measurement : {r['number']}")
    print(f"  measurements (repeat) : {r['repeat']}")
    print(f"  mean (s)              : {r['mean']:.9f}")
    print(f"  std_dev (s)           : {r['std_dev']:.9f}")
    print(f"  min (s)               : {r['min']:.9f}")
    print(f"  max (s)               : {r['max']:.9f}")

# --- statistical comparison considering standard deviations ---
def _cohens_d(mean1, mean2, s1, s2, n1, n2) -> float:
    """Compute pooled Cohen's d (small-sample pooled sd)."""
    # if pooled SD cannot be computed (e.g., n1+n2-2 == 0), return infinity-like
    denom = (n1 + n2 - 2)
    if denom <= 0:
        return float("inf")
    pooled_var = ((n1 - 1) * (s1 ** 2) + (n2 - 1) * (s2 ** 2)) / denom
    if pooled_var <= 0:
        return float("inf")
    pooled_sd = math.sqrt(pooled_var)
    return (mean2 - mean1) / pooled_sd

def _welch_t_and_df(mean1, mean2, s1, s2, n1, n2):
    """Return (t_stat, df) for Welch's t-test comparing mean1 vs mean2."""
    # t = (mean2 - mean1) / sqrt(s1^2/n1 + s2^2/n2)
    se1 = (s1 ** 2) / n1
    se2 = (s2 ** 2) / n2
    denom = se1 + se2
    if denom == 0:
        return float("inf"), float("inf")
    t = (mean2 - mean1) / math.sqrt(denom)
    # Welch-Satterthwaite df
    num = denom ** 2
    den = 0.0
    if n1 > 1:
        den += (se1 ** 2) / (n1 - 1)
    if n2 > 1:
        den += (se2 ** 2) / (n2 - 1)
    df = num / den if den != 0 else float("inf")
    return t, df

def _p_value_from_t(t_stat, df):
    """Compute two-sided p-value for Student's t.
    Prefer scipy if available for accuracy; otherwise use normal approximation.
    """
    # try scipy first (more accurate)
    try:
        from scipy import stats  # type: ignore
        p = stats.t.sf(abs(t_stat), df) * 2
        method = "scipy.stats.t"
        return p, method
    except Exception:
        # fallback: normal approximation (reasonable for moderate/large df)
        # p = 2 * (1 - Phi(|t|)) where Phi is standard normal CDF
        z = abs(t_stat)
        # standard normal survival function using erfc
        p = math.erfc(z / math.sqrt(2))
        method = "normal-approx"
        return p, method

def print_comparison(a: Dict[str, Any], b: Dict[str, Any]) -> None:
    """
    Compare a (baseline) to b (other). Show absolute and relative differences,
    but also use the standard deviations to compute Welch's t, df, p-value,
    and Cohen's d (effect size).
    """
    mean_a = a["mean"]
    mean_b = b["mean"]
    s_a = a["std_dev"]
    s_b = b["std_dev"]
    n_a = len(a["per_iter"])
    n_b = len(b["per_iter"])

    # basic diffs
    abs_diff = mean_b - mean_a
    pct = (abs_diff / mean_a * 100.0) if mean_a != 0 else float("inf")
    ratio = (mean_b / mean_a) if mean_a != 0 else float("inf")

    # stats-aware metrics
    t_stat, df = _welch_t_and_df(mean_a, mean_b, s_a, s_b, n_a, n_b)
    p_value, p_method = _p_value_from_t(t_stat, df)
    try:
        cohens = _cohens_d(mean_a, mean_b, s_a, s_b, n_a, n_b)
    except Exception:
        cohens = float("nan")

    # interpretation
    alpha = 0.05
    significant = (p_value < alpha) if (p_value is not None and not math.isnan(p_value)) else False
    faster = a["func"] if mean_a < mean_b else b["func"]
    faster_note = f"{faster} is faster" if mean_a != mean_b else "equal speed"

    print("Comparison (baseline -> other):")
    print(f"  baseline : {a['func']}")
    print(f"  other    : {b['func']}")
    print(f"  mean diff (other - baseline): {abs_diff:+.9f} s")
    print(f"  relative (other vs baseline): {pct:+.3f} %")
    print(f"  ratio (other / baseline)    : {ratio:.3f} x")
    print()
    print("Statistics-aware comparison:")
    print(f"  Welch t-statistic   : {t_stat:.6f}")
    print(f"  Welch df            : {df:.2f}")
    if p_value is not None:
        print(f"  p-value (two-sided) : {p_value:.6g}  [method: {p_method}]")
    else:
        print(f"  p-value: unavailable")
    print(f"  Cohen's d (effect)  : {cohens:.3f}")
    print(f"  alpha (threshold)   : {alpha}")
    print(f"  significant?        : {significant}")
    print(f"  conclusion          : {faster_note}")
    print()
