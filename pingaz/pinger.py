'''
fping wrapper
'''

import re
import subprocess


def ping(hosts):
    '''fetch latency on target'''

    base_command = [
        'fping',
        '-C11',
        '-B1',
        '-r1',
    ]

    procs = []
    for h in hosts:
        if type(h) == dict:
            name = h['name']
            host = h['host']
        else:
            name = host = h

        procs += [
            {
                'name': name,
                'host': host,
                'proc': subprocess.Popen(
                    base_command + [host],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ),
            },
        ]

    results = {}
    for p in procs:
        out, err = p['proc'].communicate(timeout=30)
        if p['proc'].returncode > 0:
            results[p['host']] = False
            continue

        matches = re.findall(
            r'^{host}\s*:\s*\[(\d+)\], (?:\d+) bytes, ([\d.]+) ms \((?:[\d.]+) avg, (\d+)% loss\)$'.format(host=re.escape(p['host'])),
            out.decode(),
            re.IGNORECASE|re.MULTILINE
        )

        total_matches = len(matches)
        if total_matches == 0:
            results[p['host']] = False
            continue

        total_loss = 0
        total_latency = 0

        # skip the first which might by dirty
        for match in matches[1:]:
            total_latency += float(match[1])
            total_loss += int(match[2])

        results[p['host']] = {
            'host': p['host'],
            'name': p['name'],
            'latency': round(total_latency / (total_matches - 1), 2),
            'loss': round(total_loss / (total_matches - 1), 2),
        }

    return results
