from dataclasses import dataclass

from mike_analysis.core.metric import DiffMetric
from mike_analysis.core.metric_evaluator import RowDict, MetricEvaluator
from mike_analysis.metrics.motor import MaxForce
from mike_analysis.metrics.positional import MinRom, MaxRom, Rom
from mike_analysis.metrics.summary import NumTrials


@dataclass
class _RomActivePassiveSeriesEvaluator(MetricEvaluator):
    trial_metrics = (
        MinRom(),
        MaxRom(),
        Rom(),
        MaxForce(),
    )

    summary_metrics = (
        NumTrials(),
    )


@dataclass
class _RomAutomaticPassiveSeriesEvaluator(MetricEvaluator):
    trial_metrics = (
        MaxForce(),
    )

    summary_metrics = (
        NumTrials(),
    )


@dataclass
class RomEvaluator(MetricEvaluator):
    name_prefix: str = 'Rom'
    db_result_columns_to_select = ('RomMode', )

    series_metric_evaluators = (
        _RomActivePassiveSeriesEvaluator('Active'),
        _RomActivePassiveSeriesEvaluator('Passive'),
        _RomAutomaticPassiveSeriesEvaluator('Auto'),
    )

    diff_metrics = (DiffMetric(f'Active_{MaxRom.name}_Mean', f'Passive_{MaxRom.name}_Mean', bigger_is_better=False, unit='deg'),
                    DiffMetric(f'Active_{Rom.name}_Mean', f'Passive_{Rom.name}_Mean', bigger_is_better=False, unit='deg'))

    @classmethod
    def get_series_idx(cls, db_trial_result: RowDict) -> int:
        return db_trial_result['RomMode']
