from pathlib import Path
import math
import cairosvg

OUT_DIR = Path('/data/.openclaw/workspace/figures')
SVG_PATH = OUT_DIR / 'figure-1b-orbital-ring-local-helical-lanes.svg'
PNG_PATH = OUT_DIR / 'figure-1b-orbital-ring-local-helical-lanes.png'
PDF_PATH = OUT_DIR / 'figure-1b-orbital-ring-local-helical-lanes.pdf'

W, H = 1400, 960
DRAW_LEFT, DRAW_TOP = 320, 110
DRAW_RIGHT, DRAW_BOTTOM = 1140, 830
DRAW_W = DRAW_RIGHT - DRAW_LEFT
DRAW_H = DRAW_BOTTOM - DRAW_TOP

LENGTH = 9.0
RADIUS = 1.34
HELIX_TURNS = 1.14
K = 2.0 * math.pi * HELIX_TURNS / LENGTH

LANES = [
    {
        'id': 'rh_plus',
        'label': 'RH lane, +v',
        'handed': 1.0,
        'direction': 1.0,
        'theta0': math.radians(226.0),
        'color': '#c0392b',
        'hidden': '#ebb0a7',
        'arrow_s': 5.1,
    },
    {
        'id': 'rh_minus',
        'label': 'RH lane, -v',
        'handed': 1.0,
        'direction': -1.0,
        'theta0': math.radians(232.0),
        'color': '#2e86ab',
        'hidden': '#a7cedf',
        'arrow_s': 7.3,
    },
    {
        'id': 'lh_plus',
        'label': 'LH lane, +v',
        'handed': -1.0,
        'direction': 1.0,
        'theta0': math.radians(240.0),
        'color': '#2f9e44',
        'hidden': '#afdcb8',
        'arrow_s': 4.0,
    },
    {
        'id': 'lh_minus',
        'label': 'LH lane, -v',
        'handed': -1.0,
        'direction': -1.0,
        'theta0': math.radians(246.0),
        'color': '#b26b00',
        'hidden': '#e1c288',
        'arrow_s': 6.4,
    },
]


def rot_x(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x, c * y - s * z, s * y + c * z)



def rot_y(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (c * x + s * z, y, -s * x + c * z)



def rot_z(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (c * x - s * y, s * x + c * y, z)



def transform_point(p):
    p = rot_z(p, math.radians(-8.0))
    p = rot_y(p, math.radians(-18.0))
    p = rot_x(p, math.radians(67.0))
    return p



def transform_vector(v):
    return transform_point(v)



def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]



def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )



def norm(v):
    return math.sqrt(dot(v, v))



def normalize(v):
    n = norm(v)
    if n < 1e-9:
        return (0.0, 0.0, 0.0)
    return (v[0] / n, v[1] / n, v[2] / n)



def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])



def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])



def mul(v, s):
    return (v[0] * s, v[1] * s, v[2] * s)



def cylinder_point(s, theta):
    return (s, RADIUS * math.cos(theta), RADIUS * math.sin(theta))



def cylinder_normal(theta):
    return (0.0, math.cos(theta), math.sin(theta))



def s_hat():
    return (1.0, 0.0, 0.0)



def r_hat(theta):
    return normalize(cylinder_normal(theta))



def theta_hat(theta):
    return (0.0, -math.sin(theta), math.cos(theta))



def helix_theta(s, lane):
    return lane['theta0'] + lane['handed'] * K * s



def helix_point(s, lane):
    return cylinder_point(s, helix_theta(s, lane))



def helix_tangent(s, lane):
    theta = helix_theta(s, lane)
    return add(s_hat(), mul(theta_hat(theta), lane['handed'] * RADIUS * K))


cloud = []
for i in range(151):
    s = LENGTH * i / 150.0
    for j in range(181):
        theta = 2.0 * math.pi * j / 180.0
        cloud.append(transform_point(cylinder_point(s, theta)))

min_x = min(x for x, _, _ in cloud)
max_x = max(x for x, _, _ in cloud)
min_y = min(y for _, y, _ in cloud)
max_y = max(y for _, y, _ in cloud)
scale = min(DRAW_W / (max_x - min_x), DRAW_H / (max_y - min_y))
center_model_x = 0.5 * (min_x + max_x)
center_model_y = 0.5 * (min_y + max_y)
center_screen_x = 0.5 * (DRAW_LEFT + DRAW_RIGHT)
center_screen_y = 0.5 * (DRAW_TOP + DRAW_BOTTOM)



def project_model(p):
    x, y, z = transform_point(p)
    sx = center_screen_x + scale * (x - center_model_x)
    sy = center_screen_y - scale * (y - center_model_y)
    return sx, sy, z



def project_vector(v):
    x, y, z = transform_vector(v)
    return (scale * x, -scale * y, z)



def normalize2(v):
    n = math.hypot(v[0], v[1])
    if n < 1e-9:
        return (1.0, 0.0)
    return (v[0] / n, v[1] / n)



def add2(a, b):
    return (a[0] + b[0], a[1] + b[1])



def mul2(v, s):
    return (v[0] * s, v[1] * s)



def path_from_points(points, close=False):
    if not points:
        return ''
    pieces = [f'M {points[0][0]:.2f},{points[0][1]:.2f}']
    pieces.extend(f'L {x:.2f},{y:.2f}' for x, y in points[1:])
    if close:
        pieces.append('Z')
    return ' '.join(pieces)



def split_segments(samples, closed=False):
    seq = list(samples)
    if closed:
        seq = seq + [seq[0]]
    visible = []
    hidden = []
    current = [seq[0][:2]]
    current_hidden = seq[0][2]
    for idx in range(1, len(seq)):
        x0, y0, h0 = seq[idx - 1]
        x1, y1, h1 = seq[idx]
        if h1 == current_hidden:
            current.append((x1, y1))
            continue
        current.append((x1, y1))
        (hidden if current_hidden else visible).append(current)
        current = [(x1, y1)]
        current_hidden = h1
    if current:
        (hidden if current_hidden else visible).append(current)
    return visible, hidden



def surface_visible(theta):
    return transform_vector(cylinder_normal(theta))[2] < 0.0



def helix_samples(lane, count=1000):
    samples = []
    for i in range(count + 1):
        s = LENGTH * i / count
        theta = helix_theta(s, lane)
        x, y, z = project_model(cylinder_point(s, theta))
        hidden = not surface_visible(theta)
        samples.append((x, y, hidden))
    return samples



def rim_samples(s_fixed, count=260):
    samples = []
    for i in range(count + 1):
        theta = 2.0 * math.pi * i / count
        x, y, z = project_model(cylinder_point(s_fixed, theta))
        hidden = not surface_visible(theta)
        samples.append((x, y, hidden))
    return samples



def generator_samples(theta_fixed, count=260):
    samples = []
    for i in range(count + 1):
        s = LENGTH * i / count
        x, y, z = project_model(cylinder_point(s, theta_fixed))
        hidden = not surface_visible(theta_fixed)
        samples.append((x, y, hidden))
    return samples



def arc_points(center, radius, start_deg, end_deg, count=24):
    cx, cy = center
    pts = []
    for i in range(count):
        a = math.radians(start_deg + (end_deg - start_deg) * i / (count - 1))
        pts.append((cx + radius * math.cos(a), cy - radius * math.sin(a)))
    return pts


# Surface polygons.
light_dir = normalize(transform_vector((-0.45, -0.18, 1.0)))
faces = []
N_S = 66
N_T = 34
for i in range(N_S):
    s0 = LENGTH * i / N_S
    s1 = LENGTH * (i + 1) / N_S
    for j in range(N_T):
        th0 = 2.0 * math.pi * j / N_T
        th1 = 2.0 * math.pi * (j + 1) / N_T
        p00 = cylinder_point(s0, th0)
        p10 = cylinder_point(s1, th0)
        p11 = cylinder_point(s1, th1)
        p01 = cylinder_point(s0, th1)
        tp00 = transform_point(p00)
        tp10 = transform_point(p10)
        tp11 = transform_point(p11)
        tp01 = transform_point(p01)
        avg_z = 0.25 * (tp00[2] + tp10[2] + tp11[2] + tp01[2])
        n = normalize(cross(sub(tp10, tp00), sub(tp01, tp00)))
        shade = max(0.0, dot(n, light_dir))
        gray = int(round(234 - 40 * shade))
        color = f'#{gray:02x}{min(gray + 8,255):02x}{min(gray + 16,255):02x}'
        quad = [project_model(p00)[:2], project_model(p10)[:2], project_model(p11)[:2], project_model(p01)[:2]]
        faces.append((avg_z, color, quad))
faces.sort(key=lambda item: item[0])

# Rims and light guide lines.
front_rim_samples = rim_samples(0.0)
rear_rim_samples = rim_samples(LENGTH)
front_rim_visible, front_rim_hidden = split_segments(front_rim_samples, closed=True)
rear_rim_visible, rear_rim_hidden = split_segments(rear_rim_samples, closed=True)

cross_sections = [0.0, LENGTH * 0.48, LENGTH]
generators = [math.radians(26.0), math.radians(208.0)]

lane_geometry = {}
for lane in LANES:
    visible, hidden = split_segments(helix_samples(lane), closed=False)
    lane_geometry[lane['id']] = {'visible': visible, 'hidden': hidden}

# Extended center line and external basis.
centerline_pts = [project_model((LENGTH * i / 240.0, 0.0, 0.0))[:2] for i in range(241)]
axis_dir = normalize2((centerline_pts[-1][0] - centerline_pts[0][0], centerline_pts[-1][1] - centerline_pts[0][1]))
centerline_ext_start = add2(centerline_pts[0], mul2(axis_dir, -170.0))
extended_centerline_pts = [centerline_ext_start] + centerline_pts
basis_origin = add2(centerline_ext_start, mul2(axis_dir, 46.0))

basis_theta = math.radians(236.0)
r_dir = normalize2(project_vector(r_hat(basis_theta))[:2])
s_dir = axis_dir
theta_arc_center = add2(basis_origin, (-1.0, -2.0))

theta_tip = add2(theta_arc_center, (-42.0, -46.0))
r_tip = add2(basis_origin, mul2(r_dir, 80.0))
s_tip = add2(basis_origin, mul2(s_dir, 104.0))
theta_arc_pts = arc_points(theta_arc_center, 36.0, 180.0, 110.0, count=22)
centerline_label = add2(centerline_ext_start, (18.0, 118.0))

# Alpha annotation at the front-face start of one helix.
alpha_lane = LANES[0]
alpha_theta0 = alpha_lane['theta0']
alpha_point = project_model(cylinder_point(0.0, alpha_theta0))[:2]
alpha_s_dir = normalize2(project_vector(s_hat())[:2])
alpha_h_dir = normalize2(project_vector(normalize(helix_tangent(0.0, alpha_lane)))[:2])
alpha_s_end = add2(alpha_point, mul2(alpha_s_dir, 64.0))
alpha_h_end = add2(alpha_point, mul2(alpha_h_dir, 68.0))
ang_s = math.atan2(alpha_s_dir[1], alpha_s_dir[0])
ang_h = math.atan2(alpha_h_dir[1], alpha_h_dir[0])
while ang_h < ang_s:
    ang_h += 2.0 * math.pi
if ang_h - ang_s > math.pi:
    ang_s, ang_h = ang_h, ang_s + 2.0 * math.pi
alpha_arc_pts = []
for i in range(22):
    a = ang_s + (ang_h - ang_s) * i / 21.0
    alpha_arc_pts.append((alpha_point[0] + 28.0 * math.cos(a), alpha_point[1] + 28.0 * math.sin(a)))
alpha_label = add2(alpha_point, (22.0, -20.0))

# Arrow placement on solid segments only.
def visible_arrow_points(lane, s_guess):
    for delta in [0.0, -0.35, 0.35, -0.7, 0.7, -1.0, 1.0]:
        s = max(0.35, min(LENGTH - 0.35, s_guess + delta))
        theta = helix_theta(s, lane)
        if surface_visible(theta):
            p = helix_point(s, lane)
            t = normalize(helix_tangent(s, lane))
            if lane['direction'] > 0:
                a0 = project_model(add(p, mul(t, -0.32)))[:2]
                a1 = project_model(add(p, mul(t, 0.32)))[:2]
            else:
                a0 = project_model(add(p, mul(t, 0.32)))[:2]
                a1 = project_model(add(p, mul(t, -0.32)))[:2]
            return a0, a1
    p = helix_point(s_guess, lane)
    t = normalize(helix_tangent(s_guess, lane))
    return project_model(add(p, mul(t, -0.32)))[:2], project_model(add(p, mul(t, 0.32)))[:2]

arrow_segments = [(lane, *visible_arrow_points(lane, lane['arrow_s'])) for lane in LANES]

# Shell label and legend.
shell_anchor = project_model(cylinder_point(LENGTH * 0.78, math.radians(310.0)))[:2]
shell_label = (980.0, 808.0)
legend_x = 84.0
legend_y = 82.0
legend_w = 246.0
legend_h = 52.0
legend_gap = 12.0

bottom_left_note = (420.0, 936.0)
bottom_right_note = (900.0, 936.0)

parts = []
A = parts.append
A('<?xml version="1.0" encoding="UTF-8"?>')
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
A('  <title id="title">Figure 1b local helical lanes on a prestressed membrane guide shell</title>')
A('  <desc id="desc">Straight local tube segment with four representative helical lanes, center line, local coordinates s r and theta, and a front-face helix angle alpha.</desc>')
A('  <defs>')
A('    <marker id="arrowhead-dark" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#334155"/>')
A('    </marker>')
A('    <marker id="arrowhead-soft" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#64748b"/>')
A('    </marker>')
for lane in LANES:
    A(f'    <marker id="arrowhead-{lane["id"]}" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
    A(f'      <path d="M 0 0 L 12 6 L 0 12 z" fill="{lane["color"]}"/>')
    A('    </marker>')
A('    <style><![CDATA[')
A('      text { font-family: Arial, Helvetica, sans-serif; fill: #1b2430; }')
A('      .shell-face { stroke: none; opacity: 0.97; }')
A('      .shell-guide-front { fill: none; stroke: #8d99aa; stroke-width: 1.45; stroke-linecap: round; stroke-linejoin: round; opacity: 0.74; }')
A('      .shell-guide-back { fill: none; stroke: #d3dbe5; stroke-width: 1.0; stroke-dasharray: 5.5 6.5; stroke-linecap: round; stroke-linejoin: round; opacity: 0.82; }')
A('      .front-rim { fill: #eef4fb; stroke: #8a97aa; stroke-width: 1.7; opacity: 0.92; }')
A('      .rear-rim { fill: none; stroke: #c5cfdb; stroke-width: 1.2; opacity: 0.78; }')
A('      .centerline { fill: none; stroke: #475569; stroke-width: 2.3; stroke-dasharray: 9 7; stroke-linecap: round; opacity: 0.95; }')
A('      .basis { fill: none; stroke: #334155; stroke-width: 2.4; stroke-linecap: round; marker-end: url(#arrowhead-dark); }')
A('      .basis-soft { fill: none; stroke: #64748b; stroke-width: 2.1; stroke-linecap: round; marker-end: url(#arrowhead-soft); }')
A('      .lane-halo-visible { fill: none; stroke: #ffffff; stroke-width: 8.8; stroke-linecap: round; stroke-linejoin: round; opacity: 0.97; }')
A('      .lane-halo-hidden { fill: none; stroke: #ffffff; stroke-width: 6.8; stroke-dasharray: 8 7; stroke-linecap: round; stroke-linejoin: round; opacity: 0.78; }')
A('      .lane-visible { fill: none; stroke-width: 4.8; stroke-linecap: round; stroke-linejoin: round; }')
A('      .lane-hidden { fill: none; stroke-width: 3.4; stroke-dasharray: 8 7; stroke-linecap: round; stroke-linejoin: round; opacity: 0.92; }')
A('      .leader { fill: none; stroke: #9aa8bb; stroke-width: 1.6; stroke-linecap: round; opacity: 0.9; }')
A('      .math { font-size: 28px; font-style: italic; }')
A('      .label-small { font-size: 24px; font-weight: 500; }')
A('      .note { font-size: 17px; fill: #5d6a78; }')
A('      .legend-box { fill: #ffffff; stroke: #d7dee7; stroke-width: 1.4; opacity: 0.97; }')
A('      .legend-swatch { fill: none; stroke-width: 5.8; stroke-linecap: round; }')
A('      .legend-label { font-size: 23px; font-weight: 600; }')
A('      .alpha-ref { fill: none; stroke: #1f2937; stroke-width: 1.9; stroke-linecap: round; }')
A('      .alpha-arc { fill: none; stroke: #1f2937; stroke-width: 1.8; }')
A('      .velocity { fill: none; stroke-width: 2.9; stroke-linecap: round; }')
A('    ]]></style>')
A('  </defs>')
A(f'  <rect width="{W}" height="{H}" fill="#ffffff"/>')
A('')
A('  <g id="guide_shell">')
for _, color, quad in faces:
    A(f'    <path class="shell-face" fill="{color}" d="{path_from_points(quad, close=True)}"/>')
A('    <g id="front_face">')
front_loop = [project_model(cylinder_point(0.0, 2.0 * math.pi * i / 200.0))[:2] for i in range(201)]
A(f'      <path class="front-rim" d="{path_from_points(front_loop, close=True)}"/>')
A('    </g>')
A('    <g id="rear_face">')
for seg in rear_rim_hidden + rear_rim_visible:
    if len(seg) >= 2:
        A(f'      <path class="rear-rim" d="{path_from_points(seg)}"/>')
A('    </g>')
A('    <g id="shell_guides">')
for s_fixed in cross_sections:
    vis, hid = split_segments(rim_samples(s_fixed), closed=True)
    for seg in hid:
        if len(seg) >= 2:
            A(f'      <path class="shell-guide-back" d="{path_from_points(seg)}"/>')
    for seg in vis:
        if len(seg) >= 2:
            A(f'      <path class="shell-guide-front" d="{path_from_points(seg)}"/>')
for theta_fixed in generators:
    vis, hid = split_segments(generator_samples(theta_fixed), closed=False)
    for seg in hid:
        if len(seg) >= 2:
            A(f'      <path class="shell-guide-back" d="{path_from_points(seg)}"/>')
    for seg in vis:
        if len(seg) >= 2:
            A(f'      <path class="shell-guide-front" d="{path_from_points(seg)}"/>')
A('    </g>')
A('  </g>')
A('')
A('  <g id="centerline_group">')
A(f'    <path class="centerline" d="{path_from_points(extended_centerline_pts)}"/>')
A(f'    <text x="{centerline_label[0]:.2f}" y="{centerline_label[1]:.2f}" class="label-small">center line</text>')
A('  </g>')
A('')
A('  <g id="basis_vectors">')
A(f'    <path class="basis" d="M {basis_origin[0]:.2f},{basis_origin[1]:.2f} L {s_tip[0]:.2f},{s_tip[1]:.2f}"/>')
A(f'    <text x="{s_tip[0] + 10:.2f}" y="{s_tip[1] - 8:.2f}" class="math">s</text>')
A(f'    <path class="basis" d="M {basis_origin[0]:.2f},{basis_origin[1]:.2f} L {r_tip[0]:.2f},{r_tip[1]:.2f}"/>')
A(f'    <text x="{r_tip[0] - 16:.2f}" y="{r_tip[1] - 8:.2f}" class="math">r</text>')
A(f'    <path class="basis-soft" d="{path_from_points(theta_arc_pts)}"/>')
A(f'    <text x="{theta_tip[0]:.2f}" y="{theta_tip[1]:.2f}" class="math">θ</text>')
A('  </g>')
A('')
A('  <g id="helical_lanes">')
for lane in LANES:
    geom = lane_geometry[lane['id']]
    for seg in geom['hidden']:
        if len(seg) >= 2:
            A(f'    <path class="lane-halo-hidden" d="{path_from_points(seg)}"/>')
    for seg in geom['visible']:
        if len(seg) >= 2:
            A(f'    <path class="lane-halo-visible" d="{path_from_points(seg)}"/>')
    for seg in geom['hidden']:
        if len(seg) >= 2:
            A(f'    <path class="lane-hidden" stroke="{lane["hidden"]}" d="{path_from_points(seg)}"/>')
    for seg in geom['visible']:
        if len(seg) >= 2:
            A(f'    <path class="lane-visible" stroke="{lane["color"]}" d="{path_from_points(seg)}"/>')
A('  </g>')
A('')
A('  <g id="velocity_arrows">')
for lane, a0, a1 in arrow_segments:
    A(f'    <path class="velocity" stroke="{lane["color"]}" marker-end="url(#arrowhead-{lane["id"]})" d="M {a0[0]:.2f},{a0[1]:.2f} L {a1[0]:.2f},{a1[1]:.2f}"/>')
A('  </g>')
A('')
A('  <g id="helix_angle">')
A(f'    <path class="alpha-ref" d="M {alpha_point[0]:.2f},{alpha_point[1]:.2f} L {alpha_s_end[0]:.2f},{alpha_s_end[1]:.2f}"/>')
A(f'    <path class="alpha-ref" d="M {alpha_point[0]:.2f},{alpha_point[1]:.2f} L {alpha_h_end[0]:.2f},{alpha_h_end[1]:.2f}"/>')
A(f'    <path class="alpha-arc" d="{path_from_points(alpha_arc_pts)}"/>')
A(f'    <text x="{alpha_label[0]:.2f}" y="{alpha_label[1]:.2f}" class="math">α</text>')
A('  </g>')
A('')
A('  <g id="legend">')
for idx, lane in enumerate(LANES):
    by = legend_y + idx * (legend_h + legend_gap)
    A(f'    <rect x="{legend_x:.2f}" y="{by:.2f}" width="{legend_w:.2f}" height="{legend_h:.2f}" rx="12" class="legend-box"/>')
    A(f'    <path class="legend-swatch" stroke="{lane["color"]}" d="M {legend_x + 18:.2f},{by + 27:.2f} L {legend_x + 74:.2f},{by + 27:.2f}"/>')
    A(f'    <text x="{legend_x + 92:.2f}" y="{by + 34:.2f}" class="legend-label">{lane["label"]}</text>')
A('  </g>')
A('')
A('  <g id="shell_callout">')
A(f'    <path class="leader" d="M {shell_label[0] - 24:.2f},{shell_label[1] - 40:.2f} L {shell_anchor[0]:.2f},{shell_anchor[1]:.2f}"/>')
A(f'    <text x="{shell_label[0]:.2f}" y="{shell_label[1]:.2f}" class="label-small">')
A('      <tspan x="{0}" dy="0">prestressed membrane</tspan>'.format(f'{shell_label[0]:.2f}'))
A('      <tspan x="{0}" dy="26">guide shell</tspan>'.format(f'{shell_label[0]:.2f}'))
A('    </text>')
A('  </g>')
A('')
A('  <g id="notes">')
A(f'    <text x="{bottom_left_note[0]:.2f}" y="{bottom_left_note[1]:.2f}" class="note">Only four helical lanes are shown for clarity.</text>')
A(f'    <text x="{bottom_right_note[0]:.2f}" y="{bottom_right_note[1]:.2f}" class="note">Helix angle α exaggerated for clarity.</text>')
A('  </g>')
A('</svg>')

svg = '\n'.join(parts)
SVG_PATH.write_text(svg)

cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=str(PNG_PATH), output_width=W, output_height=H)
cairosvg.svg2pdf(bytestring=svg.encode('utf-8'), write_to=str(PDF_PATH), output_width=W, output_height=H)

print(SVG_PATH)
print(PNG_PATH)
print(PDF_PATH)
