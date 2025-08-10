from datetime import datetime, timedelta

def interpolate_positions(waypoints, times):
    """
    Given waypoints [[x1, y1], [x2, y2], ...]
    and times [t1, t2, ...] in ISO format strings,
    return a list of (time, x, y) for each second.
    """
    # Convert string times to datetime
    time_points = [datetime.fromisoformat(t.replace("Z", "+00:00")) for t in times]

    all_positions = []

    for i in range(len(waypoints) - 1):
        start_wp = waypoints[i]
        end_wp = waypoints[i + 1]
        start_time = time_points[i]
        end_time = time_points[i + 1]

        total_seconds = int((end_time - start_time).total_seconds())

        for s in range(total_seconds + 1):  # include endpoint
            frac = s / total_seconds
            x = start_wp[0] + frac * (end_wp[0] - start_wp[0])
            y = start_wp[1] + frac * (end_wp[1] - start_wp[1])
            all_positions.append((start_time + timedelta(seconds=s), x, y))

    return all_positions
