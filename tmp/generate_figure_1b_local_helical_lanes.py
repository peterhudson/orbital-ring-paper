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
        'label_bias': (1.0, -0.9),
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
        'label_bias': (1.0, 1.1),
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
        'label_bias': (-1.0, -1.0),
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
        'label_bias': (-1.0, 0.9),
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



def fmt_points(points):
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in points)



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
        color = f'#{gray:02x}{gray+7:02x}{gray+14:02x}'
        quad = [project_model(p00)[:2], project_model(p10)[:2], project_model(p11)[:2], project_model(p01)[:2]]
        faces.append((avg_z, color, quad))
faces.sort(key=lambda item: item[0])

# Shell guide curves.
circ_curves = [PHI_MIN, 0.02, PHI_MAX]
long_curves = [0.15, 2.75]

# Centerline.
centerline_pts = [project_model(centerline(PHI_MIN + (PHI_MAX - PHI_MIN) * i / 260.0))[:2] for i in range(261)]

# Arrow and callout anchor helpers.
figure_center = (0.5 * W, 0.5 * H)


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



def screen_anchor(point, bias=(1.0, 0.0), distance=145.0):
    d = normalize2((point[0] - figure_center[0] + 0.55 * bias[0], point[1] - figure_center[1] + 0.55 * bias[1]))
    return add2(point, mul2(d, distance))


# Lane segments and annotations.
lane_geometry = {}
for lane in LANES:
    samples = helix_samples(lane)
    visible, hidden = split_segments(samples)
    lane_geometry[lane['id']] = {'visible': visible, 'hidden': hidden}

# Representative decomposition point on RH +v lane.
rep_lane = LANES[0]
rep_phi = -0.12
rep_theta = helix_theta(rep_phi, rep_lane)
rep_p = project_model(tube_point(rep_phi, rep_theta))[:2]
rep_s_vec = project_vector(s_hat(rep_phi))
rep_theta_vec = project_vector(theta_hat(rep_phi, rep_theta))
rep_helix_vec = project_vector(normalize(helix_tangent(rep_phi, rep_lane)))
rep_s_dir = normalize2(rep_s_vec[:2])
rep_theta_dir = normalize2(rep_theta_vec[:2])
rep_helix_dir = normalize2(rep_helix_vec[:2])

# Local vectors and angle arc for one helix.
comp_len_s = 128.0
comp_len_th = 86.0
comp_len_h = 122.0
u_s_end = add2(rep_p, mul2(rep_s_dir, comp_len_s))
u_th_end = add2(rep_p, mul2(rep_theta_dir, comp_len_th))
rep_h_end = add2(rep_p, mul2(rep_helix_dir, comp_len_h))

ang_s = math.atan2(rep_s_dir[1], rep_s_dir[0])
ang_h = math.atan2(rep_helix_dir[1], rep_helix_dir[0])
while ang_h < ang_s:
    ang_h += 2 * math.pi
if ang_h - ang_s > math.pi:
    ang_s, ang_h = ang_h, ang_s + 2 * math.pi
alpha_arc_pts = []
for i in range(26):
    t = i / 25.0
    a = ang_s + t * (ang_h - ang_s)
    alpha_arc_pts.append((rep_p[0] + 44.0 * math.cos(a), rep_p[1] + 44.0 * math.sin(a)))

# Unit-vector and guide-shell anchors.
phi_basis = -0.02
basis_center = project_model(centerline(phi_basis))[:2]
r_theta = 0.62
r_tip = project_model(tube_point(phi_basis, r_theta))[:2]

th_arc_pts = []
for i in range(22):
    theta = 0.70 + 0.75 * i / 21.0
    th_arc_pts.append(project_model(tube_point(phi_basis, theta))[:2])

shell_anchor = project_model(tube_point(0.18, 5.55))[:2]
shell_label = screen_anchor(shell_anchor, bias=(1.1, -0.2), distance=160.0)
centerline_anchor = project_model(centerline(-0.34))[:2]
centerline_label = screen_anchor(centerline_anchor, bias=(-1.0, -0.8), distance=128.0)

# Lane callout placements.
for lane in LANES:
    phi = lane['arrow_phi']
    point = project_model(helix_point(phi, lane))[:2]
    lane['callout_anchor'] = point
    lx, ly = screen_anchor(point, lane['label_bias'], distance=148.0)
    if lane['id'] == 'lh_plus':
        lx -= 132.0
        ly -= 22.0
    if lane['id'] == 'lh_minus':
        lx += 18.0
        ly += 32.0
    lx = max(96.0, min(W - 230.0, lx))
    ly = max(88.0, min(H - 42.0, ly))
    lane['callout_label'] = (lx, ly)

# Velocity arrows.
arrow_segments = []
for lane in LANES:
    phi = lane['arrow_phi']
    p0 = helix_point(phi, lane)
    tangent = normalize(helix_tangent(phi, lane))
    span = 0.22
    if lane['direction'] > 0:
        a0 = project_model(add(p0, mul(tangent, -0.38)))[:2]
        a1 = project_model(add(p0, mul(tangent, 0.38)))[:2]
        label_pos = add2(a1, mul2(normalize2(vector2(figure_center, a1)), 28.0))
        v_label = '+v'
    else:
        a0 = project_model(add(p0, mul(tangent, 0.38)))[:2]
        a1 = project_model(add(p0, mul(tangent, -0.38)))[:2]
        label_pos = add2(a1, mul2(normalize2(vector2(figure_center, a1)), 28.0))
        v_label = '-v'
    arrow_segments.append((lane, a0, a1, label_pos, v_label))


parts = []
A = parts.append
A('<?xml version="1.0" encoding="UTF-8"?>')
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
A('  <title id="title">Figure 1b local helical lanes on an inflated membrane guide shell</title>')
A('  <desc id="desc">Close view of a gently curved guide-shell tube segment with four helical lanes, local basis vectors, helix angle alpha, and representative tangential and azimuthal components.</desc>')
A('  <defs>')
A('    <marker id="arrowhead-dark" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#334155"/>')
A('    </marker>')
A('    <marker id="arrowhead-soft" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#64748b"/>')
A('    </marker>')
A('    <marker id="arrowhead-rh_plus" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#c0392b"/>')
A('    </marker>')
A('    <marker id="arrowhead-rh_minus" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#2e86ab"/>')
A('    </marker>')
A('    <marker id="arrowhead-lh_plus" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#2f9e44"/>')
A('    </marker>')
A('    <marker id="arrowhead-lh_minus" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">')
A('      <path d="M 0 0 L 12 6 L 0 12 z" fill="#b26b00"/>')
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
A('      .leader { fill: none; stroke: #94a3b8; stroke-width: 1.7; stroke-linecap: round; }')
A('      .lane-leader { fill: none; stroke-width: 1.9; stroke-linecap: round; }')
A('      .math { font-size: 30px; font-style: italic; }')
A('      .math-sub { font-size: 17px; font-style: italic; }')
A('      .math-caret { font-size: 18px; font-style: normal; }')
A('      .label { font-size: 28px; font-weight: 500; }')
A('      .label-small { font-size: 24px; font-weight: 500; }')
A('      .note { font-size: 21px; fill: #556270; }')
A('      .lane-text { font-size: 24px; font-weight: 600; }')
A('      .box { fill: #ffffff; opacity: 0.90; }')
A('      .decomp { fill: none; stroke: #1f2937; stroke-width: 2.2; stroke-linecap: round; marker-end: url(#arrowhead-dark); }')
A('      .alpha-arc { fill: none; stroke: #1f2937; stroke-width: 1.9; }')
A('      .velocity { fill: none; stroke-width: 2.6; stroke-linecap: round; }')
A('      .velocity-text { font-size: 22px; font-weight: 600; }')
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
A(f'    <path class="centerline" d="{path_from_points(centerline_pts)}"/>')
A(f'    <path class="basis" d="M {centerline_pts[120][0]:.2f},{centerline_pts[120][1]:.2f} L {centerline_pts[151][0]:.2f},{centerline_pts[151][1]:.2f}"/>')
A(f'    <text x="{centerline_pts[152][0] + 12:.2f}" y="{centerline_pts[152][1] - 10:.2f}" class="math">s</text>')
A(f'    <text x="{centerline_pts[152][0] + 28:.2f}" y="{centerline_pts[152][1] - 27:.2f}" class="math-caret">^</text>')
A(f'    <path class="leader" d="M {centerline_label[0]:.2f},{centerline_label[1] - 16:.2f} L {centerline_anchor[0]:.2f},{centerline_anchor[1]:.2f}"/>')
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
A(f'    <path class="basis" d="M {basis_center[0]:.2f},{basis_center[1]:.2f} L {r_tip[0]:.2f},{r_tip[1]:.2f}"/>')
A(f'    <text x="{r_tip[0] + 12:.2f}" y="{r_tip[1] - 8:.2f}" class="math">r</text>')
A(f'    <text x="{r_tip[0] + 28:.2f}" y="{r_tip[1] - 24:.2f}" class="math-caret">^</text>')
A(f'    <path class="basis-soft" d="{path_from_points(th_arc_pts)}"/>')
A(f'    <text x="{th_arc_pts[-1][0] + 16:.2f}" y="{th_arc_pts[-1][1] + 4:.2f}" class="math">θ</text>')
A(f'    <text x="{th_arc_pts[-1][0] + 33:.2f}" y="{th_arc_pts[-1][1] - 12:.2f}" class="math-caret">^</text>')
A('  </g>')
A('')
A('  <g id="decomposition">')
A(f'    <path class="decomp" d="M {rep_p[0]:.2f},{rep_p[1]:.2f} L {u_s_end[0]:.2f},{u_s_end[1]:.2f}"/>')
A(f'    <path class="decomp" d="M {rep_p[0]:.2f},{rep_p[1]:.2f} L {u_th_end[0]:.2f},{u_th_end[1]:.2f}"/>')
A(f'    <path class="alpha-arc" d="{path_from_points(alpha_arc_pts)}"/>')
A(f'    <text x="{u_s_end[0] + 12:.2f}" y="{u_s_end[1] - 12:.2f}" class="label-small">u</text>')
A(f'    <text x="{u_s_end[0] + 27:.2f}" y="{u_s_end[1] - 1:.2f}" class="math-sub">tangential</text>')
A(f'    <text x="{u_th_end[0] + 16:.2f}" y="{u_th_end[1] + 6:.2f}" class="label-small">u</text>')
A(f'    <text x="{u_th_end[0] + 31:.2f}" y="{u_th_end[1] + 17:.2f}" class="math-sub">azimuthal</text>')
A(f'    <text x="{rep_p[0] + 34:.2f}" y="{rep_p[1] - 46:.2f}" class="math">α</text>')
A(f'    <text x="{rep_p[0] + 132:.2f}" y="{rep_p[1] - 86:.2f}" class="note">α exaggerated for clarity</text>')
A('  </g>')
A('')
A('  <g id="velocity_arrows">')
for lane, a0, a1, label_pos, v_label in arrow_segments:
    A(f'    <path class="velocity" stroke="{lane["color"]}" marker-end="url(#arrowhead-{lane["id"]})" d="M {a0[0]:.2f},{a0[1]:.2f} L {a1[0]:.2f},{a1[1]:.2f}"/>')
    A(f'    <text x="{label_pos[0]:.2f}" y="{label_pos[1]:.2f}" class="velocity-text" fill="{lane["color"]}">{v_label}</text>')
A('  </g>')
A('')
A('  <g id="callouts">')
A(f'    <path class="leader" d="M {shell_label[0]:.2f},{shell_label[1] - 24:.2f} L {shell_anchor[0]:.2f},{shell_anchor[1]:.2f}"/>')
A(f'    <text x="{shell_label[0]:.2f}" y="{shell_label[1]:.2f}" class="label-small">')
A('      <tspan x="{0}" dy="0">inflated membrane</tspan>'.format(f'{shell_label[0]:.2f}'))
A('      <tspan x="{0}" dy="26">guide shell</tspan>'.format(f'{shell_label[0]:.2f}'))
A('    </text>')
for lane in LANES:
    ax, ay = lane['callout_anchor']
    lx, ly = lane['callout_label']
    A(f'    <path class="lane-leader" stroke="{lane["color"]}" d="M {lx:.2f},{ly - 14:.2f} L {ax:.2f},{ay:.2f}"/>')
    A(f'    <text x="{lx:.2f}" y="{ly:.2f}" class="lane-text" fill="{lane["color"]}">{lane["label"]}</text>')
A('  </g>')
A('</svg>')

svg = '\n'.join(parts)
SVG_PATH.write_text(svg)

cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=str(PNG_PATH), output_width=W, output_height=H)
cairosvg.svg2pdf(bytestring=svg.encode('utf-8'), write_to=str(PDF_PATH), output_width=W, output_height=H)

print(SVG_PATH)
print(PNG_PATH)
print(PDF_PATH)
