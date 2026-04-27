# Slug Control With and Without Fill/Drain Memo

## Status
This memo digs into Hudson's question about whether a paired slug-train tug system really needs explicit fill/drain hardware, or whether a selected section can be controlled by changing slug velocities alone.

The main conclusion is:
- explicit physical insertion/removal of slugs is **not** required in order to change the occupancy of a selected section
- occupancy can change kinematically through spacing expansion or compression
- however, whether this is cleanly achievable depends strongly on the control architecture
- **boundary-only speed changes** are not equivalent to **section-wide speed changes**

That distinction is the heart of the issue.

## 1. Three architectures to keep separate
There are really three different control architectures under discussion.

### Architecture A: Boundary-only speed control, no fill/drain hardware
At stations $A$ and $B$, slugs are accelerated or decelerated, but there is no explicit storage, insertion, or removal hardware, and no distributed actuation along the section interior.

### Architecture B: Distributed speed control, no fill/drain hardware
The stator along the selected section can accelerate or decelerate the slugs already inside the section. No slugs are physically added or removed, but their spacing and speed field can be changed throughout the section.

### Architecture C: Boundary control with explicit fill/drain or storage
Stations can temporarily store, insert, remove, or reroute slugs so that section occupancy can be changed directly rather than only through kinematic spacing changes.

Hudson's question is essentially whether A or B can work well enough that C is only needed at a few special nodes.

## 2. Discrete slug kinematics and headway
Take one lane of identical slugs of length $\ell_s$ and mass $m_s$.
Let the time headway between consecutive slugs at some reference station be $h$.
Then the number flux is

$$J = \frac{1}{h}$$

and the mass flux is

$$\dot m = \frac{m_s}{h}$$

If a locally uniform region has slug speed $v$, then the center-to-center spacing is

$$s = v h$$

and the effective line density is

$$\mu_{\mathrm{eff}} = \frac{m_s}{s} = \frac{m_s}{v h} = \frac{\dot m}{v}$$

So for a steady slug stream at fixed mass flux,

$$\mu_{\mathrm{eff}} \propto \frac{1}{v}$$

and the curvature support law becomes

$$f = \mu_{\mathrm{eff}} v^2 \kappa = \dot m v \kappa$$

This was the key result from the previous memo: at fixed slug flux, support scales linearly with speed.

## 3. Occupancy of a selected section
Take a selected section of length $L$.
If the lane speed in that section is uniformly $v$, then the number of slugs in the section is

$$N = \frac{L}{s} = \frac{L}{v h} = \frac{J L}{v}$$

So changing the speed from $v_0$ to $v_1$ changes occupancy from

$$N_0 = \frac{J L}{v_0}, \qquad N_1 = \frac{J L}{v_1}$$

and therefore

$$\Delta N = J L \left(\frac{1}{v_1} - \frac{1}{v_0}\right)$$

This is the first important answer to Hudson's question:

**a section can contain more or fewer slugs without physically adding or removing slugs from the whole loop**.

The occupancy change can happen by changing the spacing field.

So explicit slug insertion/ejection is **not fundamentally required**.

## 4. But not every speed-control architecture can realize that cleanly
The real issue is not whether occupancy can change.
It is whether the control law that changes it is physically safe and dynamically clean.

This is where architectures A, B, and C separate sharply.

## 5. Architecture A: boundary-only speed changes
Suppose the section between $A$ and $B$ is initially occupied by slugs at speed $v_0$.
Now at time $t=0$, station $A$ begins accelerating entering slugs toward a higher speed $v_1 > v_0$, while the slugs already inside the section continue at $v_0$ until they reach $B$.

This is dangerous.
The newly accelerated slug can catch the slower slug immediately ahead of it.

If the initial center-to-center spacing is $s_0 = v_0 h$, the nominal catch time is roughly

$$t_{\mathrm{catch}} \approx \frac{s_0}{v_1 - v_0}$$

and the nominal catch distance is

$$d_{\mathrm{catch}} \approx v_1 t_{\mathrm{catch}} = \frac{v_1 s_0}{v_1 - v_0}$$

For illustrative numbers:
- $s_0 = 2\,\mathrm{m}$
- $v_0 = 1000\,\mathrm{m/s}$
- $v_1 = 1100\,\mathrm{m/s}$

then

$$t_{\mathrm{catch}} \approx 0.02\,\mathrm{s}, \qquad d_{\mathrm{catch}} \approx 22\,\mathrm{m}$$

So a boundary-only command that tries to create a **faster** occupied section by accelerating new entrants while incumbents remain slow is basically hopeless for long sections.

This is the first hard conclusion:

**Architecture A cannot cleanly create an upward speed step into an already occupied section unless the incumbent slugs are also accelerated.**

## 6. Boundary-only slowdown is less pathological
Now consider the opposite command: creating a **slower** section from a faster baseline.
At $A$, incoming slugs are decelerated from $v_0$ to $v_1 < v_0$ while slugs already in the section ahead remain at $v_0$ until they leave.

In this case the entering slug does **not** chase the incumbent ahead. That part is fine.
The real risk is rear-end compression from the following slug behind.

So boundary-only slowdown is not automatically impossible, but it requires enough baseline headway that the compressed spacing remains safe.

This asymmetry matters.
It suggests that if one insisted on Architecture A, then a system biased at a higher nominal speed and actuated by local slowdowns would be much more natural than one biased low and actuated by local speedups.

## 7. Safe spacing under a speed-only control law
Suppose consecutive slugs experience the same velocity program $v(\tau)$, but offset in time by headway $h$.
Then the center-to-center spacing at the same physical time is

$$s(\tau) = \int_{\tau-h}^{\tau} v(\xi) \, d\xi$$

This is an important exact relation for identical time-shifted actuation.

A sufficient collision-avoidance condition is

$$s(\tau) \ge \ell_s + g_{\min} \qquad \text{for all } \tau$$

where $g_{\min}$ is the required minimum free gap.

Two important corollaries:

### If $v(\tau)$ is ramping upward
Spacing grows. Rear-end collision between similarly controlled neighboring slugs is not the issue.
The issue is instead catching pre-existing slower incumbents if the section interior has not yet been sped up.

### If $v(\tau)$ is ramping downward
Spacing shrinks. The limiting condition is usually the slow-state spacing,

$$s_{\mathrm{slow}} = h v_1$$

so a simple safe-design inequality is

$$h v_1 \ge \ell_s + g_{\min}$$

or equivalently

$$h \ge \frac{\ell_s + g_{\min}}{v_1}$$

This is the second hard result.

A no-fill/drain slug controller is feasible only if the baseline headway is large enough for the **slowest** commanded speed.

## 8. Architecture B: distributed speed control along the section
Now suppose the selected section itself can apply the speed command to the slugs already inside it.
Then a change from $v_0$ to $v_1$ does not rely on a single hard interface at $A$.
Instead, a transition wave or ramp can propagate through the section.

This is much cleaner.

### Why it works
- incumbents already inside the section can be accelerated or decelerated too
- a fast entrant at $A$ no longer runs into a slow incumbent ahead, because the incumbent is also being sped up
- occupancy change happens through spacing expansion/compression across the section, not through literal slug insertion/removal

This is probably the simplest architecture that makes Hudson's control idea physically plausible without requiring storage hardware at every station.

## 9. Transition times without fill/drain hardware
Even without explicit fill/drain hardware, the section occupancy still changes over time.
But it does so kinematically, through spacing changes and moving transition fronts.

A useful lower-bound timescale is the section transport time,

$$\tau_{\mathrm{conv}} \gtrsim \frac{L}{v_*}$$

where $v_*$ is a characteristic speed during the transition.

A second timescale is the local actuator ramp time $\tau_a$ required to move one slug from $v_0$ to $v_1$ subject to station or distributed acceleration limits.

So a realistic no-fill/drain transition time is at least of order

$$\tau_{\mathrm{trans}} \gtrsim \max\left(\tau_a, \frac{L}{v_*}\right)$$

This is slower than a hypothetical architecture with direct occupancy control, but it may still be perfectly adequate if macro-control bandwidth is low, which it likely is for orbital-scale steering.

## 10. What fill/drain hardware actually buys you
Explicit fill/drain or storage hardware does **not** create the possibility of occupancy change from nothing.
That was already possible kinematically.

What it buys you is:
- faster transitions
- sharper spatial plateaus
- the ability to change occupancy without waiting for a transition wave to traverse the section
- extra local authority if baseline headway is too tight for the desired slow state
- more flexibility to decouple section occupancy control from the main ring-wide slug flux

So fill/drain is a performance and controllability upgrade, not a logical necessity.

## 11. A useful reinterpretation: virtual filling/draining by spacing
It may help to rename what is happening in Architecture B.

There is no literal slug insertion/removal, but there **is** effective filling/draining of the section occupancy through spacing compression and expansion.

So the selected section can be thought of as being:
- **virtually drained** when a fast state stretches the spacing
- **virtually filled** when a slow state compresses the spacing

That may be the cleanest mental model.

## 12. Pressure/tug control implications
For a paired slug system, the control effect of a speed-modulated section has two components:

1. distributed support change inside the section
2. momentum reactions where the speed field changes in space or time

With Architecture B, those reactions are distributed over the transition zones rather than concentrated only at idealized hard boundaries.

That is probably a good thing.
It means:
- lower local actuator shock
- gentler structural loading
- less severe force ripple
- more control over transition bandwidth

So the price of distributed actuation is hardware complexity, but the benefit is a much more physical control field.

## 13. Design fork: what seems best right now
My current ranking is:

### Best near-term architecture
**Distributed speed control with no explicit fill/drain hardware at ordinary tug sections**.

Why:
- physically plausible
- avoids the hardest catch-up pathology
- keeps station complexity lower
- still allows occupancy change by spacing kinematics
- likely enough for low-bandwidth macro control

### Valuable upgrade at a few major nodes
**Optional fill/drain/storage hardware at special stations only**.

Why:
- gives extra authority
- helps with startup, shutdown, recovery, and fault handling
- may be useful near sparse tether/support nodes
- not needed everywhere

### Least attractive as a general solution
**Boundary-only speed step control with no distributed actuation**.

Why:
- upward speed steps into occupied sections are pathological
- control authority is too dependent on headway luck and transient geometry
- likely to create the exact ugly dynamics Hudson is worried about

## 14. A surprising implication for system bias point
If the system has no fill/drain hardware and only weak distributed authority, then the safest operational bias may be:
- choose a relatively high nominal speed
- create local control sections by slowing selected regions down rather than speeding them up

Why:
- boundary-only slowdown is less pathological than boundary-only speedup
- compressed spacing is easier to reason about than a fast newcomer chasing a slow incumbent

This is not yet a universal design rule, but it is a real systems insight worth keeping in mind.

## 15. Recommended next equations and simulations
The next pass should quantify:
1. distributed-transition wave propagation through a finite slug section
2. minimum-gap constraints during downward speed ramps
3. catch-up constraints for upward ramps under incomplete section-wide actuation
4. how smooth distributed transitions smear or preserve the boundary tug effect
5. whether a purely distributed actuator can still provide the ring-scale load-transfer authority we want, or whether some hard tug nodes are still necessary

## 16. Bottom line
The answer to Hudson's core question is:

- **No, explicit physical fill/drain hardware is not required to change section occupancy.**
- **Yes, speed-only control is possible in principle.**
- **But only some speed-only architectures are physically clean.**

My current judgment is:
- occupancy can be changed kinematically by spacing expansion/compression
- distributed section-wide actuation is the cleanest way to do that without fill/drain hardware
- boundary-only upward speed steps into an occupied section are probably not acceptable
- optional storage/fill/drain hardware still looks useful at a few special stations, but not as a universal requirement
