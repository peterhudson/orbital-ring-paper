# Stage 1A Addendum: Helical Rotor Inflation Model for a Fabric Tube

## Purpose
This addendum applies the corrected Stage 1 momentum-flux framing to the specific geometry Hudson described:

- a large fabric tube
- many coaxial rotor/stator members running in helical paths on or near the inner wall
- rotors moving fast enough that their required guide force generates an outward radial load on the tube

The goal is a first-pass expression for equivalent inflation pressure.

## 1. Geometry of one helix
Consider a circular helix wrapped on a cylinder of radius a.
Parameterize by angle θ:

r(θ) = (a cos θ, a sin θ, b θ)

where:
- a = tube radius
- b = axial advance per radian
- pitch per turn p = 2π b

The helix has:
- arc-length increment ds = sqrt(a^2 + b^2) dθ
- curvature

κ = a / (a^2 + b^2)

If α is the helix angle measured relative to the tube axis, then

sin α = a / sqrt(a^2 + b^2)
cos α = b / sqrt(a^2 + b^2)
tan α = a / b

and therefore

κ = sin^2 α / a

This is the cleanest form for later use.

## 2. Outward radial force from one rotor
From Stage 1, a rotor with linear mass density μ moving at speed v along a path of curvature κ requires guide force per unit rotor length

f_n = μ v^2 κ

For a helix on a cylinder, the principal normal points radially inward toward the axis.
Therefore the rotor pushes inward on itself via the guide field, and the stator feels equal outward radial reaction.
So the outward radial load on the housing from one rotor is

f_r = μ v^2 κ = μ v^2 sin^2 α / a

per unit rotor length.

This is the basic inflation-force result.

## 3. Convert rotor-length load to axial-length load
One meter of tube height contains more than one meter of rotor when the rotor is helical.
The amount of rotor length per unit axial length is

ds / dz = sec α = 1 / cos α

So the outward radial force per unit axial height from one helix is

q_r^(1) = f_r sec α
        = μ v^2 κ sec α
        = μ v^2 sin^2 α / (a cos α)

Units: N per meter of tube height.

## 4. N identical helices uniformly distributed
If there are N identical helices distributed approximately uniformly around the circumference, the total outward radial load per unit axial height is

q_r^(N) = N μ v^2 sin^2 α / (a cos α)

Spread over the cylindrical wall area per unit axial height, 2π a, the equivalent average inflation pressure is

p_eq = q_r^(N) / (2π a)

so

p_eq = N μ v^2 sin^2 α / (2π a^2 cos α)

This is the first-pass pressure formula for the helical inflation concept.

## 5. Same result in pitch form
Using b = p / (2π), we can also write

p_eq = N μ v^2 / (2π) * 1 / (b sqrt(a^2 + b^2))

or equivalently

p_eq = N μ v^2 / (p sqrt(1 + (2π a / p)^2))

The angle form is usually easier to interpret physically.

## 6. Hoop load in the fabric tube
For a thin cylindrical membrane under internal pressure p_eq, the hoop membrane force per unit axial length is

N_hoop = p_eq a

Therefore

N_hoop = N μ v^2 sin^2 α / (2π a cos α)

This is the circumferential tension the fabric system must carry on average.

## 7. First numerical example
Take:
- tube diameter = 100 m -> a = 50 m
- tube length = 1000 m
- number of helices N = 300
- rotor density μ = 1 kg/m per helix
- rotor speed v = 1000 m/s
- helix angle α = 45°

Then:
- sin^2 α = 0.5
- cos α ≈ 0.707
- f_r = μ v^2 sin^2 α / a = 1 * 10^6 * 0.5 / 50 = 10,000 N/m of rotor
- q_r^(1) = f_r sec α ≈ 14,142 N/m of tube height per helix
- q_r^(N) ≈ 4.24 MN/m
- p_eq = q_r^(N) / (2π a) ≈ 13.5 kPa

That is about 0.135 atmospheres of equivalent average pressure.

This is a serious number.
It is enough to make the concept interesting, though not enough by itself to guarantee architectural stiffness.

## 8. Scaling laws worth keeping
From

p_eq = N μ v^2 sin^2 α / (2π a^2 cos α)

we get:
- pressure scales linearly with number of helices N
- pressure scales linearly with rotor mass density μ
- pressure scales as v^2
- pressure scales roughly as 1 / a^2 at fixed helix angle
- pressure increases strongly with steeper helix angle α

That last point is important.
A shallow helix does little radial work because its curvature is low.
A steeper helix produces more radial reaction, but also requires more rotor length per meter of tube height.

## 9. Important comparison caveat
The formula above assumes N and μ are specified per rotor length.
That means steeper helices pack more rotor mass into a given tube height.
So of course the pressure rises as α increases.

If instead total rotor mass per unit tube height is fixed, define

m_z = N μ sec α

Then

p_eq = m_z v^2 κ / (2π a)
     = m_z v^2 sin^2 α / (2π a^2)

This is a better expression for fair design comparisons across different helix angles.

It shows:
- at fixed rotor mass per tube height, pressure still improves with helix angle
- but the divergence as cos α -> 0 disappears
- the real limit is then set by architecture, end turns, manufacturability, and controllability

## 10. What this model omits
This is only an average-load model. It omits:
- end effects
- discrete attachment spacing to the fabric or truss
- local shell wrinkling
- nonuniform helix spacing
- cross-coupling between clockwise and counterclockwise families
- dynamic wobble of the tube
- local guide saturation
- stator self-weight and hardware mass
- global buckling / sway / ovalization modes

So this is not yet a structural design.
It is only a first pressure estimate.

## 11. Immediate design interpretation
The helical concept passes a useful first test:

A network of fast helical rotors can, in principle, generate a real average outward pressure on a large cylindrical membrane or shell.

That means the phrase "inflation" is not just metaphorical.
It corresponds to an actual equivalent pressure field.

But the next problem is obvious:
- average pressure is not enough
- the tube must also resist sway, bending, ovalization, and local perturbations
- the stator loads must be transferred into a shell or truss without creating impossible local concentrations
- the control system must keep the guide loads smooth enough that the tube does not excite itself

## 12. Bottom line
For N helices on a tube of radius a, the first-pass equivalent pressure is

p_eq = N μ v^2 sin^2 α / (2π a^2 cos α)

This is a useful result.
It converts the concept from vague intuition into a design equation.

My current judgment is:
- the helical inflation idea is physically credible at first pass
- the pressure scales are large enough to be interesting
- the real next gates are dynamic stability, shell coupling, local load transfer, and failure containment
