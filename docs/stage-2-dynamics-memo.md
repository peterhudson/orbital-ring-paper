# Stage 2 Dynamics Memo: Single Coaxial Active-Support Member

## Status
First-pass dynamics memo, written after correcting the Stage 1 momentum-flux framing.
The purpose of this memo is to derive a local equation of motion for one guided rotor, identify the main stability terms, and expose what the control system must actually do.

## 1. Scope and framing
We consider a single rotor moving through a stationary stator at constant mean speed v.

The Stage 1 result was:
- support comes from momentum redirection, not from assuming literal cable tension everywhere
- the force scale associated with turning the stream is μ v^2 κ

Stage 2 asks a different question:

When the rotor is slightly off its intended path, what equation governs that error, and what guide stiffness/damping/control authority are required to keep it bounded?

## 2. Coordinates and state variables
Let x be arclength-like coordinate along the nominal stator centerline.
Let y(x,t) be a small lateral displacement of the rotor relative to the nominal guide centerline in one transverse direction.

For now:
- small displacement, small slope linearization
- constant transport speed v
- one transverse direction only
- locally straight nominal guide segment for perturbation analysis

Later work should extend this to:
- two transverse directions
- curved nominal centerlines
- torsion / twist
- helical bundle coupling
- large disturbances and gap saturation

## 3. Material derivative and the key inertial term
Because the rotor is moving through the stator, the acceleration of rotor material is not just ∂^2 y / ∂t^2.
It is the material derivative along the moving stream:

D/Dt = ∂/∂t + v ∂/∂x

So the lateral acceleration of rotor material is

D^2 y / Dt^2 = y_tt + 2 v y_xt + v^2 y_xx

This is the central Stage 2 kinematic result.

Interpretation:
- y_tt is ordinary local acceleration
- 2 v y_xt is the convective cross-term
- v^2 y_xx is the curvature-following inertial term of the moving stream

That last term is the same basic physics that showed up in Stage 1.

## 4. Generic local equation of motion
Let μ be rotor mass per unit length.
Let the stator apply a distributed lateral guide force f_mag.
Let f_dist represent disturbances.
Then the one-dimensional transverse dynamics are

μ (y_tt + 2 v y_xt + v^2 y_xx) = f_mag + f_int + f_dist

where f_int represents any true internal rotor force terms, such as:
- actual axial tension, if present
- bending stiffness, if present
- internal damping, if present

This is intentionally general.
It covers both:
- a slug-stream interpretation, where f_int may be very small
- a continuous cable/belt interpretation, where f_int may matter

## 5. First linear magnetic-control model
For small displacement around the guide centerline, the stator guide force can be linearized as

f_mag ≈ -k_m y - c_m y_t + f_act

where:
- k_m is passive or bias magnetic stiffness per unit length (N/m^2 in this distributed 1D form)
- c_m is local damping coefficient per unit length (N·s/m^2)
- f_act is additional actively commanded force density from feedback control

If we ignore for the moment true internal rotor forces, the simplest closed-loop model becomes

μ (y_tt + 2 v y_xt + v^2 y_xx) + c_m y_t + k_m y = f_act + f_dist

This is the minimum useful Stage 2 equation.

## 6. Optional internal-force terms
If the rotor has actual material tension T_mat and bending stiffness EI, then a more general model is

μ (y_tt + 2 v y_xt + v^2 y_xx) + c_m y_t + k_m y - T_mat y_xx + EI y_xxxx = f_act + f_dist

Notes:
- The sign convention above is chosen so positive T_mat and EI are stabilizing.
- If the rotor is not tension-dominated, T_mat may be small or even negligible compared with guide-force terms.
- If the rotor is a bead/slab/train topology rather than a continuous cable, EI and T_mat should be replaced with the correct discrete or homogenized coupling terms.

This is why Stage 2 must not assume a single rotor topology too early.

## 7. Dispersion relation and modal interpretation
Assume a local harmonic perturbation

y ~ exp(i(kx - ωt))

and ignore f_dist.
For the simplest model with no f_act, no T_mat, and no EI, substitution gives

-μ (ω - v k)^2 - i c_m ω + k_m = 0

or equivalently

μ (ω - v k)^2 + i c_m ω - k_m = 0

Written in the more useful force-balance form:

μ (ω - v k)^2 = k_m + i c_m ω

Interpretation:
- disturbances are seen in the moving frame through the shifted frequency (ω - v k)
- transport speed couples spatial wavelength directly into apparent excitation frequency
- shorter wavelength disturbances are harder because v k rises rapidly

If T_mat and EI are included, the relation becomes

μ (ω - v k)^2 = k_m + T_mat k^2 + EI k^4 + i c_m ω

This is the most useful local scaling law in the memo.

## 8. Immediate control consequence: bandwidth scales with transport speed
If the guide sees disturbance wavelength λ, then k = 2π / λ and the characteristic convective frequency scale is

ω_conv ≈ v k = 2π v / λ

So the control system must react on a timescale shorter than roughly

t_conv ≈ λ / v

Examples:
- v = 1000 m/s, λ = 10 m -> t_conv ≈ 10 ms
- v = 1000 m/s, λ = 1 m -> t_conv ≈ 1 ms
- v = 3000 m/s, λ = 1 m -> t_conv ≈ 0.33 ms

That is a hard result.
High rotor speed does not just raise force scale. It also pushes disturbance rejection into brutally fast sensing, actuation, and computation regimes.

## 9. Gap, stiffness, and acceleration requirements
If allowable lateral gap is g and we require disturbance displacement |y| to stay well below g, the guide system must supply enough acceleration to correct deviations before the rotor reaches the wall.

A simple local estimate is

a_corr ≈ (k_eff / μ) y

where k_eff includes passive plus active closed-loop stiffness.

To arrest an error of order y over a convective time t_conv, we need roughly

a_req ~ y / t_conv^2 ~ y v^2 / λ^2

Therefore the corresponding required guide force density scales as

f_req ~ μ y v^2 / λ^2

This is only a back-of-envelope scaling law, but it is useful because it shows why short-length disturbances are vicious:

required corrective force rises with v^2 and with 1 / λ^2.

## 10. Stability risks visible already
### Risk 1: Convective underdamping
If damping is weak, disturbances are transported faster than they can be removed. The rotor may remain nominally centered on average while still developing dangerous local excursions.

### Risk 2: Gap saturation
Linear guide-force models fail once the rotor approaches stator walls or actuator saturation. Real systems then become strongly nonlinear exactly when they most need margin.

### Risk 3: Delay instability
Sensor delay, computation delay, power-electronics delay, and magnetic-field build-up delay all eat directly into the convective timescale.

### Risk 4: Local-to-global coupling
A local rotor displacement changes guide force, which changes housing load, which can move the housing itself, which feeds back into rotor error. In a tall active structure, this coupling may dominate.

### Risk 5: Wrong topology assumptions
A continuous cable, segmented belt, or stream of discrete magnetic slugs do not have identical dynamics. Choosing the wrong homogenized model too early can produce fake confidence.

## 11. Most likely useful control architecture
My current view is that the control system will probably need three layers:

1. Fast local gap control
   - kHz-class sensing/actuation regime
   - keeps rotor centered inside each guide segment

2. Intermediate segment control
   - coordinates guide segments over several meters to tens of meters
   - suppresses traveling disturbances and manages force sharing

3. Slow structural control
   - manages the motion of the housing / fabric / truss itself
   - handles wind, sway, and low-frequency global modes

Trying to solve everything in one centralized loop is probably a mistake.

## 12. What the equation says about design choices
### A. Higher rotor speed is a mixed blessing
Higher v increases available support force, but it also:
- raises kinetic energy as v^2
- raises guide-force demand as v^2
- raises disturbance rejection speed as v / λ
- makes actuator delay less tolerable

### B. Short disturbance wavelengths are dangerous
Manufacturing tolerances, splice imperfections, guide misalignment, and local shell motion all create short λ disturbances, which are disproportionately hard to control.

### C. Segmentation is more than a safety feature
Segmentation may also be necessary for controllability.
Shorter independently managed sections can reduce disturbance propagation and keep control bandwidth realistic.

### D. The housing cannot be treated as rigid forever
For architectural structures, the housing and support envelope will move. Stage 3 must explicitly include stator motion and structural-mode coupling.

## 13. Minimum nondimensional groups to track
The following dimensionless ratios look useful for the next round of work:

1. Guide stiffness ratio
   Π_k = k_eff λ^2 / (μ v^2)
   This compares restoring force scale to convective inertial forcing.

2. Damping ratio in the moving frame
   Π_c = c_eff λ / (μ v)
   This compares damping to transport-driven disturbance passage.

3. Gap margin ratio
   Π_g = y_max / g
   This measures how close disturbances run to geometric saturation.

4. Delay ratio
   Π_d = τ_delay v / λ
   This compares total loop delay to disturbance passage time.

For a robust design we likely need:
- Π_k comfortably above unity in the critical wavelength band
- Π_c not tiny
- Π_g well below unity
- Π_d much less than 1

## 14. Practical immediate consequences
Before any serious prototype, we need explicit numbers for:
- sensor spacing
- sensor latency
- actuator bandwidth
- actuator force density
- allowable gap
- rotor topology choice
- guide-segment length
- maximum tolerable imperfection wavelength and amplitude

Without these, claims about stability are theatre.

## 15. Recommended next technical steps
### Step 2A
Choose one rotor topology for the next pass:
- continuous cable/belt
- discrete slugs / carriages
- magnetically linked segmented train

### Step 2B
Build a simple numerical model for one straight guide segment with:
- transport speed v
- magnetic spring-damper guide law
- disturbance input
- sensor/actuator delay
- saturation at the guide gap

### Step 2C
Extend that model to a prescribed curved segment and verify that the same system can both:
- provide average support force
- remain locally stable under disturbance

### Step 2D
Then move to the helical tube case, where guide-force demand and global structural motion are coupled.

## 16. Bottom line
The Stage 1 concept survives Stage 2 in the following sense:
- there is a coherent local equation of motion
- the stabilizing problem is not mysterious, it is definable
- the dominant control burden comes from convective disturbance passage at speed v

But Stage 2 also sharpens the real warning:

A high-speed guided rotor is not just a structural element.
It is a fast transported dynamical system whose stability requirement hardens with increasing speed and shrinking disturbance wavelength.

My current judgment is:
- the concept still looks physically serious
- the control problem is likely one of the main gates to viability
- segmentation, multi-layer control, and ruthless attention to short-wavelength disturbance handling are likely mandatory
