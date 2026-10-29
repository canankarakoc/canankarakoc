"""Research-page figures for ckarakoc.com.

Run from the repository folder:   python3 scripts/research_figures.py
Writes six PNGs to images/research/. One idea per figure and a few large
labels, so they stay readable at the size the Research page and the home-page
cards show them; 16:9 so the cards do not crop them. Colours follow the
conceptual figure in the application packages and the site's teal accent.
Uses the Inter font if it is installed, otherwise the default font.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "research")
plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 22,
                     "axes.linewidth": 2.0, "axes.edgecolor": "#1d2121",
                     "savefig.facecolor": "white"})
INK, MUTED = "#1d2121", "#5d6766"
BLUE, SAND, TEAL = "#6C9BC0", "#D9BD72", "#4E9490"
NAVY, BROWN, DTEAL, MAROON, ACCENT = "#25506F", "#8A5A28", "#1F5F5C", "#7A3F44", "#1f6f6f"
W, H = 8.0, 4.5          # 16:9; saved at 200 dpi -> 1600 x 900 px


def frame(ax, xlabel, ylabel):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(xlabel, fontsize=24, color=INK, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=24, color=INK, labelpad=10)


def save(fig, name):
    fig.savefig(os.path.join(OUT, f"{name}.png"), dpi=200)
    plt.close(fig)


# Top of the Research page: which strategy is favored (energy x predictability)
fig, ax = plt.subplots(figsize=(W, H)); fig.subplots_adjust(0.09, 0.15, 0.97, 0.97)
k = 0.26; x = np.linspace(0.001, 1, 600); yb = np.clip(k / x, 0, 1.4); BAND = 0.30
ax.fill_between(x, yb, 1, where=yb < 1, color=BLUE, alpha=.30, lw=0)
ax.fill_between(x, 0, np.minimum(yb, 1), color=SAND, alpha=.25, lw=0)
ax.fill_between([0, 1], 0, BAND, color=TEAL, alpha=.28, lw=0)
ax.plot(x, yb, color=INK, lw=3)
ax.axhline(BAND, color=MUTED, lw=1.6, ls=(0, (4, 3)))
ax.text(.17, .66, "plasticity,\nbet-hedging", ha="center", va="center", fontsize=27, weight="bold", color=BROWN)
ax.text(.70, .66, "genetic\nadaptation", ha="center", va="center", fontsize=27, weight="bold", color=NAVY)
ax.text(.50, .15, "dormancy, persistence", ha="center", va="center", fontsize=27, weight="bold", color=DTEAL)
frame(ax, "Environmental predictability  →", "Energy  →")
save(fig, "overview-strategies")

# Energy: physiological states of a clonal population as energy runs out
t = np.linspace(0, 1, 500)
act = 1 / (1 + np.exp(9 * (t - 0.44))); dor = 1 / (1 + np.exp(-10 * (t - 0.62)))
per = np.clip(1 - act - dor, 0, None); tot = act + per + dor
act, per, dor = act / tot, per / tot, dor / tot
fig, ax = plt.subplots(figsize=(W, H)); fig.subplots_adjust(0.09, 0.15, 0.97, 0.97)
ax.fill_between(t, 0, act, color=BLUE, alpha=.50, lw=0)
ax.fill_between(t, act, act + per, color=SAND, alpha=.60, lw=0)
ax.fill_between(t, act + per, 1, color=TEAL, alpha=.50, lw=0)
ax.plot(t, act, color=NAVY, lw=2.2); ax.plot(t, act + per, color=DTEAL, lw=2.2)
ax.text(.17, .38, "active", fontsize=30, weight="bold", color=NAVY, ha="center")
ax.text(.53, .52, "persister", fontsize=27, weight="bold", color=BROWN, ha="center", va="center",
        rotation=-38, rotation_mode="anchor")
ax.text(.84, .62, "dormant", fontsize=30, weight="bold", color=DTEAL, ha="center")
frame(ax, "Energy running out  →", "Share of cells")
save(fig, "energy-states")

# Predictability, Research page: how the pieces connect
fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")


def box(cx, cy, w, h, fc, ec):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.45",
                                fc=fc, ec=ec, lw=2.6, zorder=3))


def label(x, y, text, color, fs=27):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, weight="bold", color=color, zorder=4,
            linespacing=1.05)


def arrow(p, q, color=INK, lw=3.2, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=0.9,head_width=0.55", mutation_scale=14,
                                 lw=lw, color=color, linestyle=ls, zorder=2, shrinkA=0, shrinkB=0))


box(3.0, 7.0, 4.4, 1.6, "#f3e6e7", MAROON); label(3.0, 7.0, "pathogen", MAROON)
box(3.0, 3.2, 4.4, 1.9, "#e1ebf3", NAVY);   label(3.0, 3.2, "host\nresponse", NAVY)
box(8.1, 5.1, 3.6, 1.9, "#f6eed8", BROWN);  label(8.1, 5.1, "host\ndamage", BROWN)
box(13.5, 4.9, 4.4, 5.0, "white", INK);     label(13.5, 6.65, "risk of\ndeath", INK, fs=26)
tt = np.linspace(0, 1, 100)
ax.plot(11.95 + 3.0 * tt, 3.05 + 1.85 * tt ** 2.4, color=MAROON, lw=4.2, zorder=4)   # accelerating risk
ax.plot([11.95, 11.95, 15.05], [5.1, 3.05, 3.05], color=INK, lw=1.8, zorder=4)
ax.text(13.5, 2.95, "time", ha="center", va="top", fontsize=17, color=MUTED, zorder=4)
arrow((2.1, 6.15), (2.1, 4.2)); arrow((3.9, 4.2), (3.9, 6.15))                       # respond to each other
arrow((5.25, 6.55), (6.25, 5.85), color=MAROON); arrow((5.25, 3.65), (6.25, 4.35), color=NAVY)
arrow((9.95, 5.0), (11.2, 5.0), lw=4.4)                                                # damage drives death
label(3.0, 0.75, "energy", DTEAL, fs=22)                                                 # next step
arrow((3.0, 1.15), (3.0, 2.2), color=DTEAL, ls=(0, (3, 2)), lw=2.6)
save(fig, "infection-connections")

# Predictability, home-page card: hosts that start alike end differently
rng = np.random.default_rng(11)
fig, ax = plt.subplots(figsize=(W, H)); fig.subplots_adjust(0.09, 0.15, 0.97, 0.97)
t = np.linspace(0, 1, 300); TH = 0.12


def wobble(s):
    e = rng.normal(size=t.size); kern = np.exp(-np.linspace(-3, 3, 61) ** 2); kern /= kern.sum()
    w = np.convolve(e, kern, mode="same"); w -= w[0]
    return s * w * np.clip(t * 6, 0, 1)


for i in range(8):     # same early decline, then recovery at different times
    s = rng.uniform(.55, .9); tmin = rng.uniform(.35, .7); q = s / (2 * tmin)
    ax.plot(t, np.clip(1 - s * t + q * t ** 2 + wobble(.035), TH, 1.0), color=TEAL, lw=2.6, alpha=.9)
for i in range(7):     # same early decline, then an accelerating fall; deaths come late
    s = rng.uniform(.55, .85); Td = rng.uniform(.5, .97); q = (1 - TH - s * Td) / Td ** 3
    h = 1 - s * t - q * t ** 3 + wobble(.03)
    k = np.argmax(h <= TH)
    ax.plot(t[:k + 1], h[:k + 1], color=MAROON, lw=2.6, alpha=.9)
    ax.plot(t[k], TH, marker="x", ms=13, mew=3.2, color=MAROON)
ax.axhline(TH, color=MUTED, lw=1.6, ls=(0, (4, 3)))
ax.text(.995, 1.24, "recover", ha="right", va="top", fontsize=27, weight="bold", color=DTEAL)
ax.text(.53, TH + .03, "die", ha="right", va="bottom", fontsize=27, weight="bold", color=MAROON)
ax.set_xlim(0, 1); ax.set_ylim(0, 1.25); ax.set_xticks([]); ax.set_yticks([])
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
ax.set_xlabel("Time since infection  →", fontsize=24, color=INK, labelpad=10)
ax.set_ylabel("Host health", fontsize=24, color=INK, labelpad=10)
save(fig, "infection-outcomes")

# Noise: same mean and variance, different predictability
rng = np.random.default_rng(7); n = 60


def ar1(phi):
    e = rng.normal(size=n * 4); y = np.zeros_like(e)
    for i in range(1, len(e)):
        y[i] = phi * y[i - 1] + e[i]
    y = y[-n:]
    return (y - y.mean()) / y.std()


fig, axs = plt.subplots(2, 1, figsize=(W, H), sharex=True)
fig.subplots_adjust(0.09, 0.15, 0.97, 0.90, hspace=.42)
for ax, phi, col, lab in [(axs[0], 0.0, MAROON, "unpredictable"), (axs[1], 0.92, DTEAL, "predictable")]:
    y = 1 + .45 * ar1(phi)
    ax.step(np.arange(n), y, where="mid", color=col, lw=2.8)
    ax.axhline(1, color=MUTED, lw=1.4, ls=(0, (4, 3)))
    ax.set_ylim(-.1, 2.3); ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title(lab, loc="left", fontsize=25, weight="bold", color=col, pad=6)
axs[1].set_xlabel("Time (transfers)  →", fontsize=24, color=INK, labelpad=10)
fig.text(.035, .56, "Antibiotic dose", rotation=90, ha="center", va="center", fontsize=24, color=INK)
save(fig, "noise-regimes")

# Community: response diversity keeps the total stable
fig, ax = plt.subplots(figsize=(W, H)); fig.subplots_adjust(0.09, 0.15, 0.97, 0.97)
tt = np.linspace(0, 1, 400)
a = .27 + .17 * np.sin(2 * np.pi * 2.2 * tt); b = .27 - .17 * np.sin(2 * np.pi * 2.2 * tt + .25)
ax.plot(tt, a, color=BLUE, lw=3.5); ax.plot(tt, b, color=SAND, lw=3.5)
ax.plot(tt, a + b + .18, color=ACCENT, lw=5)
ax.text(.99, .88, "total", fontsize=27, weight="bold", color=ACCENT, ha="right")
ax.text(.012, .47, "species A", fontsize=22, weight="bold", color=NAVY)
ax.text(.012, .03, "species B", fontsize=22, weight="bold", color=BROWN)
frame(ax, "Time  →", "Abundance")
save(fig, "community-insurance")

print("wrote 6 figures to", os.path.normpath(OUT))
