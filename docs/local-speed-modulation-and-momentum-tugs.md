# Local Speed Modulation and Momentum Tugs Memo

## Status
First-pass memo on a question Hudson raised after reviewing the paired-rotor module memo:

Can localized rotor speed modulation be used to steer or control the macro structure, and how does the answer differ for a continuous cable versus a train of discrete slugs?

The short answer is:
- for a continuous cable, true long-lived localized speed plateaus are probably not the right primitive, because they imply axial strain and stress-wave problems
- for a discrete slug train, localized high-speed sections look much more plausible
- in the slug-train case, the most important control effect may be not just differential inflation pressure, but also the boundary reaction forces at the speed-change stations

Those boundary reactions behave like internal momentum tugs.

## 1. The core distinction
There are two very different rotor models hiding under the same word "rotor":

1. **Continuous material loop**
   - cable, belt, or other materially connected moving member
   - neighboring material points are mechanically coupled
   - local speed changes imply strain, compression/extension, and stress waves

2. **Discrete transported mass packets**
   - slugs, pellets, carriages, or gapped segments
   - neighboring packets need not be strongly mechanically coupled
   - local speed changes can be imposed by changing packet velocity and spacing without the same axial-stress penalty

This distinction is not cosmetic.
It changes the macro-control architecture.

## 2. Continuous cable: why Hudson's objection is right
Let a continuous loop have local linear density $\mu(x,t)$ and speed $v(x,t)$.
Mass conservation gives

$$\frac{\partial \mu}{\partial t} + \frac{\partial (\mu v)}{\partial x} = 0$$

If we ask for a steady section with a different speed, then the mass flux

$$\dot m = \mu v$$

must stay continuous around the loop.
So if one section has larger $v$, it must have smaller $\mu$.

For a materially connected cable, changing $\mu$ means changing axial stretch state.
In other words, a localized speed plateau in a continuous cable is not free.
It implies:
- local strain change
- axial stress change
- traveling stress / extension waves during transients
- likely ugly dynamics if the section is long and repeatedly modulated

So Hudson's concern is correct:
for a continuous cable, trying to maintain a 100 km fast section inside a much longer loop is likely to launch axial disturbances and pogo-like behavior unless the cable is intentionally designed as a highly compliant, compressible transport medium.

That does not mean a continuous cable is impossible.
It means localized quasi-steady speed-pattern control is probably not its cleanest control channel.

## 3. Discrete slug train: continuity law
Now take a rotor lane made of discrete slugs of mass $m_s$.
Let:
- $n(x,t)$ = slug number density, slugs per meter
- $v(x,t)$ = local slug speed
- $J(x,t) = n v$ = slug number flux, slugs per second

Slug conservation gives

$$\frac{\partial n}{\partial t} + \frac{\partial (n v)}{\partial x} = 0$$

The effective moving mass density is

$$\mu_{\mathrm{eff}} = n m_s$$

and the local curvature-guide force per stator length is

$$f = \mu_{\mathrm{eff}} v^2 \kappa = n m_s v^2 \kappa$$

where $\kappa$ is local path curvature.

## 4. Key result for a steady high-speed slug section
Suppose a section is driven to a steady higher speed $v_1$ while the surrounding lane runs at $v_0$, and suppose slug number flux $J$ is steady through the lane.
Then

$$n = \frac{J}{v}$$

so inside the fast section the slug density drops.
Substituting into the support law gives

$$f = J m_s v \kappa$$

This is a very important result.

For a discrete slug train at fixed slug flux, local support force per stator length scales **linearly** with speed, not quadratically.

That is different from the continuous-cable picture with fixed $\mu$.

So if a high-speed slug section has

$$v_1 = r v_0$$

then, at fixed flux,

$$\frac{f_1}{f_0} = r$$

not $r^2$.

The same applies to pressure-like support quantities derived from the guide force.

## 5. Paired slug lanes in a helical stator
For a symmetric paired module with equal slug mass flux $\dot m$ in each lane and local curvature $\kappa$, the total support-force density is

$$f_{\mathrm{pair}} = \dot m v_1 \kappa + \dot m v_2 \kappa = \dot m (v_1 + v_2) \kappa$$

If both lanes in a selected region are driven to the same speed $v$, then

$$f_{\mathrm{pair}} = 2 \dot m v \kappa$$

For a helical tube where $\kappa = \sin^2 \alpha / a$, the same conclusion carries over into the equivalent pressure model:

local pressure from a steady-speed slug train scales linearly with the local common-mode speed if slug mass flux is held fixed.

This modifies the earlier continuous-density intuition.

## 6. How to create a high-speed section in a paired slug system
Take a selected section between points $A$ and $B$.
Let lane $x$ travel from $A$ to $B$ through the section, and lane $y$ travel from $B$ to $A$.
To create a higher-speed section:

At point $A$:
- accelerate slugs in lane $x$ from $v_0$ to $v_1$
- decelerate slugs in lane $y$ from $v_1$ to $v_0$

At point $B$:
- decelerate slugs in lane $x$ from $v_1$ to $v_0$
- accelerate slugs in lane $y$ from $v_0$ to $v_1$

This creates a standing fast section between $A$ and $B$ in both lanes.

## 7. Energy bookkeeping at the boundaries
For one lane with mass flux $\dot m$, changing speed from $v_0$ to $v_1$ requires power

$$P_{\mathrm{acc}} = \dot m \frac{v_1^2 - v_0^2}{2}$$

while decelerating from $v_1$ to $v_0$ yields the same amount back in ideal regeneration.

So at point $A$:
- energy can be taken from the decelerated lane and fed into the accelerated lane

Likewise at point $B$.

That means a steady high-speed section can exist with little net power beyond losses, provided the boundary stations are regenerative and efficiently coupled.

This is encouraging.

## 8. Boundary momentum-tug force
Now the important part.

For a mass flux $\dot m$ changing velocity from $\mathbf{u}_{\mathrm{in}}$ to $\mathbf{u}_{\mathrm{out}}$, the reaction force on the stator/actuator is

$$\mathbf{F}_{\mathrm{react}} = \dot m (\mathbf{u}_{\mathrm{in}} - \mathbf{u}_{\mathrm{out}})$$

At point $A$ in the paired section:
- lane $x$ is accelerated along $+\mathbf{t}$ from $v_0$ to $v_1$
- lane $y$ is decelerated while moving along $-\mathbf{t}$ from $v_1$ to $v_0$

So the reaction from lane $x$ is

$$\mathbf{F}_{A,x} = \dot m (v_0 - v_1) \mathbf{t} = -\dot m \Delta v \, \mathbf{t}$$

and the reaction from lane $y$ is

$$\mathbf{F}_{A,y} = \dot m (-v_1 + v_0) \mathbf{t} = -\dot m \Delta v \, \mathbf{t}$$

where

$$\Delta v = v_1 - v_0$$

Therefore the total boundary force at $A$ is

$$\mathbf{F}_A = -2 \dot m \Delta v \, \mathbf{t}$$

Similarly, at $B$,

$$\mathbf{F}_B = +2 \dot m \Delta v \, \mathbf{t}$$

This is the main new result in the memo.

The high-speed section behaves like an internal force dipole:
- one tug at $A$
- an equal and opposite tug at $B$

The structure between them feels a controlled internal axial loading pair.

## 9. What this means physically
Hudson's intuition was good.
The macro-control effect may not be primarily "pressure steering" in the gas-pressure sense.
It may be better understood as a combination of:

1. **distributed support change inside the section**
   - because the faster slugs create higher guide-force density

2. **boundary momentum tugs at the section ends**
   - because the boundary stations exchange momentum with the slug streams

The second effect may be the more important one for long-scale steering.

The pair of boundary stations acts like a virtual internal tether pair.

## 10. What the tug pair can and cannot do
### It can do
- create internal forces that reshape the macro structure
- transfer load from one region of the ring/tube to another
- create bending moments if deployed asymmetrically around the structure
- potentially shuttle control forces toward sparse grounded tether points or other anchor regions

### It cannot do by itself
- create net external force on the entire closed structure
- move the center of mass of the whole ring without some external interaction

So if there are no tethers and no other external coupling, the tug pair can reshape the structure and redistribute internal load, but not give the entire ring a net push through space.

That is an important control-theory boundary.

## 11. Why this may still be exactly what is needed
An orbital ring or launch-loop-like structure is not just a rigid body that needs a shove.
It is a huge distributed structure that needs:
- shape control
- wobble damping
- load redistribution
- force transfer to the places where external support exists

For those tasks, an internal tug pair is extremely useful.
It can create local bending moments and long-scale shape corrections even though its net external force is zero.

So this may indeed be the right way to think about macro control.

## 12. Helical geometry implication
If the paired lanes lie on a symmetric clockwise/counterclockwise helical geometry, the boundary tug vector can be decomposed into:
- axial component along the tube
- circumferential component around the tube

With proper mirrored geometry, the circumferential components can be designed to cancel while the useful axial components add.

That would be ideal.
It would let the module create a clean axial tug on the tube without twisting it.

This needs to be derived carefully in the next pass, but it is a plausible and important design target.

## 13. Design consequence for rotor choice
This memo sharpens the rotor-topology decision.

If macro control depends on creating localized high-speed plateaus and boundary tug stations, then:
- a **continuous cable** looks awkward for that role
- a **discrete slug train** or **segmented carriage train** looks much more natural

That does not decide the rotor architecture by itself.
But it strongly suggests that the macro-control concept Hudson described is better matched to discrete transported masses than to a continuous cable loop.

## 14. Most useful next equations
The next pass should quantify:
1. support and pressure authority of a slug section as a function of $\dot m$, $v_0$, $v_1$, and section length $L$
2. transient filling / draining dynamics of the section, using the slug continuity law
3. boundary tug magnitude and bandwidth for realistic actuator stations
4. how tug pairs combine when many sections are commanded simultaneously
5. the helical decomposition of the tug vector into axial, radial, and circumferential components

## 15. Bottom line
The new picture is:

- **continuous cable:** local speed modulation is likely stress-wave control, not a clean long-lived local actuator
- **discrete slug train:** local speed sections are plausible
- **paired slug train:** regenerative boundary stations can create both higher local support and equal-and-opposite momentum tugs at the section ends

My current judgment is:
- Hudson's new idea is important and probably right
- for macro control, the boundary tug picture may be more fundamental than the pressure picture
- this is a serious argument in favor of discrete or segmented transported masses over a continuous cable if large-scale steering is a core requirement
