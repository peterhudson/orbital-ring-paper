# Stage 1 Physics Memo: Single Coaxial Active-Support Member

## Status
First-pass analytic memo.
This is a screening model, not a final design.
Its job is to reveal scaling laws, hard limits, and likely failure bottlenecks early.

## Executive summary
The core physics is encouraging in one narrow sense:

A fast moving internal rotor behaves like a cable with an effective tension

T_eff = μ v^2

where:
- μ = rotor mass per unit length (kg/m)
- v = rotor speed (m/s)

If the stator forces that rotor to follow a curved path with curvature κ = 1 / R, the reaction force transferred to the stator is

f_support = T_eff κ = μ v^2 κ = μ v^2 / R

where f_support is force per unit length.

That means the concept has a real mechanism for generating structural support force.
It is not nonsense.

But the same equations immediately reveal the central problem:

The support force comes bundled with enormous stored kinetic energy.

Energy per unit length is

e_k = (1/2) μ v^2 = T_eff / 2

So every increase in effective support tension also increases hazard.

This concept is therefore not primarily limited by whether it can make force.
It is limited by whether it can do so with survivable materials, magnetic force density, acceptable losses, and graceful failure handling.

## 1. Idealized model
We model one active-support member as:
- a continuous rotor moving at constant speed v
- rotor linear density μ
- a stator that constrains the rotor to a prescribed centerline
- magnetic coupling that provides levitation, guidance, and force transfer
- no mechanical contact in nominal operation

For the first-pass model, we ignore:
- local bending stiffness of the rotor
- gap variation around the circumference
- end effects
- detailed motor topology
- control latency
- aerodynamic detail

Those matter later. Right now we want the governing scaling laws.

## 2. Momentum-flux force scale of the moving rotor
Take a small element of rotor moving along a curved centerline.
The rate of momentum change required to turn that moving mass is

ΔF = μ v^2 κ

per unit length.

So the distributed guide force required to bend the rotor path is

f_guide = μ v^2 κ = μ v^2 / R

This is the first-order force law that matters most for the concept.
It says a fast-moving rotor really can push on the stator when the stator forces it to follow a curved path.

This is best understood as momentum redirection, not as ordinary structural preload.
The rotor wants to continue in a straight line.
The stator, via magnetic levitation and guidance, forces it onto a curved path.
The rotor pushes back on the stator with equal and opposite force.

## 3. Equivalent tension model, and why it is only an equivalence
For a continuous flexible rotor, the same curved-path force balance can be written in the same form as a tensioned string.
That leads to an equivalent dynamic tension scale

T_eq = μ v^2

because a tensioned string under curvature κ gives a transverse load per length of

f = T κ

Matching that to the momentum-flux result gives T_eq = μ v^2.

This equivalence is useful, but it must not be over-read.
T_eq is not automatically the literal material tension carried by the rotor.
It is the equivalent line-force scale associated with turning the moving mass stream.

That distinction matters:
- If the rotor is a train of slugs or carriages, T_eq is clearly not literal cable tension.
- If the rotor is a continuous cable but is continuously guided by distributed magnetic forces, T_eq is still primarily a momentum-flux equivalence, not automatically an axial material stress.
- T_eq becomes literal tensile force only in special cases where the curvature load is actually carried internally as end-to-end cable tension.

So for this program, the safest primary intuition is:

moving mass stream + imposed curvature -> guide force on rotor -> equal and opposite reaction on stator

## 4. What actually sets rotor speed limits
The previous draft overstated this section by treating T_eq as if it were always literal cable tension. That was too broad.

A rotor is not generically limited by

v_max ≈ sqrt(σ_allow / ρ)

just because it is moving quickly.
A moving guided mass stream can travel much faster than that without suffering an axial stress of ρ v^2.
That is exactly why concepts like orbital rings are not immediately ruled out by ordinary material specific strength.

For a continuously guided magnetically suspended rotor, the relevant first-order speed limits are instead likely to come from:
- required guide force density, f_guide = μ v^2 κ
- achievable magnetic pressure across practical gaps
- local bending and flexure limits if the rotor is a literal cable or belt
- end-turn geometry and any regions where the rotor must reverse direction tightly
- joints, splices, fatigue, creep, abrasion, and inspection limits
- loss mechanisms that scale badly with v, including drag, eddy currents, hysteresis, and internal damping
- control bandwidth, wave propagation, and dynamic stability
- failure containment and safe spin-down

A specific-strength ceiling of the form

v_max ≈ sqrt(σ_allow / ρ)

still matters in some special cases, for example:
- if the rotor is actually tension-dominated
- if unsupported spans force the rotor to carry its own curvature load internally
- if local geometry or end-turns induce true axial stress comparable to the momentum-turning load scale

But it is not a universal speed limit for the guided rotor concept.

Corrected takeaway:
The concept is not first ruled by material tensile stress from speed alone.
It is first ruled by whether the stator can guide and contain a high-speed momentum stream with acceptable force density, losses, dynamics, and failure behavior.

## 5. Support-force density examples
Use:
- μ = 10 kg/m
- case A: v = 1000 m/s
- case B: v = 1500 m/s

Then:
- case A: T_eff = 10 MN
- case B: T_eff = 22.5 MN

Now compute support force per unit length for several radii:

| Rotor case | Radius R | Curvature κ | f_support |
| --- | ---: | ---: | ---: |
| 10 kg/m at 1000 m/s | 1000 m | 0.001 1/m | 10 kN/m |
| 10 kg/m at 1000 m/s | 100 m | 0.01 1/m | 100 kN/m |
| 10 kg/m at 1500 m/s | 1000 m | 0.001 1/m | 22.5 kN/m |
| 10 kg/m at 1500 m/s | 100 m | 0.01 1/m | 225 kN/m |

So yes, substantial force per meter is available in principle.
But notice what is happening: the attractive force numbers only appear once the rotor is carrying very large effective tension and very large kinetic energy.

## 6. Stored energy and why this is scary
Rotor kinetic energy per unit length is

e_k = (1/2) μ v^2

For the same cases above:
- 10 kg/m at 1000 m/s -> 5 MJ/m
- 10 kg/m at 1500 m/s -> 11.25 MJ/m

That means a 100 m active member stores roughly:
- 500 MJ in case A
- 1125 MJ in case B

Equivalent TNT scale is roughly:
- 500 MJ ≈ 0.12 tons TNT
- 1125 MJ ≈ 0.27 tons TNT

A 1000 m member would be about ten times worse.

That does not mean every failure releases all energy instantaneously.
But it does mean the rotor must be treated more like energetic infrastructure than like ordinary structural steel.

## 7. Magnetic force-transfer requirement
The stator must provide enough magnetic force density to:
- levitate the rotor against static offsets
- steer it onto the desired path
- reject disturbances
- maintain gap control

The curvature-related steering load per unit length is

f_mag,req >= μ v^2 / R

If that load is spread over effective magnetic interface area per unit length a_int, the required magnetic stress is

p_req ≈ f_mag,req / a_int

A rough upper bound for magnetic normal stress is on the order of

p_mag,max ≈ B^2 / (2 μ0)

Numerically:
- at B = 1 T, p_mag,max ≈ 0.40 MPa
- at B = 2 T, p_mag,max ≈ 1.59 MPa
- at B = 5 T, p_mag,max ≈ 9.95 MPa

Those are idealized field-pressure numbers, not whole-system design values.
Real systems pay penalties for gap, geometry, copper loss, eddy currents, cryogenics if superconducting, and dynamic control.

Still, this gives a useful first test:
If the required steering stress approaches multi-megapascal range across practical gaps, the maglev architecture becomes very demanding very fast.

## 8. Power and loss scaling
In the ideal model, a perfectly levitated rotor moving at constant speed in vacuum can circulate without continuous propulsion except to replace losses.
Real losses will include:
- aerodynamic drag if not operated in vacuum or near-vacuum
- eddy current loss in conductive structures
- hysteresis loss in magnetic materials
- inverter and motor losses
- active control loss
- flexural/internal damping loss in the rotor

If q_loss is the equivalent longitudinal loss force per unit length, the power draw is

P_loss = q_loss v L

where L is active rotor length.

This equation is painful because high rotor speed helps support performance, but also multiplies the cost of every residual drag term.

The architecture therefore strongly prefers:
- low-pressure internal environment
- low-loss magnetic topology
- minimal conductive parasitic structures near time-varying fields
- rotor materials that tolerate repeated high-speed circulation without large internal damping

## 9. What the member can and cannot do
### It can do
- generate real distributed transverse force through curvature reaction
- act like a dynamically tensioned internal support element
- potentially create outward pressure in helical or inflatable geometries

### It cannot do for free
- create arbitrary compressive support in a perfectly straight member
- ignore curvature geometry
- ignore containment and spin-down
- escape specific-strength limits
- escape dynamics by hand-waving to "maglev"

## 10. Immediate red flags
### Red flag 1: energy density
The rotor stores enough energy that failure engineering is not secondary. It is central.

### Red flag 2: material reality
The interesting operating regime probably pushes toward high-specific-strength fibers, but those are exactly the materials with awkward joining, wear, bend-fatigue, creep, and inspection problems.

### Red flag 3: magnetic steering stress
The magnetic system must do real structural work, not just delicate positioning. That may be achievable, but it is not cheap or trivial.

### Red flag 4: curvature-control coupling
The same geometry that creates support force also creates disturbance sensitivity. If the member shape wobbles, the required steering force changes dynamically.

### Red flag 5: scaling hazard
As the concept scales up, stored energy scales with length. A member that is merely dramatic at 10 m may be unacceptable at 1000 m unless segmented and energy-isolated.

## 11. Design implications already visible
1. Segmentation is probably mandatory.
   Very long continuous energetic loops look dangerous.

2. Low-pressure operation is probably mandatory.
   Atmospheric drag at high speed will be punishing.

3. Rotor material selection is a first-order program decision.
   Specific strength dominates the ceiling.

4. Geometry must be designed together with control.
   The structural form and the actuator problem are the same problem.

5. Passive fault tolerance must exist outside the rotor.
   A system that instantly becomes nothing when the rotor trips is too brittle for public deployment.

## 12. Most useful next equations to derive
Stage 2 should build from this memo and derive:
- linearized lateral dynamics of rotor within the stator
- magnetic actuator stiffness and damping limits
- disturbance rejection bandwidth requirements
- segmented-isolation energy release model
- first structural-mode coupling for a helical bundle or inflated shell

## 13. Bottom line
The single-member concept is physically real in the sense that it has a valid support-force mechanism:

moving rotor -> effective tension -> curvature reaction -> distributed support force

So the concept survives the first smell test.

But it survives in a dangerous way.
It buys structural force by carrying large momentum and large stored kinetic energy.

My current judgment is:
- the concept is promising enough to justify serious work
- the real bottlenecks are likely containment, control, and failure management more than raw force production
- the next step should be a Stage 2 dynamics memo plus a more explicit force-density check for specific magnetic topologies
