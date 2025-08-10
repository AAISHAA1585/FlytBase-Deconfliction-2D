from math import sqrt

def calculate_distance(p1, p2):
    """Euclidean distance between two (x, y) points."""
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def check_conflicts(primary_positions, other_positions, safety_radius):
    """
    Compare primary drone positions with other drone positions.
    Return list of conflicts: (time, other_id, distance).
    """
    conflicts = []

    # Convert other drone positions into a dict by time for fast lookup
    other_positions_dict = {}
    for t, x, y in other_positions:
        other_positions_dict[t] = (x, y)

    for t, px, py in primary_positions:
        if t in other_positions_dict:
            ox, oy = other_positions_dict[t]
            dist = calculate_distance((px, py), (ox, oy))
            if dist < safety_radius:
                conflicts.append((t, dist))

    return conflicts
