import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

def animate_drones(primary_positions, others_positions_dict, conflicts, save_path=None):
    """
    Animate drone movements and highlight conflict regions.
    primary_positions: list of (datetime, x, y)
    others_positions_dict: { drone_id: [(datetime,x,y), ...] }
    conflicts: list of (datetime, distance)
    save_path: if provided (str) try to save animation, otherwise show on screen
    """

    if not primary_positions:
        print("Error: No primary positions to animate.")
        return

    times = [t for t, _, _ in primary_positions]

    xs = [x for _, x, _ in primary_positions]
    ys = [y for _, _, y in primary_positions]
    for pos_list in others_positions_dict.values():
        xs.extend([x for _, x, _ in pos_list])
        ys.extend([y for _, _, y in pos_list])

    if not xs or not ys:
        xmin = -10; xmax = 10; ymin = -10; ymax = 10
    else:
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

    pad_x = max(5, (xmax - xmin) * 0.1)
    pad_y = max(5, (ymax - ymin) * 0.1)

    fig, ax = plt.subplots()
    ax.set_title("Drone Conflict Visualization")
    ax.set_xlim(xmin - pad_x, xmax + pad_x)
    ax.set_ylim(ymin - pad_y, ymax + pad_y)
    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")

    # Artists for drones
    primary_scatter, = ax.plot([], [], 'bo', markersize=10, label="Primary")
    others_scatters = {
        drone_id: ax.plot([], [], 'go', markersize=10, label=f"Drone {drone_id}")[0]
        for drone_id in others_positions_dict
    }

    # Artists for conflict region
    conflict_circle = patches.Circle((0, 0), radius=5, color='red', alpha=0.3, visible=False, zorder=2, label="Conflict Region")
    ax.add_patch(conflict_circle)
    conflict_marker, = ax.plot([], [], 'rX', markersize=12, markeredgewidth=2, visible=False, zorder=3, label="Conflict Point")
    
    # Legend setup
    # Create proxy artists for the legend to show all labels correctly
    proxy_handles = [
        plt.Line2D([0], [0], marker='o', color='b', label='Primary', linestyle=''),
        plt.Line2D([0], [0], marker='o', color='g', label='Simulated', linestyle=''),
        patches.Patch(color='red', alpha=0.3, label='Conflict Region'),
        plt.Line2D([0], [0], marker='x', color='r', markersize=10, markeredgewidth=2, label='Conflict Point', linestyle='')
    ]
    ax.legend(handles=proxy_handles, loc='upper right')

    def init():
        primary_scatter.set_data([], [])
        for s in others_scatters.values():
            s.set_data([], [])
        conflict_circle.set_visible(False)
        conflict_marker.set_data([], [])
        return [primary_scatter, conflict_circle, conflict_marker] + list(others_scatters.values())

    def update(frame):
        t = times[frame]

        # Update primary drone position
        _, px, py = primary_positions[frame]
        primary_scatter.set_data([px], [py])

        # Update other drones' positions
        for drone_id, scatter in others_scatters.items():
            pos_list = others_positions_dict[drone_id]
            match = next((p for p in pos_list if p[0] == t), None)
            if match:
                _, ox, oy = match
                scatter.set_data([ox], [oy])
            else:
                scatter.set_data([], [])

        # Update conflict markers
        conflict_detected = any(c[0] == t for c in conflicts)
        if conflict_detected:
            # We assume the conflict location is near the primary drone for this simple 2D example
            conflict_circle.center = (px, py)
            conflict_circle.set_visible(True)
            conflict_marker.set_data([px], [py])
            conflict_marker.set_visible(True)
        else:
            conflict_circle.set_visible(False)
            conflict_marker.set_visible(False)

        return [primary_scatter, conflict_circle, conflict_marker] + list(others_scatters.values())

    ani = animation.FuncAnimation(fig, update, frames=len(times),
                                 init_func=init, blit=False, interval=200)

    if save_path:
        try:
            ani.save(save_path, writer='pillow')
            print(f"Saved animation to {save_path}")
        except Exception as e:
            print("Could not save animation (writer error):", e)
            print("Showing animation instead.")
            plt.show()
    else:
        plt.show()