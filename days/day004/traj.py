import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def projectile_trajectory(v0, angle_deg, g=9.81):

    """
    compute projectile trajectory
    """


    theta = np.radians(angle_deg)

    #time of flight
    t_flight = 2 * v0 * np.sin(theta) / g

    #metrics
    range_max = v0 ** 2 * np.sin(2 * theta) / g
    height_max = (v0 * np.sin(theta)) ** 2 / (2 * g)

    t_peak = t_flight / 2

    #time array for smooth curve

    t = np.linspace(0, t_flight, 1000)


    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t ** 2

    return x, y, {
        "range": range_max,
        "max_height": height_max,
        "time_flight": t_flight,
        "t_peak": t_peak,
        "x_peak": v0 * np.cos(theta) * t_peak,
    }


def inp(prompt, lo, hi):


    while True:
        try:
            val = float(input(prompt))
            if lo <= val <= hi:
                return val




            print(f"  Please enter a value between {lo} and {hi}.")
        except ValueError:

            print("  Invalid input — please enter a number.")




print("PROJECTILE MOTION PLOTTER")
print("(no air resistance, flat ground, g = 9.81 m/s²)")


v0 = inp("\nInitial velocity  v₀  [1–500 m/s]: ", 1, 500)

angle = inp("Launch angle      θ   [1–89 °]:    ", 1, 89)

x, y, stats = projectile_trajectory(v0, angle)


fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#0d1117")


from matplotlib.collections import LineCollection
points = np.array([x, y]).T.reshape(-1, 1, 2)
segs = np.concatenate([points[:-1], points[1:]], axis=1)
norm = plt.Normalize(0, x.max())
lc = LineCollection(segs, cmap="plasma", norm=norm, linewidth=2.5, zorder=3)
lc.set_array(x[:-1])
ax.add_collection(lc)


ax.axhline(0, color="#30363d", linewidth=1, zorder=1)
ax.fill_between(x, y, 0, where=(y >= 0), alpha=0.08, color="#a371f7", zorder=2)


ax.plot(stats["x_peak"], stats["max_height"], "o",
            color="#f0e040", markersize=7, zorder=5, label="Peak")
ax.annotate(
    f"  H = {stats['max_height']:.1f} m",
    (stats["x_peak"], stats["max_height"]),
        color="#f0e040", fontsize=9, va="bottom"
)


ax.plot(0, 0, "^", color="#3fb950", markersize=9, zorder=5)
ax.plot(stats["range"], 0, "v", color="#f85149", markersize=9, zorder=5)


info = (
    f"v₀ = {v0} m/s    θ = {angle}°\n"
    f"Range        = {stats['range']:.2f} m\n"
    f"Max height   = {stats['max_height']:.2f} m\n"
    f"Flight time  = {stats['time_flight']:.2f} s"
)
ax.text(
    0.98, 0.97, info, transform=ax.transAxes,
    ha="right", va="top", fontsize=9.5,
    color="#c9d1d9", family="monospace",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#161b22",
            edgecolor="#30363d", alpha=0.9)
)


for spine in ax.spines.values():
    spine.set_color("#30363d")
ax.tick_params(colors="#8b949e", labelsize=9)
ax.set_xlabel("Horizontal distance (m)", color="#8b949e", fontsize=10)
ax.set_ylabel("Height (m)", color="#8b949e", fontsize=10)
ax.set_title(
    f"Projectile Trajectory  —  v₀ = {v0} m/s, θ = {angle}°",
    color="#c9d1d9", fontsize=12, pad=12
)
ax.set_xlim(-stats["range"] * 0.03, stats["range"] * 1.05)
ax.set_ylim(-stats["max_height"] * 0.08, stats["max_height"] * 1.25)
ax.grid(True, color="#21262d", linewidth=0.7, linestyle="--", zorder=0)

legend_items = [
    mpatches.Patch(color="#3fb950", label="Launch"),
    mpatches.Patch(color="#f0e040", label="Peak"),
    mpatches.Patch(color="#f85149", label="Landing"),
]


ax.legend(handles=legend_items, facecolor="#161b22",
        edgecolor="#30363d", labelcolor="#c9d1d9", fontsize=9)

plt.tight_layout()
plt.show()


print(f"\n  Range:       {stats['range']:.3f} m")
print(f"  Max height:  {stats['max_height']:.3f} m")
print(f"  Flight time: {stats['time_flight']:.3f} s\n")


