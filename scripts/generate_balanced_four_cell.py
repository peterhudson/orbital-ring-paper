#!/usr/bin/env python3
import math
from pathlib import Path

import cairosvg

W = 1200
H = 900
CX = 330
CY = 585
SCALE = 1.08
LENGTH = 700.0
RADIUS = 92.0
TURNS = 0.96
SAMPLES = 1200
LANE_X0 = 16.0
LANE_X1 = LENGTH - 16.0

OUT_DIR = Path('/data/.openclaw/workspace/figures')
OUT_DIR.mkdir(parents=True, exist_ok=True)
SVG_PATH = OUT_DIR / 'balanced-four-cell-clean.svg'
PNG_PATH = OUT_DIR / 'balanced-four-cell-clean.png'
PDF_PATH = OUT_DIR / 'balanced-four-cell-clean.pdf'

COLORS = {
    'ink': '#1f2937',
    'soft': '#64748b',
    'rim': '#8fa1b5',
    'rear_rim': '#cbd5e1',
    'surface': '#eaf1f8',
    'face': '#f3f7fb',
    'center': '#475569',
    'rh_pos': '#c0392b',
    'lh_pos': '#2f9e44',
    'rh_neg': '#2e86ab',
    'lh_neg': '#b26b00',
    'rh_pos_hidden': '#e4aba3',
    'lh_pos_hidden': '#a8d6b1',
    'rh_neg_hidden': '#a8cee2',
    'lh_neg_hidden': '#e0bc8f',
}

LANES = [
    {
        'key': 'rh_pos',
        'label': 'RH (+p)',
        'handedness': +1,
        'phase': 0.08 * math.tau,
        'momentum': +1,
    },
    {
        'key': 'lh_pos',
        'label': 'LH (+p)',
        'handedness': -1,
        'phase': 0.33 * math.tau,
        'momentum': +1,
    },
    {
        'key': 'rh_neg',
        'label': 'RH (-p)',
        'handedness': +1,
        'phase': 0.58 * math.tau,
        'momentum': -1,
    },
    {
        'key': 'lh_neg',
        'label': 'LH (-p)',
        'handedness': -1,
        'phase': 0.83 * math.tau,
        'momentum': -1,
    },
]


def mm(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def mv(m, v):
    return (
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
    )


def rz(a):
    c = math.cos(a)
    s = math.sin(a)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]


def ry(a):
    c = math.cos(a)
    s = math.sin(a)
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]


ROT = mm(rz(math.radians(35)), ry(math.radians(-47)))


def project_local(x, y, z):
    X, Y, Z = mv(ROT, (x, y, z))
    return (CX + SCALE * X, CY - SCALE * Y, Z)


def helix_point(x, handedness, phase):
    lane_u = (x - LANE_X0) / (LANE_X1 - LANE_X0)
    theta = handedness * (math.tau * TURNS * lane_u) + phase
    return project_local(x, RADIUS * math.cos(theta), RADIUS * math.sin(theta))


def axis_point(x):
    return project_local(x, 0, 0)


def sample_circle(x, n=220):
    pts = []
    for i in range(n):
        t = math.tau * i / n
        pts.append(project_local(x, RADIUS * math.cos(t), RADIUS * math.sin(t)))
    return pts


def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])


def perp(v):
    return (-v[1], v[0])


def unit(v):
    n = math.hypot(v[0], v[1])
    return (v[0] / n, v[1] / n)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def path_from_points(points):
    if not points:
        return ''
    return 'M ' + ' '.join(f'{x:.2f},{y:.2f}' if i == 0 else f'L {x:.2f},{y:.2f}' for i, (x, y, *_rest) in enumerate(points))


def svg_path_from_xy(points):
    if not points:
        return ''
    out = [f'M {points[0][0]:.2f},{points[0][1]:.2f}']
    for x, y in points[1:]:
        out.append(f'L {x:.2f},{y:.2f}')
    return ' '.join(out)


def split_visible_hidden(points):
    visible = []
    hidden = []
    current = []
    current_vis = None
    for pt in points:
        depth = pt[2]
        axis_depth = axis_point(pt[3])[2]
        vis = depth >= axis_depth
        if current_vis is None:
            current_vis = vis
            current = [pt]
        elif vis == current_vis:
            current.append(pt)
        else:
            if current_vis:
                visible.append(current)
            else:
                hidden.append(current)
            current = [current[-1], pt]
            current_vis = vis
    if current:
        if current_vis:
            visible.append(current)
        else:
            hidden.append(current)
    return visible, hidden


def lane_segments(handedness, phase):
    pts = []
    for i in range(SAMPLES + 1):
        x = LANE_X0 + (LANE_X1 - LANE_X0) * i / SAMPLES
        px, py, pz = helix_point(x, handedness, phase)
        pts.append((px, py, pz, x))
    return split_visible_hidden(pts)


def find_extreme_angles():
    a0 = axis_point(0)
    a1 = axis_point(LENGTH)
    axis_vec = unit(vec(a0, a1))
    n = unit(perp(axis_vec))
    candidates = []
    for i in range(720):
        t = math.tau * i / 720
        p = project_local(0, RADIUS * math.cos(t), RADIUS * math.sin(t))
        candidates.append((dot((p[0] - a0[0], p[1] - a0[1]), n), t))
    top = max(candidates)[1]
    bottom = min(candidates)[1]
    return top, bottom


def sample_edge(theta, x_values):
    return [project_local(x, RADIUS * math.cos(theta), RADIUS * math.sin(theta)) for x in x_values]


def ellipse_arc(x, theta0, theta1, steps=80):
    pts = []
    delta = theta1 - theta0
    if delta <= -math.pi:
        delta += math.tau
    elif delta > math.pi:
        delta -= math.tau
    for i in range(steps + 1):
        t = theta0 + delta * i / steps
        pts.append(project_local(x, RADIUS * math.cos(t), RADIUS * math.sin(t)))
    return pts


def pick_arrow_point(handedness, phase, momentum, target):
    x_target, y_target, x_lo, x_hi = target
    best = None
    for i in range(1000):
        x = LANE_X0 + (LANE_X1 - LANE_X0) * i / 999
        if not (x_lo <= x <= x_hi):
            continue
        p = helix_point(x, handedness, phase)
        axis_d = axis_point(x)[2]
        if p[2] < axis_d:
            continue
        score = -abs(x - x_target) - 0.55 * abs(p[1] - y_target)
        if best is None or score > best[0]:
            best = (score, x)
    if best is None:
        for i in range(1000):
            x = LANE_X0 + (LANE_X1 - LANE_X0) * i / 999
            p = helix_point(x, handedness, phase)
            axis_d = axis_point(x)[2]
            if p[2] < axis_d:
                continue
            score = -abs(x - x_target) - 0.55 * abs(p[1] - y_target)
            if best is None or score > best[0]:
                best = (score, x)
    x = best[1]
    dx = 20.0
    x0 = max(LANE_X0, min(LANE_X1, x - momentum * dx))
    x1 = max(LANE_X0, min(LANE_X1, x + momentum * dx))
    p0 = helix_point(x0, handedness, phase)
    p1 = helix_point(x1, handedness, phase)
    return (p0[0], p0[1]), (p1[0], p1[1])


def text(x, y, value, cls='', extra=''):
    class_attr = f' class="{cls}"' if cls else ''
    extra_attr = f' {extra}' if extra else ''
    return f'<text x="{x:.2f}" y="{y:.2f}"{class_attr}{extra_attr}>{value}</text>'


def line_path(points):
    return ' '.join([f'M {points[0][0]:.2f},{points[0][1]:.2f}', f'L {points[1][0]:.2f},{points[1][1]:.2f}'])


def main():
    top_angle, bottom_angle = find_extreme_angles()
    xs = [LENGTH * i / 120 for i in range(121)]
    top_edge = sample_edge(top_angle, xs)
    bottom_edge = sample_edge(bottom_angle, xs)

    rear_top = project_local(LENGTH, RADIUS * math.cos(top_angle), RADIUS * math.sin(top_angle))
    rear_bottom = project_local(LENGTH, RADIUS * math.cos(bottom_angle), RADIUS * math.sin(bottom_angle))
    front_top = project_local(0, RADIUS * math.cos(top_angle), RADIUS * math.sin(top_angle))
    front_bottom = project_local(0, RADIUS * math.cos(bottom_angle), RADIUS * math.sin(bottom_angle))

    side_poly = [(p[0], p[1]) for p in top_edge] + [(p[0], p[1]) for p in reversed(bottom_edge)]
    side_path = svg_path_from_xy(side_poly) + ' Z'

    front_arc = ellipse_arc(0, bottom_angle, top_angle, 90)
    rear_arc = ellipse_arc(LENGTH, top_angle, bottom_angle, 90)
    front_face = svg_path_from_xy([(p[0], p[1]) for p in front_arc]) + ' Z'

    front_ellipse = sample_circle(0, 240)
    rear_ellipse = sample_circle(LENGTH, 240)

    lanes_svg = []
    legend_rows = []
    arrow_regions = {
        'rh_pos': (0.18 * LENGTH, 570, LANE_X0, 0.36 * LENGTH),
        'lh_pos': (0.12 * LENGTH, 520, LANE_X0, 0.36 * LENGTH),
        'rh_neg': (0.77 * LENGTH, 430, 0.40 * LENGTH, LANE_X1),
        'lh_neg': (0.58 * LENGTH, 505, 0.30 * LENGTH, 0.82 * LENGTH),
    }

    for lane in LANES:
        visible, hidden = lane_segments(lane['handedness'], lane['phase'])
        hidden_key = lane['key'] + '_hidden'
        for seg in hidden:
            xy = [(p[0], p[1]) for p in seg]
            if len(xy) < 2:
                continue
            lanes_svg.append(
                f'<path d="{svg_path_from_xy(xy)}" class="lane-hidden" stroke="{COLORS[hidden_key]}" />'
            )
        for seg in visible:
            xy = [(p[0], p[1]) for p in seg]
            if len(xy) < 2:
                continue
            lanes_svg.append(
                f'<path d="{svg_path_from_xy(xy)}" class="lane-visible" stroke="{COLORS[lane["key"]]}" />'
            )
        a0, a1 = pick_arrow_point(lane['handedness'], lane['phase'], lane['momentum'], arrow_regions[lane['key']])
        lanes_svg.append(
            f'<path d="{line_path((a0, a1))}" class="velocity" stroke="{COLORS[lane["key"]]}" marker-end="url(#{lane["key"]}_arrow)" />'
        )
        legend_rows.append((lane['label'], COLORS[lane['key']]))

    center0 = axis_point(-55)
    center1 = axis_point(LENGTH + 70)

    basis_origin = (142, 742)
    r_tip = (112, 675)
    s_tip = (215, 706)
    theta_arc = 'M 163,722 A 40,40 0 0 1 127,695'

    legend_x = 88
    legend_y = 90
    legend_w = 312
    legend_h = 196

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="dark_arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS['ink']}" />
    </marker>
    <marker id="soft_arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS['soft']}" />
    </marker>
    <marker id="rh_pos_arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS['rh_pos']}" />
    </marker>
    <marker id="lh_pos_arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS['lh_pos']}" />
    </marker>
    <marker id="rh_neg_arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS['rh_neg']}" />
    </marker>
    <marker id="lh_neg_arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS['lh_neg']}" />
    </marker>
    <style><![CDATA[
      text {{ font-family: Arial, Helvetica, sans-serif; fill: {COLORS['ink']}; }}
      .shell-surface {{ fill: {COLORS['surface']}; opacity: 0.93; stroke: {COLORS['rim']}; stroke-width: 1.55; stroke-linejoin: round; }}
      .front-face {{ fill: {COLORS['face']}; opacity: 0.985; stroke: {COLORS['rim']}; stroke-width: 1.8; }}
      .rear-rim {{ fill: none; stroke: {COLORS['rear_rim']}; stroke-width: 1.35; stroke-dasharray: 6 7; opacity: 0.98; }}
      .front-rim {{ fill: none; stroke: {COLORS['rim']}; stroke-width: 1.9; opacity: 0.97; }}
      .surface-guide {{ fill: none; stroke: #d6dee8; stroke-width: 1.05; opacity: 0.86; }}
      .shell-edge {{ fill: none; stroke: {COLORS['rim']}; stroke-width: 1.55; opacity: 0.92; }}
      .centerline {{ fill: none; stroke: {COLORS['center']}; stroke-width: 2.3; stroke-dasharray: 10 8; stroke-linecap: round; }}
      .lane-visible {{ fill: none; stroke-width: 4.9; stroke-linecap: round; stroke-linejoin: round; }}
      .lane-hidden {{ fill: none; stroke-width: 3.0; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 7 7; opacity: 0.82; }}
      .velocity {{ fill: none; stroke-width: 3.0; stroke-linecap: round; }}
      .basis {{ fill: none; stroke: {COLORS['ink']}; stroke-width: 2.4; stroke-linecap: round; marker-end: url(#dark_arrow); }}
      .basis-soft {{ fill: none; stroke: {COLORS['soft']}; stroke-width: 2.2; stroke-linecap: round; marker-end: url(#soft_arrow); }}
      .theta-arc {{ fill: none; stroke: {COLORS['ink']}; stroke-width: 1.8; marker-end: url(#dark_arrow); }}
      .label-small {{ font-size: 24px; font-weight: 500; }}
      .note {{ font-size: 18px; fill: #5d6a78; }}
      .legend-box {{ fill: #ffffff; stroke: #d7dee7; stroke-width: 1.4; opacity: 0.98; }}
      .legend-title {{ font-size: 24px; font-weight: 700; }}
      .legend-label {{ font-size: 21px; font-weight: 600; }}
      .legend-swatch {{ fill: none; stroke-width: 6; stroke-linecap: round; }}
    ]]></style>
  </defs>
  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" />
  <g id="legend">
    <rect x="{legend_x}" y="{legend_y}" width="{legend_w}" height="{legend_h}" rx="12" class="legend-box" />
    <text x="{legend_x + 18}" y="{legend_y + 34}" class="legend-title">Balanced Four-Cell Lanes</text>
    <text x="{legend_x + 18}" y="{legend_y + 57}" class="note">Conceptual, not to scale</text>
    {''.join(f'<path d="M {legend_x + 18},{legend_y + 82 + i*31} L {legend_x + 74},{legend_y + 82 + i*31}" class="legend-swatch" stroke="{color}" />' + f'<text x="{legend_x + 90}" y="{legend_y + 89 + i*31}" class="legend-label">{label}</text>' for i, (label, color) in enumerate(legend_rows))}
  </g>
  <g id="guide_shell">
    <path d="{side_path}" class="shell-surface" />
    <path d="{front_face}" class="front-face" />
    <path d="{svg_path_from_xy([(p[0], p[1]) for p in rear_ellipse])} Z" class="rear-rim" />
    <path d="M {front_top[0]:.2f},{front_top[1]:.2f} L {rear_top[0]:.2f},{rear_top[1]:.2f}" class="surface-guide" />
    <path d="M {front_bottom[0]:.2f},{front_bottom[1]:.2f} L {rear_bottom[0]:.2f},{rear_bottom[1]:.2f}" class="surface-guide" />
    <path d="M {front_top[0]:.2f},{front_top[1]:.2f} L {rear_top[0]:.2f},{rear_top[1]:.2f}" class="shell-edge" />
    <path d="M {front_bottom[0]:.2f},{front_bottom[1]:.2f} L {rear_bottom[0]:.2f},{rear_bottom[1]:.2f}" class="shell-edge" />
    <path d="{svg_path_from_xy([(p[0], p[1]) for p in front_ellipse])} Z" class="front-rim" />
  </g>
  <g id="centerline_group">
    <path d="M {center0[0]:.2f},{center0[1]:.2f} L {center1[0]:.2f},{center1[1]:.2f}" class="centerline" />
    {text(857, 258, 'center line', 'label-small')}
  </g>
  <g id="helical_lanes">
    {''.join(lanes_svg)}
  </g>
  <g id="basis_vectors">
    <path d="M {basis_origin[0]},{basis_origin[1]} L {r_tip[0]},{r_tip[1]}" class="basis" />
    <path d="M {basis_origin[0]},{basis_origin[1]} L {s_tip[0]},{s_tip[1]}" class="basis-soft" />
    <path d="{theta_arc}" class="theta-arc" />
    {text(r_tip[0] - 18, r_tip[1] - 8, '<tspan font-style="italic">r</tspan>', 'label-small')}
    {text(s_tip[0] + 6, s_tip[1] - 2, '<tspan font-style="italic">s</tspan>', 'label-small')}
    {text(118, 719, '<tspan font-style="italic">θ</tspan>', 'label-small')}
  </g>
  <g id="notes">
    {text(472, 806, 'Helix angle α exaggerated for clarity.', 'note')}
  </g>
</svg>
'''

    SVG_PATH.write_text(svg)
    cairosvg.svg2png(url=str(SVG_PATH), write_to=str(PNG_PATH), output_width=1600)
    cairosvg.svg2pdf(url=str(SVG_PATH), write_to=str(PDF_PATH))
    print(SVG_PATH)
    print(PNG_PATH)
    print(PDF_PATH)


if __name__ == '__main__':
    main()
