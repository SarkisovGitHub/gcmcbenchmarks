__version__ = '1.0.0'


from . import templates
from . import parsers
from . import analysis

# Fill top namespace
from .parsers.general_parser import (
    find_simdirs,
    find_equil,
    grab_all_results,
    parse,
    make_Series,
)
from .parsers.time_parser import (
    parse_timefile,
    parse_all_timefiles,
    parse_cpuinfo,
    get_times,
)
from .analysis import find_equil, find_tau
