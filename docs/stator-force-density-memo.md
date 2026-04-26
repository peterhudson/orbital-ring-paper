# Stator Force-Density Memo

## Status
First-pass force-density memo for the coaxial stator / rotor interface.
This memo asks a narrower question than the previous ones:

Given the required guide force density from the moving rotor, what magnetic interface area and field pressure are implied, and when do those requirements become implactical?

## 1. Starting point from Stage 1
For a rotor with linear mass density μ moving at speed v through a path of curvature κ = 1/R, the required guide force per unit rotor length is

f_guide = μ v^2 κ = μ v^2 / R

This is the load the stator must transmit magnetically if nominal operation is contactless.

## 2. From line force to interface stress
Let A' be the effective magnetic interface area per unit rotor length, with units m^2 per m = m.
For a cylindrical coaxial interface of effective active perimeter P_eff, we have approximately

A' ≈ P_eff

because one meter of length contributes roughly P_eff square meters of interacting area.

Then the average magnetic traction required is

p_req = f_guide / A' = μ v^2 / (R A')

This is the average pressure scale the stator must support.

## 3. Geometric interpretation for a coaxial stator
Suppose the active magnetic interaction occupies an effective circumference

P_eff = η 2π r

where:
- r is characteristic rotor radius
- η is the fraction of circumference that contributes usefully to guidance

Then

p_req = μ v^2 / (R η 2π r)

This equation is very useful because it connects the architecture directly to force density.

Larger rotor radius helps by giving more interface area.
So does larger active coverage η.
But both fight mass, packaging, and cost.

## 4. Magnetic pressure limits
A very rough upper bound for magnetic normal stress in a gap is

p_mag,max ≈ B^2 / (2 μ0)

with μ0 = 4π × 10^-7 H/m.

Useful reference values:
- B = 0.5 T -> p_mag,max ≈ 0.10 MPa
- B = 1 T -> p_mag,max ≈ 0.40 MPa
- B = 2 T -> p_mag,max ≈ 1.59 MPa
- B = 3 T -> p_mag,max ≈ 3.58 MPa
- B = 5 T -> p_mag,max ≈ 9.95 MPa

These are ideal field-pressure numbers, not delivered whole-system engineering values.
Real systems will be worse because of:
- finite gap
- fringing fields
- alternating or dynamic loading
- thermal limits in coils
- mechanical packaging
- eddy-current losses
- the fact that some field authority must be reserved for stabilization, not just average load support

## 5. A usable design inequality
To first order, feasible guide operation requires

p_req << p_mag,max

or

μ v^2 / (R η 2π r) << B^2 / (2 μ0)

Rearranging gives a curvature bound

1/R << (B^2 η 2π r) / (2 μ0 μ v^2)

or a radius-of-curvature bound

R >> (2 μ0 μ v^2) / (B^2 η 2π r)

Interpretation:
- larger v and larger μ make the required curvature harder to support
- larger rotor radius helps
- stronger field helps quadratically
- larger active circumference helps linearly

This is one of the first really useful architecture filters.

## 6. Numerical examples
Take a notional coaxial member with:
- μ = 1 kg/m
- v = 1000 m/s
- r = 0.10 m
- η = 0.5

Then
- μ v^2 = 1.0 MN
- A' ≈ η 2π r ≈ 0.314 m^2/m

Now compute required average traction:

### Case A: R = 1000 m
f_guide = 1000 N/m
p_req ≈ 3.18 kPa

### Case B: R = 100 m
f_guide = 10,000 N/m
p_req ≈ 31.8 kPa

### Case C: R = 10 m
f_guide = 100,000 N/m
p_req ≈ 318 kPa = 0.318 MPa

These are surprisingly manageable from a pure average-stress standpoint.
Even Case C is below the ideal 1 T pressure scale.

But note what this means: average traction may not be the main bottleneck in gentle-curvature segments.
The harder issues may be dynamic authority, losses, and saturation margin.

## 7. Higher-energy example
Now take a more aggressive member:
- μ = 5 kg/m
- v = 1500 m/s
- r = 0.10 m
- η = 0.5

Then
- μ v^2 = 11.25 MN
- A' ≈ 0.314 m^2/m

### Case D: R = 1000 m
f_guide = 11.25 kN/m
p_req ≈ 35.8 kPa

### Case E: R = 100 m
f_guide = 112.5 kN/m
p_req ≈ 358 kPa = 0.358 MPa

### Case F: R = 10 m
f_guide = 1.125 MN/m
p_req ≈ 3.58 MPa

Now the picture changes.
At very tight curvature, the average magnetic traction starts entering the multi-megapascal regime.
That is not obviously impossible, but it is no longer comfortable.

## 8. Dynamic margin matters more than average load
The dangerous mistake would be to compare p_req to p_mag,max and conclude that the interface is fine.
In reality the guide system needs margin for:
- dynamic centering
- disturbance rejection
- local geometry error
- misalignment
- vibration suppression
- control transients
- local overloads due to segment-to-segment imperfections

So the useful quantity is not merely

p_req / p_mag,max

but a margin ratio such as

M_p = p_req / p_avail

where p_avail is the field traction that remains after thermal, control, and gap penalties.

A serious design probably wants M_p well below 1, not near it.
Something like 0.1 to 0.3 in the critical operating envelope would feel much healthier than 0.8.

## 9. Gap scaling and why it hurts
The ideal field-pressure formula hides the fact that practical force drops rapidly with gap and with poorly shaped return paths.

Consequences:
- large stator clearance for safety and fault tolerance fights force density
- tight gap helps force density but reduces allowable runout and manufacturing tolerance
- dynamic wobble directly attacks magnetic authority by modulating gap

This means the actual design variable is not just field strength B.
It is field strength at the required working gap with acceptable heat and stability.

## 10. Implications for rotor topology
### Continuous cable / belt
Pros:
- smooth load distribution
- potentially high interface area

Cons:
- local runout, splice geometry, and flexural vibration may force larger gaps than desired

### Discrete carriages / slugs
Pros:
- easier segmentation and containment
- easier local replacement

Cons:
- interface becomes spatially intermittent
- peak local force per carriage can exceed the average-pressure estimates badly
- force ripple may couple into shell modes

### Magnetically linked segmented train
This may be the most promising compromise, but only if linkage suppresses force ripple without creating giant local end loads.

## 11. Helical tube implication
For the helical tube concept, the average radial pressure estimate from the previous memo may look encouraging, but the stator interface must actually deliver that load continuously all along the helix.

That means the helical tube concept inherits a local design condition:

μ v^2 κ / A' must remain comfortably below practical magnetic traction capacity.

Large tube radius a helps because helix curvature decreases roughly as sin^2(α)/a.
That is good.
But if the architecture tries to extract too much pressure by pushing to high μ, high v, or steep helices, the local guide interface may become the first failing layer.

## 12. Most useful first-pass screening metric
A useful dimensionless screening parameter is

Π_p = μ v^2 / (R A' p_avail)

Interpretation:
- Π_p << 1 means local magnetic force density is comfortable
- Π_p ~ 1 means the guide interface is near its average traction limit
- Π_p > 1 means the concept is not viable without changing geometry, area, speed, or field capability

This is a much better local metric than talking about rotor speed alone.

## 13. Bottom line
The early result is actually encouraging in one specific way:

For large-radius structures and modest rotor mass density, average required magnetic traction may be quite manageable.

That means the force-density problem may not kill the concept immediately.

But the harder truth is:
- tight-curvature regions are expensive in magnetic traction
- dynamic margin matters more than average traction
- working gap and thermal limits probably dominate practical designs
- end turns and local defects may be much harder than the gentle main spans

My current judgment is:
- main-span stator force density is probably not the first showstopper for large-radius helical structures
- tight-radius features, transients, and disturbance margin are much more dangerous
- the next worthwhile step is a reduced-order model combining gap, actuator bandwidth, and available magnetic traction under realistic disturbance amplitudes
