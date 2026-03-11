import pandas as pd


def compare(current, baseline, higher_is_better=True):
    """
    Classify current vs baseline — five states:
      significantly above / slightly above / stable / slightly below / significantly below
    Thresholds:  change < 1%: stable, 1-5%: slight, > 5%: significant
    """
    # guard: can't compute a meaningful delta
    if baseline == 0 or pd.isna(current):
        return dict(
            icon="circle-minus", theme="secondary", badge="no data", label="no data"
        )

    # percentage change relative to baseline; sign tells direction
    pct = (current - baseline) / abs(baseline) * 100

    # "good" depends on context: higher MPG is good, lower HP is good for efficiency
    is_good = (pct > 0) if higher_is_better else (pct < 0)
    abs_pct = abs(pct)

    # badge string shown below the value: e.g. "+5.6 (+24.3%) vs overall avg"
    sign = "+" if pct >= 0 else ""
    badge = f"{sign}{current - baseline:.1f} ({sign}{pct:.1f}%) vs overall avg"

    # under 1% change — treat as noise, no colour signal
    if abs_pct < 1:
        return dict(
            icon="arrow-right",
            theme="secondary",
            badge="≈ stable vs overall avg",
            label="stable",
        )

    # direction: matching FA icon
    icon = "arrow-trend-up" if pct > 0 else "arrow-trend-down"

    # colour: good changes are green (success ≥5%, teal <5%),
    #         bad changes are red (danger ≥5%, warning <5%)
    theme = (
        "success"
        if (is_good and abs_pct >= 5)
        else "teal" if is_good else "danger" if abs_pct >= 5 else "warning"
    )

    quantifier = "significantly" if abs_pct >= 5 else "slightly"
    return dict(
        icon=icon,
        theme=theme,
        badge=badge,
        label=f"{quantifier} {'above' if pct > 0 else 'below'} avg",
    )
