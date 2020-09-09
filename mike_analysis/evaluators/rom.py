from dataclasses import dataclass

from mike_analysis.core.metric_evaluator import RowType, MetricEvaluator
from mike_analysis.metrics.motor import MaxForce
from mike_analysis.metrics.positional import MinRom, MaxRom, Rom


@dataclass
class _RomActivePassiveSeriesEvaluator(MetricEvaluator):
    trial_metrics = (
        MinRom(),
        MaxRom(),
        Rom(),
        MaxForce(),
    )


@dataclass
class _RomAutomaticPassiveSeriesEvaluator(MetricEvaluator):
    trial_metrics = (
        MaxForce(),
    )


@dataclass
class RomEvaluator(MetricEvaluator):
    name_prefix: str = 'Rom'
    db_result_columns_to_select = ('RomMode', )

    series_metric_computers = (
        _RomActivePassiveSeriesEvaluator('Active'),
        _RomActivePassiveSeriesEvaluator('Passive'),
        _RomAutomaticPassiveSeriesEvaluator('Auto'),
    )

    @classmethod
    def get_series_idx(cls, db_trial_result: RowType) -> int:
        return db_trial_result['RomMode']