# Sector Width, Section Transients, Bending Control, and Ring Coupling Memo

## Status
Second-pass control memo following Section 14 of the helical tug memo.

This note advances five specific items:
1. finite-width azimuthal sectors rather than point-sector approximations
2. transient filling and draining of a fast section
3. realistic actuator power and regenerative coupling at the two boundaries
4. closed-loop bending control of a finite tube segment using opposed sectors
5. how tangential tug patterns on a curved ring couple into ring-shape correction and tether load transfer

The goal is not a final flight-control model.
The goal is to get the first clean equations that connect the slug-train actuator concept to real structural control variables.

## 1. Finite-width azimuthal sectors
In the previous memo, a tug sector was treated like a point force applied at one azimuth.
That is useful, but real control sectors occupy a finite azimuthal width.

Take a tube of radius $a$.
Let a sector be centered at azimuth $\phi_0$ and span width $\Delta \phi$.
Suppose the boundary station generates a uniform axial tug density $q_z$ per unit arc length over that sector.
Then the differential force is

$$d\mathbf{F} = q_z a \, d\phi \, \mathbf{e}_z$$

and the position vector is

$$\mathbf{r}(\phi) = a \, \mathbf{e}_r(\phi)$$

So the total force is

$$\mathbf{F}_{\mathrm{sec}} = q_z a \Delta \phi \, \mathbf{e}_z$$

with magnitude

$$F_{\mathrm{sec}} = q_z a \Delta \phi$$

The bending moment about the tube centerline is

$$\mathbf{M}_{\mathrm{sec}} = \int_{\phi_0-\Delta\phi/2}^{\phi_0+\Delta\phi/2} \mathbf{r}(\phi) \times d\mathbf{F}$$

Carrying out the integral gives

$$M_{\mathrm{sec}} = a F_{\mathrm{sec}} \, C_{\mathrm{sec}}(\Delta\phi)$$

where the sector-width correction factor is

$$C_{\mathrm{sec}}(\Delta\phi) = \frac{\sin(\Delta\phi/2)}{\Delta\phi/2}$$

This is just a sinc factor.

Implications:
- narrow sectors have $C_{\mathrm{sec}} \approx 1$
- very wide sectors lose bending leverage because the load wraps around the circumference and partially self-cancels

Useful values:
- $\Delta\phi = 20^\circ$ -> $C_{\mathrm{sec}} \approx 0.995$
- $\Delta\phi = 60^\circ$ -> $C_{\mathrm{sec}} \approx 0.955$
- $\Delta\phi = 120^\circ$ -> $C_{\mathrm{sec}} \approx 0.827$
- $\Delta\phi = 180^\circ$ -> $C_{\mathrm{sec}} \approx 0.637$

So moderate-width sectors are fine, but whole-half-circumference sectors are noticeably less efficient as bending actuators.

## 2. Opposed sectors and pure bending
Take two equal sectors centered at opposite azimuths $\phi_0$ and $\phi_0 + \pi$.
If both sectors are given the **same** axial tug sign, their bending moments cancel.
If they are given **opposite** tug signs, the moments add.

Therefore pure first-order bending control should use opposed sectors commanded with opposite sign.

If each sector has magnitude $F_{\mathrm{sec}}$, the total bending moment is

$$M_{\mathrm{pair}} = 2 a F_{\mathrm{sec}} \, C_{\mathrm{sec}}(\Delta\phi)$$

This is the correct finite-width version of the earlier point-sector estimate.

## 3. Tug force from a finite sector of mirrored paired modules
From the previous memo, one mirrored paired module gives

$$F_{\mathrm{tug,1}} = 2 \dot m \, \Delta v \, \cos\alpha$$

If a sector contains $N_s$ paired modules, then

$$F_{\mathrm{sec}} = 2 N_s \dot m \, \Delta v \, \cos\alpha$$

and the corresponding opposed-sector bending moment is

$$M_{\mathrm{pair}} = 4 a N_s \dot m \, \Delta v \, \cos\alpha \, C_{\mathrm{sec}}(\Delta\phi)$$

This is the first equation I would use for actuator sizing.

## 4. Fast-section filling and draining: occupancy picture
The previous memo showed that a steady fast slug section is plausible.
But a real controller must create and remove that section in finite time.

Take one lane of a selected section of length $L$.
Let:
- $J$ = baseline slug number flux (slugs/s)
- $m_s$ = slug mass
- $v_0$ = baseline speed
- $v_1$ = commanded speed in the fast section

Then the steady slug density is

$$n = \frac{J}{v}$$

and the steady number of slugs in the section is

$$N = nL = \frac{JL}{v}$$

So the number change required to transition from $v_0$ to $v_1$ is

$$\Delta N = JL \left(\frac{1}{v_1} - \frac{1}{v_0}\right)$$

If $v_1 > v_0$, then $\Delta N < 0$.
The fast section contains fewer slugs and must be drained.

The corresponding mass change is

$$\Delta M = m_s \Delta N = \dot m L \left(\frac{1}{v_1} - \frac{1}{v_0}\right)$$

where $\dot m = J m_s$.

## 5. Controlled fill/drain rate
To change section occupancy, the controller must create a temporary difference between incoming and outgoing slug number flux.
Let

$$\delta J = J_{\mathrm{in}} - J_{\mathrm{out}}$$

Then the occupancy dynamics are

$$\frac{dN}{dt} = \delta J$$

and therefore

$$\frac{dM}{dt} = m_s \delta J$$

If $\delta J$ is approximately constant during a transition, the fill/drain time is

$$\tau_{\mathrm{fill}} \approx \frac{|\Delta N|}{|\delta J|}
= \frac{JL \left|\frac{1}{v_1} - \frac{1}{v_0}\right|}{|\delta J|}$$

Equivalently,

$$\tau_{\mathrm{fill}} \approx \frac{L \left|\frac{1}{v_1} - \frac{1}{v_0}\right|}{|\delta J|/J}$$

This is useful because it makes the tradeoff explicit:
- short transition time requires larger temporary flux mismatch
- larger temporary flux mismatch means more severe transient boundary forces and more control burden

## 6. Kinematic timescale lower bound
Even with arbitrarily powerful actuators, information and packets must traverse the section.
So there is also a transport lower bound of order

$$\tau_{\mathrm{conv}} \gtrsim \frac{L}{v_1}$$

Therefore the practical transition time cannot be much shorter than the larger of:
- occupancy adjustment time from flux mismatch
- transport time across the section

A useful rule is

$$\tau_{\mathrm{trans}} \gtrsim \max \left[ \frac{|\Delta N|}{|\delta J|}, \frac{L}{v_1} \right]$$

## 7. Boundary station power with regeneration
For one lane, accelerating mass flux $\dot m$ from $v_0$ to $v_1$ requires kinetic-power increment

$$\Delta P = \dot m \frac{v_1^2 - v_0^2}{2}$$

A decelerating lane can ideally return the same power.

If one boundary station both accelerates one lane and regeneratively decelerates the paired lane, then in the ideal reversible limit the net external power is zero apart from losses.

Let:
- $\eta_a$ = acceleration-chain efficiency from electrical bus to slug stream
- $\eta_r$ = regeneration efficiency from slug stream back to electrical bus

Then the net imported power at one boundary station is approximately

$$P_{\mathrm{net,st}} \approx \Delta P \left(\frac{1}{\eta_a} - \eta_r\right)$$

and the total import for both boundaries is

$$P_{\mathrm{net,tot}} \approx 2 \Delta P \left(\frac{1}{\eta_a} - \eta_r\right) + P_{\mathrm{misc\,loss}}$$

where $P_{\mathrm{misc\,loss}}$ includes control, magnetic, drag, and switching losses.

This is encouraging.
It means the actuation energy for maintaining a steady fast section can be far smaller than the raw kinetic throughput suggests if regenerative coupling is good.

## 8. Numerical sanity check
Take a notional sector with:
- $a = 50\,\mathrm{m}$
- $\alpha = 45^\circ$
- $N_s = 50$
- $\dot m = 100\,\mathrm{kg/s}$ per lane
- $v_0 = 1000\,\mathrm{m/s}$
- $v_1 = 1100\,\mathrm{m/s}$ so $\Delta v = 100\,\mathrm{m/s}$
- $\Delta \phi = 60^\circ$ so $C_{\mathrm{sec}} \approx 0.955$

Then

$$F_{\mathrm{sec}} = 2 N_s \dot m \Delta v \cos\alpha \approx 0.707\,\mathrm{MN}$$

and the opposed-sector bending moment is

$$M_{\mathrm{pair}} \approx 2 a F_{\mathrm{sec}} C_{\mathrm{sec}} \approx 67.5\,\mathrm{MN\cdot m}$$

The per-lane kinetic power increment is

$$\Delta P = \dot m \frac{v_1^2 - v_0^2}{2} = 10.5\,\mathrm{MW}$$

If $\eta_a = 0.95$ and $\eta_r = 0.90$, then one boundary station imports about

$$P_{\mathrm{net,st}} \approx 1.6\,\mathrm{MW}$$

and both stations together import about

$$P_{\mathrm{net,tot}} \approx 3.2\,\mathrm{MW}$$

plus miscellaneous losses.

That is not small, but it is much smaller than the raw kinetic throughput might suggest.

## 9. Finite-segment bending control model
Take a finite tube segment of length $L_t$.
Let $y(z,t)$ be the lateral deflection in one bending plane.
A reduced beam-like model is

$$m_t y_{tt} + c_t y_t + K_t y = q_{\mathrm{ext}} + q_{\mathrm{act}}$$

where:
- $m_t$ is effective line mass
- $c_t$ is effective damping
- $K_t$ is the structural restoring operator
- $q_{\mathrm{act}}$ is the distributed control loading induced by tug sectors

For a two-sector opposed actuator pair localized near station positions $z_A$ and $z_B$, the actuation can be modeled as an equivalent bending-moment couple:

$$M_{\mathrm{act}}(t) = 2 a F_{\mathrm{sec}}(t) C_{\mathrm{sec}}(\Delta\phi)$$

and the beam loading enters through moment gradients.

For a first-mode reduction with generalized coordinate $q(t)$,

$$m_1 \ddot q + c_1 \dot q + k_1 q = g_1 u + d_1$$

where the control input is naturally

$$u = \Delta v_+ - \Delta v_-$$

that is, the signed speed command difference between opposed sectors.

This is the control architecture result:
- common azimuthal command adjusts global pressure / axial load
- differential azimuthal command produces bending moment

## 10. Closed-loop bending idea
A minimal feedback law for one bending plane would be

$$u = -k_q q - k_{\dot q} \dot q$$

with saturation from actuator limits and occupancy-transition limits.

That is not profound, but it matters:
we now have a plausible physical control input, not just a vague steering story.

The hard part is not inventing a controller law.
The hard part is making sure the actuator dynamics, section-transient limits, and regenerative stations can actually realize the commanded $u(t)$ without lag or instability.

## 11. Curved-ring force balance
Now move from a straight tube to a ring of large radius $R_r$.
Let $s$ be arc length along the ring centerline, with unit tangent $\mathbf{t}(s)$ and normal $\mathbf{n}(s)$.
If the internal tangential force is $T(s)$, then

$$\frac{d}{ds} \big(T \mathbf{t}\big) = \frac{dT}{ds} \mathbf{t} + \kappa_r T \mathbf{n}$$

where

$$\kappa_r = \frac{1}{R_r}$$

So the tangential and normal force balances are linked.

This yields two important equations:

### Tangential balance
$$\frac{dT}{ds} + q_t(s) = 0$$

where $q_t$ is net external or actuator tangential load per unit ring length.

### Normal balance
$$\kappa_r T + q_n(s) = 0$$

where $q_n$ is net normal load per unit ring length.

## 12. Why tangential tug patterns matter on a ring
This is the key ring-level consequence.

If tug stations impose a spatial pattern of tangential actuator load $q_t(s)$, then they modify the ring tension field $T(s)$ through

$$\frac{dT}{ds} = -q_t(s)$$

And because the ring is curved, variation in $T$ changes the normal support condition through the $\kappa_r T$ term.

So tangential tug actuation can influence ring shape indirectly by changing the local tangential force field, which is then converted into normal load through curvature.

This is not hand-waving anymore.
It is the actual geometric coupling.

## 13. Tether load transfer interpretation
Suppose the ring has sparse grounded tether stations or support stations.
Those act like discrete external load insertion points.
The tug actuators cannot create net external force on the whole ring, but they can redistribute the internal tension field so that load is transported to and from those tether points.

In a coarse sense:
- tug stations create $q_t(s)$
- that reshapes $T(s)$ around the ring
- tether stations appear as localized external terms in the same tangential balance
- the resulting $T(s)$ field determines how load is shared and where curvature-derived support changes occur

So the tug system may act like a distributed load-transport layer for the ring.
That is exactly the kind of mechanism Hudson was reaching for.

## 14. What this means physically
The macro-control picture now looks like this:

### Local scale
Speed changes create fast sections and boundary tug stations.

### Tube scale
Opposed sectors convert axial tug into bending moments and shape-control authority.

### Ring scale
Tangential tug patterns reshape the internal tension field $T(s)$, which in a curved geometry couples into normal support and tether load sharing.

This is a coherent multiscale control story.

## 15. Main caveats
This memo is still a reduced-order treatment.
It ignores:
- detailed tube shell modes
- local lane mismatch and force ripple
- saturation of the occupancy transition process
- interaction between neighboring fast sections
- detailed tether dynamics
- full 3D ring modes

But the basic equations now exist, which is a real step.

## 16. Bottom line
The strongest new results are:

### Finite-width sector correction
$$M_{\mathrm{sec}} = a F_{\mathrm{sec}} \, C_{\mathrm{sec}}(\Delta\phi), \qquad C_{\mathrm{sec}} = \frac{\sin(\Delta\phi/2)}{\Delta\phi/2}$$

### Opposed-sector bending authority
$$M_{\mathrm{pair}} = 4 a N_s \dot m \, \Delta v \, \cos\alpha \, C_{\mathrm{sec}}(\Delta\phi)$$

### Section fill/drain time
$$\tau_{\mathrm{trans}} \gtrsim \max \left[ \frac{JL \left|\frac{1}{v_1} - \frac{1}{v_0}\right|}{|\delta J|}, \frac{L}{v_1} \right]$$

### Station power with regeneration
$$P_{\mathrm{net,tot}} \approx 2 \dot m \frac{v_1^2 - v_0^2}{2} \left(\frac{1}{\eta_a} - \eta_r\right) + P_{\mathrm{misc\,loss}}$$

### Ring tangential-force transport
$$\frac{dT}{ds} + q_t(s) = 0, \qquad \kappa_r T + q_n(s) = 0$$

My current judgment is:
- the actuator concept survives this next pass
- the opposed-sector bending channel looks physically meaningful
- regenerative boundary stations make the power picture less frightening than it first appears
- the ring-control idea is becoming concrete: tug stations transport tangential load, and ring curvature converts that into shape and tether-load effects
