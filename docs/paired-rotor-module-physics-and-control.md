# Paired Rotor Module Physics and Control Memo

## Status
First-pass memo for the paired counter-moving rotor module.

This memo treats the symmetric paired module, rather than the single rotor, as the basic design atom.
The goal is to derive the cleanest first-order relations for:
- momentum cancellation
- torque balance
- spin-up / spin-down behavior
- local support-force generation
- common-mode versus differential-mode control
- how local speed modulation could create macro-scale steering authority

## 1. Working paired-module model
Consider a conjoined figure-8 or Siamese-twin stator containing two rotor lanes.

At a matched local station, let the two rotor velocity vectors be

$$\mathbf{u}_1 = v_1 \, \mathbf{t}, \qquad \mathbf{u}_2 = -v_2 \, \mathbf{t}$$

where:
- $v_1, v_2 \ge 0$ are the speed magnitudes in the two lanes
- $\mathbf{t}$ is a local unit tangent direction for lane 1
- lane 2 is arranged so its local velocity is the opposite vector

Let both lanes have the same rotor linear density $\mu$.

This captures the intended paired architecture:
- equal and opposite local flow directions
- symmetric geometry
- equal support-force direction into the surrounding structure

## 2. Net linear momentum of the pair
The linear momentum per unit rotor length is

$$\mathbf{p}_{\mathrm{pair}} = \mu \mathbf{u}_1 + \mu \mathbf{u}_2 = \mu (v_1 - v_2) \, \mathbf{t}$$

So if the pair is speed-matched,

$$v_1 = v_2 = v$$

then

$$\mathbf{p}_{\mathrm{pair}} = 0$$

This is the first key result.
A perfectly matched paired module can carry large internal mass flow while having zero net linear momentum in the surrounding structure.

## 3. Spin-up and spin-down symmetry
Take the time derivative of the pair momentum:

$$\dot{\mathbf{p}}_{\mathrm{pair}} = \mu (\dot v_1 - \dot v_2) \, \mathbf{t} + \mu (v_1 - v_2) \, \dot{\mathbf{t}}$$

Under symmetric ramping with matched speeds,

$$v_1 = v_2, \qquad \dot v_1 = \dot v_2$$

we get, to first order,

$$\dot{\mathbf{p}}_{\mathrm{pair}} = 0$$

Interpretation:
- common-mode ramping of the pair does not inject a first-order net linear impulse into the membrane or housing
- differential ramping does

This is an important systems advantage over an unpaired rotor.
It means pressure can be adjusted by ramping both lanes together without the same first-order momentum kick that a single-lane module would impose.

## 4. Local guide force from each lane
For one rotor lane moving through curvature $\kappa = 1/R$, the guide-force density magnitude is

$$f = \mu v^2 \kappa$$

and in vector form

$$\mathbf{f} = \mu v^2 \kappa \, \mathbf{n}$$

where $\mathbf{n}$ is the local principal-normal direction of the rotor path.

For the paired module, if the geometry is arranged so both lanes load the surrounding structure in the same support direction $\mathbf{n}_s$, then the total support-force density is

$$\mathbf{f}_{\mathrm{pair}} = \mu (v_1^2 + v_2^2) \kappa \, \mathbf{n}_s$$

For the symmetric operating point $v_1 = v_2 = v$,

$$\mathbf{f}_{\mathrm{pair}} = 2 \mu v^2 \kappa \, \mathbf{n}_s$$

This is the second key result.
The pair doubles the support-force scale while still allowing zero net momentum when speeds are matched.

## 5. Common-mode and differential-mode decomposition
Define

$$v_c = \frac{v_1 + v_2}{2}, \qquad v_d = \frac{v_1 - v_2}{2}$$

so that

$$v_1 = v_c + v_d, \qquad v_2 = v_c - v_d$$

Then the pair momentum becomes

$$\mathbf{p}_{\mathrm{pair}} = 2 \mu v_d \, \mathbf{t}$$

while the pair support-force density becomes

$$\mathbf{f}_{\mathrm{pair}} = 2 \mu (v_c^2 + v_d^2) \kappa \, \mathbf{n}_s$$

This decomposition is extremely useful.

It says:
- **differential mode** $v_d$ carries the net momentum imbalance
- **common mode** $v_c$ is the clean way to modulate support force

At first order around a balanced operating point with small $v_d$,

$$\mathbf{p}_{\mathrm{pair}} \approx 2 \mu v_d \, \mathbf{t}$$

and

$$\mathbf{f}_{\mathrm{pair}} \approx 2 \mu v_c^2 \kappa \, \mathbf{n}_s$$

with first-order force perturbation under common-mode change $\delta v_c$:

$$\delta \mathbf{f}_{\mathrm{pair}} \approx 4 \mu \kappa v_c \, \delta v_c \, \mathbf{n}_s$$

This is probably the most important control result in the memo.

It means pressure/support modulation and momentum balance are naturally separated:
- use $v_c$ to control pressure
- keep $v_d \approx 0$ to avoid contaminating the structure with net momentum

## 6. Torque balance
Suppose the two lanes are symmetrically placed about the module centerline at offsets

$$\mathbf{r}_1 = +\mathbf{r}, \qquad \mathbf{r}_2 = -\mathbf{r}$$

and both exert the same support-force vector

$$\mathbf{f}_1 = \mathbf{f}_2 = \mu v^2 \kappa \, \mathbf{n}_s$$

Then the net moment density about the module centerline is

$$\boldsymbol{\tau}_{\mathrm{pair}} = \mathbf{r}_1 \times \mathbf{f}_1 + \mathbf{r}_2 \times \mathbf{f}_2 = \mathbf{r} \times \mathbf{f} - \mathbf{r} \times \mathbf{f} = 0$$

So a symmetric pair can provide net support force without introducing a first-order torque on the membrane or local structural bus.

That is exactly the behavior Hudson was aiming for.

## 7. Helical pair on a cylindrical tube
For one helical lane on a tube of radius $a$ and helix angle $\alpha$, the curvature is

$$\kappa = \frac{\sin^2 \alpha}{a}$$

So one lane contributes radial support-force density

$$f_r = \mu v^2 \frac{\sin^2 \alpha}{a}$$

and one lane contributes equivalent average tube pressure

$$p_{\mathrm{lane}} = \frac{\mu v^2 \sin^2 \alpha}{2\pi a^2 \cos \alpha}$$

For one symmetric paired module, the pressure contribution is therefore

$$p_{\mathrm{pair}} = \frac{\mu (v_1^2 + v_2^2) \sin^2 \alpha}{2\pi a^2 \cos \alpha}$$

and at the matched operating point $v_1 = v_2 = v$,

$$p_{\mathrm{pair}} = \frac{2 \mu v^2 \sin^2 \alpha}{2\pi a^2 \cos \alpha}
= \frac{\mu v^2 \sin^2 \alpha}{\pi a^2 \cos \alpha}$$

If there are $N_p$ such paired modules distributed around the tube, the total equivalent pressure is

$$p_{\mathrm{eq}} = N_p \, \frac{\mu (v_1^2 + v_2^2) \sin^2 \alpha}{2\pi a^2 \cos \alpha}$$

and for matched speeds,

$$p_{\mathrm{eq}} = N_p \, \frac{\mu v^2 \sin^2 \alpha}{\pi a^2 \cos \alpha}$$

This is just the earlier helix-pressure model rewritten in the paired-module language.

## 8. Macro-control via common-mode pressure modulation
If the pair is operated near a matched baseline speed $v_0$ and both lanes in a selected region are sped up together by $\delta v$, then the local pressure change is approximately

$$\delta p \approx \frac{2 N_p \mu v_0 \sin^2 \alpha}{\pi a^2 \cos \alpha} \, \delta v$$

Equivalently, because pressure scales as $v^2$,

$$\frac{\delta p}{p_0} \approx 2 \frac{\delta v}{v_0}$$

for small common-mode perturbations.

This is a strong and clean systems result.
It means a relatively modest percentage change in common-mode rotor speed creates about twice that percentage change in local support pressure.

That gives a plausible path to macro-control:
- nominal uniform $v_c(x)$ holds the nominal tube shape
- spatial variation in $v_c(x)$ creates spatial pressure variation
- spatial pressure variation creates long-scale distributed steering loads

The key point is that this can be done while keeping $v_d \approx 0$, so pressure steering need not inject large net linear momentum into the structure.

## 9. What differential mode is for
Because

$$\mathbf{p}_{\mathrm{pair}} = 2 \mu v_d \, \mathbf{t}$$

nonzero differential mode acts like a momentum-imbalance channel.

That suggests:
- for ordinary operation, $v_d$ should be tightly controlled near zero
- persistent nonzero $v_d$ is probably undesirable in the membrane/tube architecture
- transient nonzero $v_d$ may still be useful for diagnostics, balancing, or fault handling, but should be treated cautiously

In other words:
- **common mode** is the natural pressure actuator
- **differential mode** is the natural imbalance variable

## 10. Three bandwidth layers now look cleaner
The paired module strengthens the earlier multiscale control picture.

### Layer 1: Fast local lane control
Goals:
- keep each rotor centered in its lane
- keep the pair matched so $v_d$ stays small
- handle local disturbances and gap control

### Layer 2: Local structural-bus control
Goals:
- modulate $v_c$ across nearby paired modules
- control local pressure and local stiffness
- suppress ovalization and local tube deformation

### Layer 3: Macro-scale shape control
Goals:
- command long-wavelength spatial patterns in $v_c(x)$
- create differential inflation pressure over very long scales
- steer and stabilize a planetary-length tube or ring

This is a better control decomposition than trying to make one loop do everything.

## 11. Important caveats
This memo is first-order and idealized.
It assumes:
- perfect geometric symmetry of the pair
- equal rotor linear density in both lanes
- matched curvature loading direction into the surrounding structure
- negligible coupling losses between the lanes
- no actuator saturation, gap closure, or faulted operation

Real designs will have penalties from:
- mismatch between the two lanes
- sensor and actuation delay
- magnetic cross-coupling between twin stators
- local force ripple
- different loss characteristics during ramping
- asymmetric failure modes

So the clean cancellation results here are design targets, not guarantees.

## 12. Most useful next equations to derive
The next pass should quantify:
1. paired-module spin-up power and transient reaction under realistic motor topology
2. how lane mismatch $\Delta v$, $\Delta \mu$, and geometric asymmetry leak force and torque into the membrane
3. local pressure authority versus common-mode control bandwidth
4. coupled bus dynamics when many paired modules share the same membrane patch
5. long-wavelength steering authority from a prescribed spatial field $v_c(x)$

## 13. Bottom line
The paired module is a real upgrade in how the project should be framed.

At first order, it gives us all of the following at once:
- support force adds through $v_1^2 + v_2^2$
- net momentum cancels through $v_1 - v_2$
- symmetric spin-up and spin-down can avoid a first-order momentum kick
- common-mode speed becomes the natural pressure-control channel
- differential mode becomes the natural imbalance variable

My current judgment is:
- the paired rotor module is a much better base element than the single rotor
- it gives the project a cleaner local-to-global control architecture
- the next worthwhile step is to turn this memo into a reduced-order dynamic control model with explicit common-mode and differential-mode states
