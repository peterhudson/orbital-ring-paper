from pathlib import Path
import math
import cairosvg

OUT_DIR = Path('/data/.openclaw/workspace/figures')
SVG_PATH = OUT_DIR / 'figure-1a-orbital-ring-global-geometry.svg'
PNG_PATH = OUT_DIR / 'figure-1a-orbital-ring-global-geometry.png'
PDF_PATH = OUT_DIR / 'figure-1a-orbital-ring-global-geometry.pdf'

W, H = 1200, 900
cx, cy = 600.0, 450.0

earth_r = 280.0
ring_r = earth_r * (6871.0 / 6371.0)
tilt_deg = 72.5
screen_rot_deg = 12.0


def screen_rotate(x, y, deg):
    a = math.radians(deg)
    xr = x * math.cos(a) - y * math.sin(a)
    yr = x * math.sin(a) + y * math.cos(a)
    return xr, yr


def ring_point(t_deg):
    t = math.radians(t_deg)
    x0 = ring_r * math.cos(t)
    y0 = ring_r * math.sin(t) * math.cos(math.radians(tilt_deg))
    z0 = ring_r * math.sin(t) * math.sin(math.radians(tilt_deg))
    x1, y1 = screen_rotate(x0, y0, screen_rot_deg)
    return cx + x1, cy - y1, x1, y1, z0


def path_from_points(points):
    if not points:
        return ''
    return 'M ' + ' L '.join(f'{x:.2f},{y:.2f}' for x, y in points)


def split_segments(samples):
    visible = []
    hidden = []
    current = [samples[0][:2]]
    current_hidden = samples[0][2]
    for i in range(1, len(samples)):
        x0, y0, h0 = samples[i - 1]
        x1, y1, h1 = samples[i]
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


samples = []
for i in range(721):
    t_deg = i * 360.0 / 720.0
    sx, sy, x1, y1, z0 = ring_point(t_deg)
    hidden = (z0 > 0.0) and (x1 * x1 + y1 * y1 <= earth_r * earth_r)
    samples.append((sx, sy, hidden, t_deg))

visible_segments, hidden_segments = split_segments([(x, y, h) for x, y, h, _ in samples])

# Highlight a front-visible sector on the lower-right front side.
local_sector = []
for x, y, hidden, t_deg in samples:
    if 302.0 <= t_deg <= 326.0 and not hidden:
        local_sector.append((x, y))

# Radius line to the rightmost major-axis point.
rx, ry, _, _, _ = ring_point(0.0)
r_mid_x = cx + 0.58 * (rx - cx)
r_mid_y = cy + 0.58 * (ry - cy) - 6

# Earth rotation axis, projected from the ring plane normal.
# Before screen rotation, axis projection is vertical; after rotation it rotates with the drawing.
ax_dir_x, ax_dir_y = screen_rotate(0.0, 1.0, screen_rot_deg)
axis_len = earth_r + 95.0
axis_top_x = cx - axis_len * ax_dir_x
axis_top_y = cy + axis_len * ax_dir_y
axis_bot_x = cx + axis_len * ax_dir_x
axis_bot_y = cy - axis_len * ax_dir_y
axis_label_x = 420
axis_label_y = 800

# Label anchor points.
local_anchor_x, local_anchor_y, _, _, _ = ring_point(312.0)
local_label_x, local_label_y = 900, 655

parts = []
A = parts.append
A('<?xml version="1.0" encoding="UTF-8"?>')
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
A('  <title id="title">Figure 1a orbital ring global geometry</title>')
A('  <desc id="desc">Earth shown from the side with an equatorial orbital ring rendered as a slightly tilted hoop. The visible front portion is solid, the part occluded by Earth is dashed, and labels mark Earth, the Earth rotation axis, a local sector enlarged in Figure 1b, and the radius R.</desc>')
A('  <defs>')
A('    <style><![CDATA[')
A('      text { font-family: Arial, Helvetica, sans-serif; fill: #1f2937; }')
A('      .earth-fill { fill: #dfe7f0; }')
A('      .earth-stroke { fill: none; stroke: #475569; stroke-width: 3.0; }')
A('      .ring-visible { fill: none; stroke: #4b5563; stroke-width: 3.8; stroke-linecap: round; stroke-linejoin: round; }')
A('      .ring-hidden { fill: none; stroke: #98a2b3; stroke-width: 3.0; stroke-dasharray: 10 10; stroke-linecap: round; stroke-linejoin: round; }')
A('      .sector { fill: none; stroke: #c64e35; stroke-width: 6.8; stroke-linecap: round; }')
A('      .radius { fill: none; stroke: #374151; stroke-width: 2.6; }')
A('      .axis { fill: none; stroke: #94a3b8; stroke-width: 2.2; stroke-dasharray: 7 8; }')
A('      .leader { fill: none; stroke: #9ca3af; stroke-width: 1.8; }')
A('      .earth-label { font-size: 30px; font-weight: 600; }')
A('      .label { font-size: 27px; font-weight: 500; }')
A('      .label-small { font-size: 24px; font-weight: 500; }')
A('      .math { font-size: 29px; font-style: italic; }')
A('      .label-box { fill: #ffffff; stroke: #e2e8f0; stroke-width: 0.9; opacity: 0.92; }')
A('      .center-dot { fill: #374151; }')
A('    ]]></style>')
A('  </defs>')
A(f'  <rect width="{W}" height="{H}" fill="#ffffff"/>')
A('')
A('  <g id="earth_rotation_axis">')
A(f'    <path d="M {axis_top_x:.2f},{axis_top_y:.2f} L {axis_bot_x:.2f},{axis_bot_y:.2f}" class="axis"/>')
A(f'    <text x="{axis_label_x:.2f}" y="{axis_label_y:.2f}" class="label">Earth rotation axis</text>')
A('  </g>')
A('')
A('  <g id="earth">')
A(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{earth_r:.2f}" class="earth-fill"/>')
A(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{earth_r:.2f}" class="earth-stroke"/>')
A(f'    <text x="{cx:.2f}" y="{cy - 28:.2f}" class="earth-label" text-anchor="middle">Earth</text>')
A('  </g>')
A('')
A('  <g id="ring_hidden">')
for seg in hidden_segments:
    if len(seg) >= 2:
        A(f'    <path d="{path_from_points(seg)}" class="ring-hidden"/>')
A('  </g>')
A('')
A('  <g id="ring_visible">')
for seg in visible_segments:
    if len(seg) >= 2:
        A(f'    <path d="{path_from_points(seg)}" class="ring-visible"/>')
A(f'    <path d="{path_from_points(local_sector)}" class="sector"/>')
A('  </g>')
A('')
A('  <g id="radius_dimension">')
A(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="4.5" class="center-dot"/>')
A(f'    <path d="M {cx:.2f},{cy:.2f} L {rx:.2f},{ry:.2f}" class="radius"/>')
A(f'    <text x="{r_mid_x:.2f}" y="{r_mid_y:.2f}" class="math" text-anchor="middle">R</text>')
A('  </g>')
A('')
A('  <g id="callouts">')
A(f'    <path d="M {local_label_x - 18:.2f},{local_label_y - 42:.2f} L {local_anchor_x + 8:.2f},{local_anchor_y + 2:.2f}" class="leader"/>')
A(f'    <text x="{local_label_x:.2f}" y="{local_label_y:.2f}" class="label-small">')
A(f'      <tspan x="{local_label_x:.2f}" dy="0">detail view</tspan>')
A(f'      <tspan x="{local_label_x:.2f}" dy="28">in Fig. 1b</tspan>')
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
