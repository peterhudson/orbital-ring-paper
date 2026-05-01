from pathlib import Path
import math
import cairosvg

OUT_DIR = Path('/data/.openclaw/workspace/figures')
SVG_PATH = OUT_DIR / 'figure-1b-orbital-ring-local-helical-lanes.svg'
PNG_PATH = OUT_DIR / 'figure-1b-orbital-ring-local-helical-lanes.png'
PDF_PATH = OUT_DIR / 'figure-1b-orbital-ring-local-helical-lanes.pdf'

W, H = 1400, 960
MARGIN_X = 130
MARGIN_Y = 110

R_MAJOR = 8.3
R_TUBE = 1.38
PHI_MIN = -0.58
PHI_MAX = 0.62
HELIX_RATE = 5.75

N_PHI = 48
N_THETA = 28

LANES = [
    {
        'id': 'rh_plus',
        'label': 'RH lane, +v',
        'handed': 1.0,
        'direction': 1.0,
        'theta0': 0.30,
        'color': '#c0392b',
        'hidden': '#e5a39b',
        'arrow_phi': -0.18,
    },
    {
        'id': 'rh_minus',
        'label': 'RH lane, -v',
        'handed': 1.0,
        'direction': -1.0,
        'theta0': math.pi + 0.10,
        'color': '#2e86ab',
        'hidden': '#9bc8da',
        'arrow_phi': 0.26,
    },
    {
        'id': 'lh_plus',
        'label': 'LH lane, +v',
        'handed': -1.0,
        'direction': 1.0,
        'theta0': 1.55,
        'color': '#2f9e44',
        'hidden': '#a8d9b3',
        'arrow_phi': 0.08,
    },
    {
        'id': 'lh_minus',
        'label': 'LH lane, -v',
        'handed': -1.0,
        'direction': -1.0,
        'theta0': 4.55,
        'color': '#b26b00',
        'hidden': '#e2c28c',
        'arrow_phi': 0.45,
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
    p = rot_z(p, math.radians(-27.0))
    p = rot_y(p, math.radians(16.0))
    p = rot_x(p, math.radians(71.5))
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



def centerline(phi):
    return (R_MAJOR * math.cos(phi), R_MAJOR * math.sin(phi), 0.0)



def basis(phi):
    n = (math.cos(phi), math.sin(phi), 0.0)
    t = (-math.sin(phi), math.cos(phi), 0.0)
    b = (0.0, 0.0, 1.0)
    return t, n, b



def tube_point(phi, theta):
    t, n, b = basis(phi)
    radial = add(mul(n, math.cos(theta)), mul(b, math.sin(theta)))
    return add(centerline(phi), mul(radial, R_TUBE))



def tube_normal(phi, theta):
    _, n, b = basis(phi)
    return normalize(add(mul(n, math.cos(theta)), mul(b, math.sin(theta))))



def theta_hat(phi, theta):
    _, n, b = basis(phi)
    return normalize(add(mul(n, -math.sin(theta)), mul(b, math.cos(theta))))



def s_hat(phi):
    t, _, _ = basis(phi)
    return normalize(t)



def helix_theta(phi, lane):
    return lane['theta0'] + lane['handed'] * HELIX_RATE * (phi - PHI_MIN)



def helix_point(phi, lane):
    return tube_point(phi, helix_theta(phi, lane))



def helix_tangent(phi, lane):
    theta = helix_theta(phi, lane)
    t_hat = s_hat(phi)
    th_hat = theta_hat(phi, theta)
    tangential = mul(t_hat, R_MAJOR + R_TUBE * math.cos(theta))
    azimuthal = mul(th_hat, lane['handed'] * R_TUBE * HELIX_RATE)
    return add(tangential, azimuthal)


# Fit the projected geometry to the canvas.
cloud = []
for i in range(101):
    phi = PHI_MIN + (PHI_MAX - PHI_MIN) * i / 100.0
    for j in range(121):
        theta = 2.0 * math.pi * j / 120.0
        x, y, z = transform_point(tube_point(phi, theta))
        cloud.append((x, y, z))

min_x = min(x for x, _, _ in cloud)
max_x = max(x for x, _, _ in cloud)
min_y = min(y for _, y, _ in cloud)
max_y = max(y for _, y, _ in cloud)
scale = min((W - 2 * MARGIN_X) / (max_x - min_x), (H - 2 * MARGIN_Y) / (max_y - min_y))
center_model_x = 0.5 * (min_x + max_x)
center_model_y = 0.5 * (min_y + max_y)
center_screen_x = 0.5 * W
center_screen_y = 0.5 * H + 14.0



def project_model(p):
    x, y, z = transform_point(p)
    sx = center_screen_x + scale * (x - center_model_x)
    sy = center_screen_y - scale * (y - center_model_y)
    return sx, sy, z



def project_vector(v):
    x, y, z = transform_vector(v)
    return (scale * x, -scale * y, z)



def vector2(a, b):
    return (b[0] - a[0], b[1] - a[1])



def length2(v):
    return math.hypot(v[0], v[1])



def normalize2(v):
    n = length2(v)
    if n < 1e-6:
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
    if not samples:
        return [], []
    seq = samples + [samples[0]] if closed else list(samples)
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



def screen_visibility_from_normal(phi, theta):
    return transform_vector(tube_normal(phi, theta))[2] < 0.0



def helix_samples(lane, count=900):
    samples = []
    for i in range(count + 1):
        phi = PHI_MIN + (PHI_MAX - PHI_MIN) * i / count
        theta = helix_theta(phi, lane)
        x, y, z = project_model(tube_point(phi, theta))
        hidden = not screen_visibility_from_normal(phi, theta)
        samples.append((x, y, hidden))
    return samples



def iso_phi_samples(phi, count=220):
    samples = []
    for i in range(count + 1):
        theta = 2.0 * math.pi * i / count
        x, y, z = project_model(tube_point(phi, theta))
        hidden = not screen_visibility_from_normal(phi, theta)
        samples.append((x, y, hidden))
    return samples



def iso_theta_samples(theta, count=260):
    samples = []
    for i in range(count + 1):
        phi = PHI_MIN + (PHI_MAX - PHI_MIN) * i / count
        x, y, z = project_model(tube_point(phi, theta))
        hidden = not screen_visibility_from_normal(phi, theta)
        samples.append((x, y, hidden))
    return samples



def arc_points(center, radius, start_deg, end_deg, count=24):
    cx, cy = center
    pts = []
    for i in range(count):
        a = math.radians(start_deg + (end_deg - start_deg) * i / (count - 1))
        pts.append((cx + radius * math.cos(a), cy - radius * math.sin(a)))
    return pts


# Tube surface polygons with light shading.
light_dir = normalize(transform_vector((-0.35, -0.15, 1.0)))
faces = []
for i in range(N_PHI):
    phi0 = PHI_MIN + (PHI_MAX - PHI_MIN) * i / N_PHI
    phi1 = PHI_MIN + (PHI_MAX - PHI_MIN) * (i + 1) / N_PHI
    for j in range(N_THETA):
        th0 = 2.0 * math.pi * j / N_THETA
        th1 = 2.0 * math.pi * (j + 1) / N_THETA
        p00 = tube_point(phi0, th0)
        p10 = tube_point(phi1, th0)
        p11 = tube_point(phi1, th1)
        p01 = tube_point(phi0, th1)
        tp00 = transform_point(p00)
        tp10 = transform_point(p10)
        tp11 = transform_point(p11)
        tp01 = transform_point(p01)
        avg_z = 0.25 * (tp00[2] + tp10[2] + tp11[2] + tp01[2])
        n = normalize(cross(sub(tp10, tp00), sub(tp01, tp00)))
        shade = max(0.0, dot(n, light_dir))
        gray = int(round(233 - 42 * shade))
        color = f'#{gray:02x}{gray + 7:02x}{gray + 14:02x}'
        quad = [project_model(p00)[:2], project_model(p10)[:2], project_model(p11)[:2], project_model(p01)[:2]]
        faces.append((avg_z, color, quad))
faces.sort(key=lambda item: item[0])

# Shell guide curves.
circ_curves = [PHI_MIN, 0.02, PHI_MAX]
long_curves = [0.15, 2.75]

# Center line.
centerline_pts = [project_model(centerline(PHI_MIN + (PHI_MAX - PHI_MIN) * i / 260.0))[:2] for i in range(261)]

# Helical lane paths.
lane_geometry = {}
for lane in LANES:
    samples = helix_samples(lane)
    visible, hidden = split_segments(samples)
    lane_geometry[lane['id']] = {'visible': visible, 'hidden': hidden}

# Extend the center line into the clear front area and move basis vectors there.
front_dir = normalize2(vector2(centerline_pts[0], centerline_pts[24]))
centerline_ext_start = add2(centerline_pts[0], mul2(front_dir, -215.0))
extended_centerline_pts = [centerline_ext_start] + centerline_pts
centerline_label = add2(centerline_ext_start, (74.0, 20.0))

basis_origin = add2(centerline_ext_start, (60.0, -118.0))
front_s_dir = normalize2(project_vector(s_hat(PHI_MIN))[:2])
front_r_dir = normalize2(project_vector(tube_normal(PHI_MIN, 4.85))[:2])
front_s_tip = add2(basis_origin, mul2(front_s_dir, 128.0))
front_r_tip = add2(basis_origin, mul2(front_r_dir, 94.0))
theta_arc_pts = arc_points(add2(basis_origin, (20.0, -2.0)), 48.0, 210.0, 106.0, count=26)

# Helix-angle annotation for one lane only.
rep_lane = LANES[0]
rep_phi = -0.10
rep_theta = helix_theta(rep_phi, rep_lane)
rep_p = project_model(tube_point(rep_phi, rep_theta))[:2]
rep_s_dir = normalize2(project_vector(s_hat(rep_phi))[:2])
rep_helix_dir = normalize2(project_vector(normalize(helix_tangent(rep_phi, rep_lane)))[:2])
alpha_s_end = add2(rep_p, mul2(rep_s_dir, 70.0))
alpha_h_end = add2(rep_p, mul2(rep_helix_dir, 72.0))
ang_s = math.atan2(rep_s_dir[1], rep_s_dir[0])
ang_h = math.atan2(rep_helix_dir[1], rep_helix_dir[0])
while ang_h < ang_s:
    ang_h += 2 * math.pi
if ang_h - ang_s > math.pi:
    ang_s, ang_h = ang_h, ang_s + 2 * math.pi
alpha_arc_pts = []
for i in range(24):
    t = i / 23.0
    a = ang_s + t * (ang_h - ang_s)
    alpha_arc_pts.append((rep_p[0] + 36.0 * math.cos(a), rep_p[1] + 36.0 * math.sin(a)))
alpha_label_pos = add2(rep_p, (26.0, -30.0))
alpha_note_pos = add2(rep_p, (118.0, -82.0))

# Shell label and legend.
shell_anchor = project_model(tube_point(0.18, 5.55))[:2]
shell_label = (1008.0, 818.0)
legend_x = 84.0
legend_y = 78.0
legend_w = 246.0
legend_h = 52.0
legend_gap = 12.0

# Velocity arrows, one on each lane.
arrow_segments = []
for lane in LANES:
    phi = lane['arrow_phi']
    p0 = helix_point(phi, lane)
    tangent = normalize(helix_tangent(phi, lane))
    if lane['direction'] > 0:
        a0 = project_model(add(p0, mul(tangent, -0.38)))[:2]
        a1 = project_model(add(p0, mul(tangent, 0.38)))[:2]
    else:
        a0 = project_model(add(p0, mul(tangent, 0.38)))[:2]
        a1 = project_model(add(p0, mul(tangent, -0.38)))[:2]
    arrow_segments.append((lane, a0, a1))

parts = []
A = parts.append
A('<?xml version="1.0" encoding="UTF-8"?>')
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
A('  <title id="title">Figure 1b local helical lanes on a prestressed membrane guide shell</title>')
A('  <desc id="desc">Close view of a gently curved guide-shell tube segment with four helical lanes, an extended local center line and basis vectors, and one annotated helix angle alpha.</desc>')
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
A('      text { font-family: Arial, Helvetica, sans-serif; fill: #18212d; }')
A('      .shell-face { stroke: none; opacity: 0.96; }')
A('      .shell-guide-front { fill: none; stroke: #8694a3; stroke-width: 1.55; stroke-linecap: round; stroke-linejoin: round; opacity: 0.72; }')
A('      .shell-guide-back { fill: none; stroke: #cfd7e1; stroke-width: 1.05; stroke-dasharray: 5 6; stroke-linecap: round; stroke-linejoin: round; opacity: 0.78; }')
A('      .centerline { fill: none; stroke: #475569; stroke-width: 2.3; stroke-dasharray: 9 7; stroke-linecap: round; opacity: 0.95; }')
A('      .basis { fill: none; stroke: #334155; stroke-width: 2.5; stroke-linecap: round; marker-end: url(#arrowhead-dark); }')
A('      .basis-soft { fill: none; stroke: #64748b; stroke-width: 2.2; stroke-linecap: round; marker-end: url(#arrowhead-soft); }')
A('      .lane-halo-visible { fill: none; stroke: #ffffff; stroke-width: 8.8; stroke-linecap: round; stroke-linejoin: round; opacity: 0.96; }')
A('      .lane-halo-hidden { fill: none; stroke: #ffffff; stroke-width: 6.8; stroke-dasharray: 8 7; stroke-linecap: round; stroke-linejoin: round; opacity: 0.76; }')
A('      .lane-visible { fill: none; stroke-width: 4.8; stroke-linecap: round; stroke-linejoin: round; }')
A('      .lane-hidden { fill: none; stroke-width: 3.5; stroke-dasharray: 8 7; stroke-linecap: round; stroke-linejoin: round; opacity: 0.92; }')
A('      .leader { fill: none; stroke: #94a3b8; stroke-width: 2.0; stroke-linecap: round; }')
A('      .math { font-size: 30px; font-style: italic; }')
A('      .math-caret { font-size: 18px; font-style: normal; }')
A('      .label-small { font-size: 24px; font-weight: 500; }')
A('      .note { font-size: 18px; fill: #556270; }')
A('      .legend-box { fill: #ffffff; stroke: #d7dee7; stroke-width: 1.4; opacity: 0.97; }')
A('      .legend-swatch { fill: none; stroke-width: 5.8; stroke-linecap: round; }')
A('      .legend-label { font-size: 23px; font-weight: 600; }')
A('      .alpha-ref { fill: none; stroke: #1f2937; stroke-width: 2.0; stroke-linecap: round; }')
A('      .alpha-arc { fill: none; stroke: #1f2937; stroke-width: 1.9; }')
A('      .velocity { fill: none; stroke-width: 2.6; stroke-linecap: round; }')
A('    ]]></style>')
A('  </defs>')
A(f'  <rect width="{W}" height="{H}" fill="#ffffff"/>')
A('')
A('  <g id="guide_shell">')
for _, color, quad in faces:
    A(f'    <path class="shell-face" fill="{color}" d="{path_from_points(quad, close=True)}"/>')
A('    <g id="shell_guides">')
for phi in circ_curves:
    vis, hid = split_segments(iso_phi_samples(phi), closed=True)
    for seg in hid:
        if len(seg) >= 2:
            A(f'      <path class="shell-guide-back" d="{path_from_points(seg)}"/>')
    for seg in vis:
        if len(seg) >= 2:
            A(f'      <path class="shell-guide-front" d="{path_from_points(seg)}"/>')
for theta in long_curves:
    vis, hid = split_segments(iso_theta_samples(theta), closed=False)
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
A('  <g id="basis_vectors">')
A(f'    <path class="basis" d="M {basis_origin[0]:.2f},{basis_origin[1]:.2f} L {front_s_tip[0]:.2f},{front_s_tip[1]:.2f}"/>')
A(f'    <text x="{front_s_tip[0] + 12:.2f}" y="{front_s_tip[1] - 8:.2f}" class="math">s</text>')
A(f'    <text x="{front_s_tip[0] + 28:.2f}" y="{front_s_tip[1] - 24:.2f}" class="math-caret">^</text>')
A(f'    <path class="basis" d="M {basis_origin[0]:.2f},{basis_origin[1]:.2f} L {front_r_tip[0]:.2f},{front_r_tip[1]:.2f}"/>')
A(f'    <text x="{front_r_tip[0] - 8:.2f}" y="{front_r_tip[1] - 10:.2f}" class="math">r</text>')
A(f'    <text x="{front_r_tip[0] + 8:.2f}" y="{front_r_tip[1] - 26:.2f}" class="math-caret">^</text>')
A(f'    <path class="basis-soft" d="{path_from_points(theta_arc_pts)}"/>')
A(f'    <text x="{theta_arc_pts[-1][0] + 14:.2f}" y="{theta_arc_pts[-1][1] - 4:.2f}" class="math">θ</text>')
A(f'    <text x="{theta_arc_pts[-1][0] + 31:.2f}" y="{theta_arc_pts[-1][1] - 20:.2f}" class="math-caret">^</text>')
A('  </g>')
A('')
A('  <g id="helix_angle">')
A(f'    <path class="alpha-ref" d="M {rep_p[0]:.2f},{rep_p[1]:.2f} L {alpha_s_end[0]:.2f},{alpha_s_end[1]:.2f}"/>')
A(f'    <path class="alpha-ref" d="M {rep_p[0]:.2f},{rep_p[1]:.2f} L {alpha_h_end[0]:.2f},{alpha_h_end[1]:.2f}"/>')
A(f'    <path class="alpha-arc" d="{path_from_points(alpha_arc_pts)}"/>')
A(f'    <text x="{alpha_label_pos[0]:.2f}" y="{alpha_label_pos[1]:.2f}" class="math">α</text>')
A(f'    <text x="{alpha_note_pos[0]:.2f}" y="{alpha_note_pos[1]:.2f}" class="note">α exaggerated for clarity</text>')
A('  </g>')
A('')
A('  <g id="velocity_arrows">')
for lane, a0, a1 in arrow_segments:
    A(f'    <path class="velocity" stroke="{lane["color"]}" marker-end="url(#arrowhead-{lane["id"]})" d="M {a0[0]:.2f},{a0[1]:.2f} L {a1[0]:.2f},{a1[1]:.2f}"/>')
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
A(f'    <path class="leader" d="M {shell_label[0] - 18:.2f},{shell_label[1] - 38:.2f} L {shell_anchor[0]:.2f},{shell_anchor[1]:.2f}"/>')
A(f'    <text x="{shell_label[0]:.2f}" y="{shell_label[1]:.2f}" class="label-small">')
A('      <tspan x="{0}" dy="0">prestressed membrane</tspan>'.format(f'{shell_label[0]:.2f}'))
A('      <tspan x="{0}" dy="26">guide shell</tspan>'.format(f'{shell_label[0]:.2f}'))
A('    </text>')
A('  </g>')
A('</svg>')

svg = '\n'.join(parts)
SVG_PATH.write_text(svg)

cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=str(PNG_PATH), output_width=W, output_height=H)
cairosvg.svg2pdf(bytestring=svg.encode('utf-8'), write_to=str(PDF_PATH), output_width=W, output_height=H)

print(SVG_PATH)
print(PNG_PATH)
print(PDF_PATH)
