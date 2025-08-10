from deconflict.io import load_mission
from deconflict.trajectory import interpolate_positions
from deconflict.detector import check_conflicts
from deconflict.visualizer import animate_drones
from datetime import datetime, timedelta

def assign_times_evenly(waypoints, time_window):
    """Generate evenly spaced times for waypoints based on total mission time."""
    start_time = datetime.fromisoformat(time_window[0].replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(time_window[1].replace("Z", "+00:00"))
    total_seconds = int((end_time - start_time).total_seconds())
    num_segments = len(waypoints) - 1
    segment_time = total_seconds // num_segments
    return [(start_time + timedelta(seconds=i * segment_time)).isoformat() for i in range(len(waypoints))]

def main():
    # Load missions
    primary = load_mission("scenarios/primary.json")
    others = load_mission("scenarios/others.json")

    # Assign times to primary if not provided
    if "times" in primary:
        primary_times = primary["times"]
    else:
        primary_times = assign_times_evenly(primary["waypoints"], primary["time_window"])

    # Get primary positions
    primary_positions = interpolate_positions(primary["waypoints"], primary_times)

    safety_radius = 5.0  # meters
    all_conflicts = []
    others_positions_dict = {}

    # Check conflicts once for each other drone
    for other in others:
        other_positions = interpolate_positions(other["waypoints"], other["times"])
        others_positions_dict[other['id']] = other_positions
        conflicts = check_conflicts(primary_positions, other_positions, safety_radius)
        all_conflicts.extend(conflicts)

        if conflicts:
            print(f"Conflict detected with {other['id']}:")
            for t, dist in conflicts:
                print(f"  Time: {t}, Distance: {dist:.2f} m")
        else:
            print(f"No conflict with {other['id']}")

    # Animate once
    animate_drones(primary_positions, others_positions_dict, all_conflicts, save_path="demo/conflict_animation.gif")

if __name__ == "__main__":
    main()
