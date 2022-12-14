# Standardized column names
from contextlib import contextmanager
from enum import IntEnum, Enum
from timeit import default_timer as timer
from typing import Dict, Any

TimeCol = 'Time'
TrialCol = 'Trial'
TSCol = 'TargetState'
RStateCol = 'RomState'
PosCol = 'Pos'
SPosCol = 'StartingPos'
TPosCol = 'TargetPos'
ForceCol = 'Force'
VelSensorCol = 'VelocityMeasured'

col_names = [TimeCol, TrialCol, TSCol, RStateCol, PosCol,
             SPosCol, TPosCol, ForceCol]  # , VelSensorCol]

# Matching columns names in csv and tdms files
csv_cols = ['Time', 'TrialNr', 'TargetState', 'RomState',
            'Position', 'StartingPosition', 'TargetPosition', 'Force']
tdms_cols = ['Time [s]', 'Trial Nr', 'Target state?', 'ROM State 0-Active 1-Passive 2-Automatic', 'Position [deg]',
             'Starting position [deg]', 'Target Position [deg]', 'Force filtered [N] ']  # , 'Velocity [deg/s]']


class SqlTypes:
    Integer = 'integer'
    Bool = 'integer'
    String = 'varchar'
    Date = 'date'
    Float = 'real'


# Names of these enum entries must match result table names
class Modes(IntEnum):
    RangeOfMotion = 0
    Force = 1
    TargetReaching = 2
    TargetFollowing = 3
    PositionMatch = 4
    PreciseReaching = 5


class ModeResults(IntEnum):
    RangeOfMotionResult = 0
    ForceResult = 1
    TargetReachingResult = 2
    TargetFollowingResult = 3
    PositionMatchResult = 4
    PreciseReachingResult = 5


# Assessment mode descriptions (== name of assessment folders in data folder)
ModeDescs = {
    Modes.RangeOfMotion: 'Range Of Motion Task',
    Modes.Force: 'Force Task',
    Modes.TargetReaching: 'Motor Task',
    Modes.TargetFollowing: 'Sensorimotor Task',
    Modes.PositionMatch: 'Position Matching Task',
    Modes.PreciseReaching: 'Precise Reaching Task'
}


class AssessmentState(IntEnum):
    InProgress = 0
    Aborted = 1
    Discarded = 2
    Finished = 3


class RomPhase(IntEnum):
    Active = 0
    Passive = 1
    AutomaticPassive = 2


class Tables:
    Patient = 'Patient'
    Assessment = 'Assessment'
    Session = 'Session'
    MetricResults = {m: f'{m.name}MetricResult' for m in Modes}
    Results = {m: f'{m.name}Result' for m in Modes}


class RCCols:
    EventName = 'redcap_event_name'
    RepeatInstrument = 'redcap_repeat_instrument'
    RepeatInst = 'redcap_repeat_instance'


class TColor(Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[36m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@contextmanager
def colored_print(color: TColor):
    print(color.value, end='')
    yield
    print(TColor.ENDC.value, end='')


@contextmanager
def time_measured(desc: str):
    start = timer()
    yield
    end = timer()
    print(f'Done with {desc}, elapsed: {end - start:.2f}s')


RowDict = Dict[str, Any]
"""Type representing a result row from a database query (maps column name -> value)"""


def dict_factory(cursor, row) -> RowDict:
    """
    Row factory which can be used with python's sqlite3 module.
    Each database row is returned as a dictionary mapping column names to values.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
