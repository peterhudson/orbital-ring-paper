# Distributed Slug Transition and Load-Transport Memo

## Status
This memo follows Section 15 of the previous slug-control memo and digs into the distributed-actuation branch that Hudson prefers.

The focus here is fivefold:
1. distributed-transition wave propagation through a finite slug section
2. minimum-gap constraints during downward speed ramps
3. catch-up constraints for upward ramps under incomplete section-wide actuation
4. how smooth distributed transitions smear or preserve the tug effect
5. whether purely distributed actuation can still provide the ring-scale load-transfer authority we want, or whether hard tug nodes are still necessary

## 1. Executive summary
The cleanest picture I have now is:

- a distributed speed transition can change section occupancy without literal fill/drain hardware
- for a monotone distributed slowdown, the minimum spacing is set by the final slow-state spacing, not by some extra hidden dynamic catastrophe
- for an upward ramp, the real risk is lag between the entrant acceleration and the activation of the slugs already ahead of it
- smooth distributed transitions do **not** destroy the tug effect, they smear it into a distributed axial load density
- the integrated tug across the transition is preserved
- therefore a purely distributed actuator field can still transport tangential load around a ring
- hard tug nodes are useful for sharp localization and special high-authority interfaces, but they do not appear strictly necessary everywhere

## 2. Discrete slug spacing dynamics in a prescribed speed field
Label consecutive slug centers by $x_i(t)$ with increasing index in the forward direction.
Suppose each slug follows the local commanded speed field

$$\dot x_i = v(x_i,t)$$

Let the center-to-center spacing be

$$s_i = x_{i+1} - x_i$$

Then

$$\dot s_i = v(x_{i+1},t) - v(x_i,t)$$

For smoothly varying fields and small relative spacing,

$$\dot s_i \approx \frac{\partial v}{\partial x} \, s_i$$

Hence

$$s_i(t) = s_i(0) \exp\left(\int_0^t \frac{\partial v}{\partial x}(x_i(\tau),\tau) \, d\tau \right)$$

This is the basic spacing-evolution law.

Interpretation:
- positive velocity gradient stretches spacing
- negative velocity gradient compresses spacing

This is the clean mathematical form of the virtual fill/drain picture.

## 3. Distributed transition wave model
Take a transition profile moving through the section:

$$v(x,t) = V\!\left(\frac{x-c_f t}{\lambda}\right)$$

where:
- $c_f$ is the transition-front propagation speed through the stator frame
- $\lambda$ is the characteristic transition width
- $V(\xi)$ changes smoothly from $v_0$ to $v_1$

The local gradient is

$$\frac{\partial v}{\partial x} = \frac{1}{\lambda} V'(\xi)$$

So a narrower transition width $\lambda$ creates stronger compression/stretching rates, while a broader transition spreads them out over longer distance and time.

A useful characteristic transition time for one slug crossing the front is

$$\tau_{\lambda} \sim \frac{\lambda}{|v_* - c_f|}$$

where $v_*$ is a representative slug speed in the front.

This is the first design tradeoff:
- small $\lambda$ gives sharper tug density and sharper control
- large $\lambda$ gives gentler spacing dynamics and less actuator shock

## 4. Minimum-gap constraint during downward ramps
Consider a monotone slowdown from $v_0$ to $v_1 < v_0$.
Assume all slugs eventually see the same transition profile, just shifted in time.

Let the baseline headway be $h$.
Then the exact spacing relation is

$$s(\tau) = \int_{\tau-h}^{\tau} v(\xi) \, d\xi$$

If $v(\tau)$ is monotone decreasing from $v_0$ to $v_1$, then

$$h v_1 \le s(\tau) \le h v_0$$

for all $\tau$.

Therefore the minimum spacing is simply

$$s_{\min} = h v_1$$

and the collision-avoidance condition is

$$h v_1 \ge \ell_s + g_{\min}$$

This is an important result.

For a clean monotone distributed slowdown, the minimum-gap condition is not worse than the final slow-state spacing. The transition shape itself does not add a stricter first-order gap constraint.

So if the system is safe in the target slow state, it is safe throughout the monotone slowdown transition.

## 5. Compression ratio under slowdown
If the initial spacing is

$$s_0 = h v_0$$

and the final spacing is

$$s_1 = h v_1$$

then the compression ratio is

$$\frac{s_1}{s_0} = \frac{v_1}{v_0}$$

This is independent of transition width.
Transition width changes how quickly the compression happens, not the total compression required by the final state.

## 6. Upward ramp with incomplete actuation: catch-up criterion
Now consider the dangerous case: a faster target state $v_1 > v_0$.
If a trailing slug is accelerated before the leading incumbent ahead of it, their relative closing speed is approximately

$$\Delta v = v_1 - v_0$$

until the incumbent begins accelerating.

If the incumbent's acceleration is delayed by $\tau_d$, the gap shrinks by

$$\Delta s_{\mathrm{loss}} \approx \Delta v \, \tau_d$$

To avoid rear-end catch-up we need

$$\Delta v \, \tau_d < s_0 - s_{\mathrm{safe}}$$

where

$$s_0 = h v_0, \qquad s_{\mathrm{safe}} = \ell_s + g_{\min}$$

So the admissible delay is

$$\tau_d < \frac{h v_0 - (\ell_s + g_{\min})}{v_1 - v_0}$$

This is the key upward-ramp safety inequality.

It says the actuation of the slugs already inside the section must propagate ahead fast enough that the entrants do not consume the available gap margin.

## 7. Front-speed version of the same criterion
If the acceleration command front propagates into the section at speed $c_f$ in the stator frame, and the leading slug is one initial spacing $s_0$ ahead, then the activation delay is roughly

$$\tau_d \approx \frac{s_0}{c_f}$$

Substituting into the previous condition gives

$$c_f > \frac{s_0 (v_1 - v_0)}{s_0 - s_{\mathrm{safe}}}$$

If the safety margin is generous, this reduces approximately to

$$c_f \gtrsim v_1 - v_0$$

That is a useful intuitive rule:

**the actuation front must outrun the relative closing speed created by the upward ramp.**

In practice electronic command propagation is easy, but actual actuator response of the incumbents is the real bottleneck.

## 8. Distributed tug density from a smooth transition
For one lane with mass flux $\dot m$, the stream momentum flux is

$$\Pi = \dot m v$$

So the force per unit length applied to the stream by a spatial speed gradient is

$$q_{\mathrm{stream}} = \dot m \frac{dv}{dx}$$

and the reaction on the stator is

$$q_{\mathrm{stator}} = -\dot m \frac{dv}{dx}$$

For a mirrored helical pair in one sector, the axial tug density becomes

$$q_z(x) = -2 N_s \dot m \cos\alpha \, \frac{dv}{dx}$$

This is the distributed version of the earlier node-based tug law.

## 9. Integrated tug is preserved
Integrate the tug density across the transition zone:

$$F_z = \int q_z \, dx = -2 N_s \dot m \cos\alpha \int \frac{dv}{dx} \, dx$$

Hence

$$F_z = -2 N_s \dot m \cos\alpha \, (v_1 - v_0)$$

or in magnitude,

$$|F_z| = 2 N_s \dot m \Delta v \cos\alpha$$

This is exactly the same integrated tug magnitude derived earlier for an idealized hard boundary station.

This is a central result.

**Smoothing the transition does not destroy the tug. It only distributes it over a finite length scale.**

## 10. Peak tug density versus transition width
If the transition occurs approximately uniformly over width $\lambda$, then

$$\frac{dv}{dx} \sim \frac{\Delta v}{\lambda}$$

and the characteristic axial tug density is

$$q_z^{\mathrm{peak}} \sim 2 N_s \dot m \cos\alpha \frac{\Delta v}{\lambda}$$

So smoothing reduces local force concentration by a factor proportional to $1/\lambda$ while preserving total integrated load transfer.

This is exactly the kind of tradeoff we want:
- larger $\lambda$ means gentler local forces
- total tug authority stays the same
- the price is reduced spatial sharpness

## 11. Opposed sectors with smooth transitions
If opposite azimuthal sectors are commanded with opposite sign, the distributed bending-moment density becomes

$$m_b(x) \sim 2 a \, q_z(x) \, C_{\mathrm{sec}}(\Delta\phi)$$

where the finite-sector correction is still

$$C_{\mathrm{sec}}(\Delta\phi) = \frac{\sin(\Delta\phi/2)}{\Delta\phi/2}$$

Integrating over the transition region yields the total bending moment step

$$M_b = 4 a N_s \dot m \Delta v \cos\alpha \, C_{\mathrm{sec}}(\Delta\phi)$$

So again, smoothing preserves total bending authority while softening local loading.

## 12. Can distributed transitions still transport load around a ring?
Yes, at least in the reduced-order sense.

On a ring, tangential load balance is

$$\frac{dT}{ds} + q_t(s) = 0$$

where $T(s)$ is tangential force in the ring and $q_t$ is tangential actuator load per unit length.

A distributed tug transition is exactly such a $q_t(s)$ field.
If the transition goes from $v_0$ to $v_1$, then the net tension change across it is

$$\Delta T = -\int q_t(s) \, ds$$

and therefore

$$\Delta T = 2 N_s \dot m \Delta v \cos\alpha$$

up to sign convention.

This means a distributed transition can step the ring's internal tangential force field by the same amount as a hard tug node.

That is the key ring-level conclusion.

## 13. What hard nodes still buy you
If distributed transitions preserve integrated load transfer, why have hard nodes at all?

Because hard or semi-hard nodes still buy:
- sharper localization in space
- shorter effective control lag
- stronger coupling to sparse tether/support points
- easier metering of power and regeneration at special interfaces
- special handling for startup, shutdown, storage, or faults

So the distinction is now clearer:

- **distributed transitions** are sufficient for low-bandwidth load transport and shape control
- **hard nodes** are valuable where you need sharp localization, special infrastructure, or high-authority coupling to external supports

## 14. My current architecture preference
For an orbital-ring-like control system, my current preference is:

### Ordinary control segments
Use smooth distributed transitions with no explicit fill/drain hardware.

### Special strategic nodes
Use enhanced stations only where needed, such as:
- tether interfaces
- startup / shutdown / maintenance hubs
- major load-exchange regions
- fault-isolation or recovery points

This keeps the ordinary system simpler while preserving the option for more aggressive actuation where it is most valuable.

## 15. Practical implications for control bandwidth
Distributed transitions imply that the control input is not a pure force impulse but a spatially extended profile.
That means:
- lower local stress and force ripple
- lower effective bandwidth
- better compatibility with slow macro-control tasks like orbital-shape management

This aligns well with Hudson's judgment that the orbital ring likely has low control bandwidth requirements.

## 16. Bottom line
The strongest new results are:

### Spacing evolution
$$\dot s \approx \frac{\partial v}{\partial x} s$$

### Safe monotone slowdown condition
$$h v_1 \ge \ell_s + g_{\min}$$

### Upward-ramp delay bound
$$\tau_d < \frac{h v_0 - (\ell_s + g_{\min})}{v_1 - v_0}$$

### Distributed tug density for mirrored paired helices
$$q_z(x) = -2 N_s \dot m \cos\alpha \, \frac{dv}{dx}$$

### Integrated tug / tension step
$$\Delta T = 2 N_s \dot m \Delta v \cos\alpha$$

My current judgment is:
- distributed actuation without fill/drain hardware remains the best default architecture
- smooth transitions preserve the core load-transport authority we care about
- the main design challenge is not whether the tug survives smoothing, but whether upward ramps are propagated cleanly enough to avoid catch-up under incomplete actuation
- hard nodes still look useful, but as special infrastructure rather than as the universal primitive
