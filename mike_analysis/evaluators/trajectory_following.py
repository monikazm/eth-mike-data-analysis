from dataclasses import dataclass

from mike_analysis.core.metric_evaluator import RowDict, MetricEvaluator
from mike_analysis.metrics.motor import MAPR, VelocitySD, NIJ
from mike_analysis.metrics.positional import MinRom, Rom
from mike_analysis.metrics.sensorimotor import RMSError, StdPeakAmplitude, MeanAbsPeakdiff
from mike_analysis.metrics.summary import NumTrials


@dataclass
class _TrajectoryFollowingSeriesEvaluator(MetricEvaluator):
    trial_metrics = (
        RMSError(),
        MAPR(),
        MinRom(),
        Rom(),
        MeanAbsPeakdiff(),
        StdPeakAmplitude(),
        NIJ(),
        VelocitySD(),
    )

    summary_metrics = (
        NumTrials(),
    )


@dataclass
class TrajectoryFollowingEvaluator(MetricEvaluator):
    name_prefix: str = 'TrajectoryFollowing'
    db_result_columns_to_select = ('Fast', )

    series_metric_evaluators = (
        _TrajectoryFollowingSeriesEvaluator('Slow'),
        _TrajectoryFollowingSeriesEvaluator('Fast'),
    )

    @classmethod
    def get_series_idx(cls, db_trial_result: RowDict) -> int:
        return db_trial_result['Fast']
