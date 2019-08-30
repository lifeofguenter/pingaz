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
    for host in hosts:
        procs.append(subprocess.Popen(
            base_command + [host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ))

    results = {}
    for i, p in enumerate(procs):
        out, err = p.communicate(timeout=30)
        if p.returncode > 0:
            results[hosts[i]] = False
            continue

        matches = re.findall(
            r'^{host}\s*:\s*\[(\d+)\], (?:\d+) bytes, ([\d.]+) ms \((?:[\d.]+) avg, (\d+)% loss\)$'.format(host=re.escape(hosts[i])),
            out.decode(),
            re.IGNORECASE|re.MULTILINE
        )

        total_matches = len(matches)
        if total_matches == 0:
            results[hosts[i]] = False
            continue

        total_loss = 0
        total_latency = 0

        # skip the first which might by dirty
        for match in matches[1:]:
            total_latency += float(match[1])
            total_loss += int(match[2])

        results[hosts[i]] = {
            'host': hosts[i],
            'latency': round(total_latency / (total_matches - 1), 2),
            'loss': round(total_loss / (total_matches - 1), 2),
        }

    return results
