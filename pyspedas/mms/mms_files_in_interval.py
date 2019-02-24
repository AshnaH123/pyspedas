
import re
from dateutil.parser import parse
from bisect import bisect_left

def mms_files_in_interval(in_files, trange):

    file_name = 'mms.*_([0-9]{8,14})_v(\d+).(\d+).(\d+).cdf'

    file_times = []

    regex = re.compile(file_name)

    for file in in_files:
        matches = regex.match(file['file_name'])
        if matches:
            file_times.append((file['file_name'], parse(matches.groups()[0]).timestamp(), file['timetag']))

    # sort in time
    sorted_files = sorted(file_times, key=lambda x: x[1])

    times = [t[1] for t in sorted_files]

    idx_min = bisect_left(times, parse(trange[0]).timestamp())

    # note: purposefully liberal here; include one extra file so that we always get the burst mode data
    if idx_min == 0:
        return [{'file_name': f[0], 'timetag': f[2]} for f in sorted_files[idx_min:]]
    else:
        return [{'file_name': f[0], 'timetag': f[2]} for f in sorted_files[idx_min-1:]]
