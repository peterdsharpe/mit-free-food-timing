from get_data import times
from datetime import datetime
import numpy as np
from aerosandbox.tools.pretty_plots import mpl, plt, sns, show_plot

sns.set_style('ticks')

### Clean the data
times = np.array(times)

valid_range = (
    datetime(year=1900, month=1, day=1, hour=18, minute=42),
    datetime(year=1900, month=1, day=1, hour=21)
)
plot_range = (
    datetime(year=1900, month=1, day=1, hour=18, minute=30),
    datetime(year=1900, month=1, day=1, hour=21)
)

times = times[np.logical_and(times > valid_range[0], times < valid_range[1])]

### Set a time format
time_formatter = mpl.dates.DateFormatter("%I:%M %p")

### Compute statistics about the data
email_send_time = datetime(year=1900, month=1, day=1, hour=18, minute=43)
median_latency = np.median(np.array([
    time - email_send_time for time in times
]))
median_response_time = email_send_time + median_latency

### Plot the data
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the responses
sns.histplot(
    times,
    bins=30,
    kde=True
)

# Plot the email send time
plt.axvline(x=email_send_time, ls='--', color="k")
plt.text(
    x=email_send_time,
    y=0.9 * ax.get_ylim()[1] + (1 - 0.9) * ax.get_ylim()[0],
    s=f"Email sent ({email_send_time.time().__format__('%I:%M %p')})",
    color="k",
    horizontalalignment='right',
    verticalalignment='top',
    rotation=90
)

# Plot the median response
plt.axvline(x=median_response_time, ls='--', color="k")
plt.text(
    x=median_response_time,
    y=0.9 * ax.get_ylim()[1] + (1 - 0.9) * ax.get_ylim()[0],
    s=f"Median receipt time\n({median_response_time.time().__format__('%I:%M %p')}, {int(np.round(median_latency.seconds / 60))} min)",
    color="k",
    horizontalalignment='right',
    verticalalignment='top',
    rotation=90
)

# Format and show
ax.xaxis.set_major_formatter(time_formatter)
ax.xaxis.set_major_locator(mpl.dates.MinuteLocator([0, 30]))
ax.xaxis.set_minor_locator(mpl.dates.MinuteLocator([0, 10, 20, 30, 40, 50]))
plt.xlim(*plot_range)
plt.gcf().autofmt_xdate(rotation=45, ha='center')

show_plot(
    f"Email Latency of free-food@mit.edu and free-foods@mit.edu (N={len(times)})",
    "Receipt Time",
    pretty_grids=False,
    show=False
)
plt.savefig("plot.png", dpi=300)
plt.show()
