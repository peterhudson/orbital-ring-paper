# Helical Slug Streams in an Inflated Fabric Torus: A Control-Capable Architecture for Active-Support Orbital Rings

## Abstract

This paper proposes an orbital-ring architecture built from magnetically guided high-speed slug streams running in small-helix-angle lanes around a very large lightweight fabric torus. The paper's main claim is not that such a ring is presently practical. It is that this architecture introduces two linked ideas that are genuinely useful at the concept level.

The first is that helical slug streams can do more than circulate momentum. By forcing the streams to follow curved helical paths on a large toroidal membrane, the design converts momentum redirection into distributed outward pressure, hoop prestress, and local structural rigidity. The result is not a passive rigid pipe. It is a prestressed active membrane structure, more like a giant fabric sock or fabric torus wrapped around the world, whose local stiffness is created by internal moving mass.

The second is that the same helical geometry enables a four-lane balanced cell that can generate distributed tug fields for macro-scale control of the orbital ring. In a fixed spatial speed gradient, one counter-propagating lane accelerates while its mirrored partner decelerates. Their structural reactions add, and the station exchanges power between the two streams. That makes the control system a momentum-flux actuator and a high-power energy exchanger at the same time.

A central motivation for this architecture is that simple straight-lane or monolithic-rotor orbital-ring concepts are not passively stable under curvature perturbations. A fast mass stream pushes into existing curvature. Without a surrounding structure and active control system that can react against that tendency, perturbations are anti-restored rather than damped away. The helical fabric-torus architecture is therefore not cosmetic. It supplies a reaction substrate and a prestress mechanism that such a control system can work through, even though it does not by itself prove local dynamic stability.

After presenting the force mechanism, lane-level guide requirements, perturbation argument, helical membrane architecture, and four-lane macro-control scheme, the paper turns to feasibility screens. Those screens remain severe. Full-scale macro lift requires superorbital ring-tangential momentum flux, failures are energetically extreme, and losses, thermal rejection, and containment all feed back into passive structural weight. The architecture should therefore be understood as a new way to make an orbital ring controllable and structurally legible in principle, not as evidence that an orbital ring is easy.

---

## 1. Introduction

The usual picture of an orbital ring is seductively simple: put a very fast moving mass around Earth, let curvature redirect momentum, and use the resulting reaction force to support a ring. But that picture leaves out two problems that are not secondary.

First, a fast moving mass stream is not passively self-stabilizing. If its path develops a curvature perturbation, the stream pushes further into that curvature. A simple straight lane or monolithic rotor therefore does not merely need support force. It needs a surrounding architecture that can resist and control a fundamentally anti-restoring tendency.

Second, even if one has enough moving momentum to loft a ring, that does not by itself provide a good mechanism for local structural rigidity or macro-scale alignment control. A ring around Earth has to survive construction tolerances, tether loads, payload impulses, gravity-gradient effects, and long-wavelength wobble. A concept that only says "there is a rotor going around the planet" has not yet explained how the machine is to be controlled.

This paper proposes a specific answer to both problems.

1. **Helical small-\(\alpha\) slug streams in a lightweight fabric torus.** The lanes are wrapped helically around a very large tensile membrane tube. Their curvature creates outward pressure that inflates and prestresses the torus, turning moving momentum into local structural stiffness.
2. **A four-lane balanced cell for macro-scale control.** The same helical geometry allows balanced groups of lanes whose momentum components cancel in steady operation but can be modulated through fixed spatial speed gradients to produce distributed tug fields and ring-scale bending moments.

Those are the two main novelties of the paper.

The cleanest way to say the thesis is this:

> Earth-scale curvature supplies macro lift, tube-scale helical curvature supplies local membrane prestress, and controlled spatial gradients in lane momentum flux supply macro-shape actuation. A four-lane balanced cell allows those three functions to coexist while cancelling first-order steady momentum and torque channels.

### 1.1 Coordinate convention

To avoid ambiguity, the paper uses three local coordinates:

\[
s = \text{distance along the ring centerline around Earth}
\]

\[
\theta = \text{azimuth around the torus cross-section}
\]

\[
r = \text{local radial direction normal to the torus cross-section}
\]

In the local tube approximation, what earlier orbital-ring discussions often call "axial" means the \(s\) direction, not the global Earth rotation axis. The helical lanes wind in \(\theta\) while moving mainly along \(s\).

**Suggested Figure 1. Overall concept sketch.** Show a world-encircling torus with roughly 100 m diameter, rendered as a lightweight fabric membrane rather than a solid pipe. Include a local cutaway showing several shallow-angle helical lanes attached to the membrane and one enlarged inset showing a four-lane balanced cell. The image should make the paper's core claim visible in one glance: the same helical lane system gives both local prestress and macro-control authority.

The argument proceeds in six steps. First, momentum redirection is established as the basic force mechanism. Second, the paper asks what one lane demands from its magnetic guide. Third, it shows why a straight high-speed lane is not passively stable under perturbation. Fourth, it introduces the helical fabric-torus architecture as a way to turn the dominant steady curvature load into useful local prestress while making the remaining stability problem explicit. Fifth, it develops the four-lane balanced cell and distributed tug fields as the main macro-control result. Only then does it turn to the harder practicality screens: macro lift throughput, atmospheric environment, fault-domain architecture, and closure.

---

## 2. Momentum redirection is the force mechanism

Consider a mass stream moving at speed \(v\) along a guide path of curvature \(\kappa\). The stream requires normal acceleration

\[
a_n = v^2\kappa.
\]

For a continuous stream of line density \(\mu\), the required guide force per unit path length is

\[
f = \mu v^2\kappa.
\]

For a discrete slug train with fixed mass flux \(\dot m\), the effective line density is \(\mu_\mathrm{eff}=\dot m/v\), so the corresponding force law becomes

\[
f = \dot m v\kappa.
\]

That distinction matters. A continuously filled cable-like stream at fixed line density scales as \(v^2\). A throughput-limited slug train whose spacing changes with speed scales as \(v\).

The physical interpretation is straightforward. The guide pushes the stream onto a curved path. The stream pushes back on the guide with equal and opposite force. This is the structural force source. No speculative physics is required.

It is often convenient to introduce an equivalent dynamic-tension scale

\[
T_\mathrm{eq} = \mu v^2
\]

for the continuous case, or equivalently \(T_\mathrm{eq}=\dot m v\) for the fixed-flux slug-train case. That notation is useful, but it must not be over-read. In this architecture the support force does not require a passive material hoop carrying literal mechanical tension equal to \(T_\mathrm{eq}\). The force can instead arise from guided momentum redirection in discrete moving masses.

At this early stage it is worth previewing an organizing distinction that becomes central later. The paper is not claiming that local helical inflation replaces orbital support. The two curvature channels do different jobs:

- **tube-scale helical curvature** supplies local prestress in the membrane torus,
- **Earth-scale ring curvature** supplies macro lift.

For one lane with ring-centerline speed component \(u=v\cos\alpha\), the Earth-scale lift channel is

\[
q_{\mathrm{lift,lane}} = \dot m\left(\frac{u}{R} - \frac{g_h}{u}\right)
\]

where \(R\) is ring radius and \(g_h\) is gravity at altitude. At this point it is enough to note that local helix curvature and Earth-scale curvature are separate channels and must not be conflated.

**Suggested Figure 2. Momentum-redirection force law.** Draw one curved guide segment with slugs moving along it. Show the tangent velocity, the local radius of curvature, the inward guide force on the slug, and the equal outward reaction on the guide. Include both labels \(f=\mu v^2\kappa\) and \(f=\dot m v\kappa\) so the reader sees immediately that the same geometry applies to continuous and discrete pictures.

---

## 3. What one lane requires from its guide

Before discussing orbital-ring architecture, it is worth asking what one lane demands from its stator.

### 3.1 Magnetic reaction scale

A rough upper bound on magnetic normal stress is

\[
p_\mathrm{mag,max} \sim \frac{B^2}{2\mu_0},
\]

where \(B\) is field strength and \(\mu_0\) is the permeability of free space. Ideal field-pressure scales are therefore on the order of 0.10 MPa at 0.5 T, 0.40 MPa at 1 T, 1.59 MPa at 2 T, and 3.58 MPa at 3 T. Real delivered traction will be lower because of gap, fringing, force margin, thermal limits, imperfect field topology, and control requirements.

If \(A'\) is effective magnetic interaction area per unit lane length, then the required mean traction is

\[
p_\mathrm{req} = \frac{f}{A'}.
\]

For a fixed-flux slug lane this becomes

\[
p_\mathrm{req} = \frac{\dot m v\kappa}{A'}.
\]

So tight curvature, high speed, and small interaction perimeter all make the lane harder to guide.

### 3.2 Convective local control

A lane is not merely static curvature plus average force. The stream is convected through the guide at high speed, so disturbances arrive on a timescale

\[
t_\mathrm{conv} \sim \frac{\lambda}{v},
\]

where \(\lambda\) is disturbance wavelength. At \(v=10\,\mathrm{km/s}\), a 100 m disturbance convects past in 10 ms, a 10 m disturbance in 1 ms, and a 1 m disturbance in 0.1 ms. High speed helps force generation and hurts control.

Using lateral displacement \(y(x,t)\) along a lane coordinate \(x\), the convective derivative is

\[
\frac{D}{Dt} = \frac{\partial}{\partial t} + v\frac{\partial}{\partial x},
\]

so the lateral acceleration contains

\[
\frac{D^2y}{Dt^2} = y_{tt} + 2v y_{xt} + v^2 y_{xx}.
\]

The last term is the same curvature-following term that generates support force. The middle term is transport coupling. Both must be handled by the guide.

A credible architecture therefore needs layered control:

- very fast local gap control at the lane level,
- bus-level coordination of nearby lanes and sectors,
- and slower macro-shape control at the ring scale.

The orbital ring cannot be treated as a single centralized control loop.

**Suggested Figure 3. One lane as a guided control problem.** Show a single lane with magnetic stator modules, guide gap, slug train, sensors, and fast local controllers. Include a disturbance entering from the left and being convected downstream. The figure should make it obvious that the lane problem is distributed and time-critical, not a quasi-static guideway.

---

## 4. Why straight lanes and monolithic rotors are not passively stable

This is the missing structural argument in many simple orbital-ring pictures.

Consider a nominally straight lane or monolithic rotor segment with a small transverse deflection \(y(x,t)\). For small slope, the centerline curvature is approximately

\[
\kappa \approx y_{xx}.
\]

The moving stream must then be forced to follow that curved path. The stream exerts on the guide a reaction load per unit length of the form

\[
q_\mathrm{stream} \approx -T_\mathrm{eq} y_{xx},
\]

where \(T_\mathrm{eq}=\mu v^2\) or \(T_\mathrm{eq}=\dot m v\), depending on whether one uses the continuous or fixed-flux picture.

Now consider a sinusoidal perturbation,

\[
y(x,t) = Y\sin(kx).
\]

Then

\[
y_{xx} = -k^2 y,
\]

so the stream reaction becomes

\[
q_\mathrm{stream} = +T_\mathrm{eq} k^2 y.
\]

That has the **same sign as the displacement**. If the lane is displaced upward at some point, the stream pushes upward there as well. The moving mass therefore pushes further into an existing curvature perturbation rather than restoring the lane to straightness.

This is not yet a complete stability model. Real dynamics also involve beam stiffness, membrane stiffness, damping, actuator delay, and control law. But it is enough to establish the key point: a straight high-speed lane is not passively self-centering. The moving stream behaves like an anti-restoring curvature follower unless the surrounding structure and controls provide compensating reaction.

That observation cuts directly against naive pictures of a single giant monolithic rotor or a set of parallel straight rotors simply going around Earth. Such concepts may contain enough momentum to generate support in principle, but they do not automatically contain a good structural answer to perturbations.

**Suggested Figure 4. Anti-restoring behavior of a perturbed straight lane.** Show a nominally straight lane with a small sinusoidal bend. Draw the local curvature and the stream reaction arrows pushing into the bend rather than away from it. Under the drawing, show the short derivation \(q_\mathrm{stream}\approx -T_\mathrm{eq}y_{xx}\rightarrow +T_\mathrm{eq}k^2y\). This figure should be the moment where the reader understands why a simple straight rotor picture is incomplete.

---

## 5. Helical lanes in a lightweight fabric torus

The helical fabric-torus architecture is the first major payoff of the paper.

Instead of asking a fast lane to remain straight in free space, the architecture places the lane on an intentionally curved helical path wrapped around a very large tensile membrane tube. The tube should be imagined as a lightweight fabric torus, likely made from a high-tensile membrane family rather than a heavy rigid shell. "Fabric sock around the world" is crude language, but it is not the wrong mental image.

### 5.1 Helical curvature creates a steady prestress channel

For a helix on a cylinder of radius \(a\), with helix angle \(\alpha\) measured relative to the local \(s\) direction,

\[
\kappa_\mathrm{helix} = \frac{\sin^2\alpha}{a}
\]

in the local-cylinder approximation.

That curvature is not an accident. It is the local mechanism that converts moving momentum into distributed outward reaction on the membrane-supported lane system.

For a fixed-flux slug lane, the local outward load per unit ring length is

\[
q_\mathrm{loc,lane} = \dot m u \frac{\tan^2\alpha}{a}
\]

where

\[
u = v\cos\alpha
\]

is the ring-centerline speed component.

For one symmetric pair of lanes,

\[
q_\mathrm{loc,pair} = 2\dot m u \frac{\tan^2\alpha}{a}
\]

and, if those loads are azimuthally smoothed, the corresponding equivalent pressure from one pair is

\[
p_\mathrm{pair} = \frac{\dot m u \tan^2\alpha}{\pi a^2}.
\]

For \(N_p\) paired modules distributed around the torus,

\[
p_\mathrm{eq} = \frac{N_p \dot m u \tan^2\alpha}{\pi a^2}.
\]

So the helical lanes create a steady outward load channel that can inflate the torus and prestress its membrane.

### 5.2 Equivalent pressure is an averaged load model

The pressure language is useful, but it is an azimuthally averaged approximation. The real loads are applied through discrete lanes, ribs, or lane carriers.

The averaging is only justified when lane pitch, rib stiffness, and membrane shear transfer are fine enough that the discrete loads appear smooth at the wavelengths of interest. At \(a=50\,\mathrm{m}\), the circumference is about

\[
2\pi a \approx 314\,\mathrm{m}.
\]

If the torus carries on the order of 300 lanes, the pitch is about 1 m and a pressure-like description may be reasonable for long-wave structural modes. If it carries only a few tens of lanes, the loading is much less pressure-like and the discrete rib-and-membrane mechanics become first-order.

Equivalent pressure should therefore be read as a useful homogenized model, not as proof that the membrane literally feels a perfectly smooth gas-like pressure field.

### 5.3 Prestress creates a reaction substrate, not automatic stability

Equivalent pressure \(p_\mathrm{eq}\) creates hoop membrane force per unit axial length

\[
N_\theta = p_\mathrm{eq} a.
\]

This prestress plausibly helps with:

- maintaining circular cross-section,
- resisting ovalization,
- suppressing wrinkling in a membrane wall,
- increasing local indentation stiffness,
- and providing a stable substrate onto which guides, sensors, power hardware, and auxiliary structure can be mounted.

That is the architectural move. The imposed helical curvature converts the dominant **steady** curvature load into useful membrane prestress.

But that does not by itself prove local dynamic stability. Perturbations about the helical path still have follower-force character. The moving stream still carries an effective dynamic-tension scale \(T_\mathrm{eq} \sim \dot m v\), and displaced lane segments can still generate incremental curvature-following loads unless the membrane, guide, and controller supply enough incremental stiffness and damping.

A useful screening inequality is therefore

\[
K_\mathrm{membrane} + K_\mathrm{guide} + K_\mathrm{control} > K_\mathrm{stream}
\]

and, for a sinusoidal perturbation of wavenumber \(k\), a more explicit version is

\[
N_\mathrm{eff} k^2 + K_\mathrm{guide}(k,\omega) > T_\mathrm{eq} k^2
\]

with the understanding that damping and phase margin matter as much as static stiffness.

Put differently, the torus gives the lane something real to push against. It does not let the paper claim that the instability problem has disappeared.

Lanes could in principle be mounted on the inner or outer surface of the membrane, or on shallow truss or rib hardware attached directly to it. The point is not the exact attachment detail at this stage. The point is that the prestressed membrane becomes the structural reaction surface for the helical lanes.

**Suggested Figure 5. Helical lane inflating a fabric torus.** Draw a cutaway of the torus wall with shallow-angle helical lanes attached to it. Show the lane reaction pressing outward, the membrane carrying hoop tension, and secondary hardware mounted to the now-prestressed wall. Add a second overlay showing a small perturbation about the nominal helical path, with labels indicating that the steady load becomes prestress but incremental stability still depends on membrane stiffness, guide stiffness, and active damping.

### 5.4 Why the helix angle is likely small

The architecture wants helical curvature for local prestress, but it also wants most of the speed to remain ring-tangential so the orbital ring can loft itself. That trade pushes the design toward shallow helical angles.

Define the paired-module momentum-flux scale

\[
A_\mathrm{pair} = N_p \dot m u.
\]

The total paired-lane contribution is then \(2A_\mathrm{pair}\).

The inflation requirement can be written as

\[
A_\mathrm{pair} \ge \frac{\pi a N_{\theta,\mathrm{req}}}{\tan^2\alpha}
\]

where \(N_{\theta,\mathrm{req}}\) is required hoop membrane force per unit length.

The macro-lift requirement, derived later, is

\[
A_\mathrm{pair} \ge \frac{w_p}{2\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}.
\]

Balancing the two gives a useful screening estimate

\[
\tan^2\alpha_\mathrm{opt} = 2\pi a\Gamma\left(\frac{1}{R} - \frac{g_h}{u^2}\right)
\]

with

\[
\Gamma = \frac{N_{\theta,\mathrm{req}}}{w_p}.
\]

For small angles,

\[
\alpha_\mathrm{opt} \approx \sqrt{2\pi a\Gamma\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}.
\]

Using a screening case with \(a=50\,\mathrm{m}\), altitude 80 km, \(u=10\,\mathrm{km/s}\), and \(\Gamma=10\), one gets

\[
\alpha_\mathrm{opt} \approx 0.78^\circ.
\]

That is a striking result. Once macro lift matters, the optimal helical bias may be very small. This supports exactly the picture advocated here: a large torus with many shallow-angle helical lanes, not a steeply wrapped screw conveyor.

### 5.5 What the inflated torus does and does not solve

The inflated fabric torus solves an important local problem. It gives the lanes a reaction structure, creates local prestress, and provides a platform for hardware.

It does **not** automatically create a globally rigid torus, and it does **not** by itself close the local stability problem. A 100 m diameter prestressed membrane can be locally round and still be very flexible at long wavelength, while local perturbations can still go unstable if the incremental guide-and-membrane stiffness is inadequate.

That is why the orbital ring still requires active macro-control, and why the four-lane balanced cell becomes essential.

---

## 6. The four-lane balanced cell

A simple mirrored pair is useful, but it is not enough for a helical architecture.

If one chooses a mirrored helical pair with tangent vectors

\[
t_x = \cos\alpha\,e_z + \sin\alpha\,e_\theta,
\]

\[
t_y = -\cos\alpha\,e_z + \sin\alpha\,e_\theta,
\]

then the axial components cancel, but the circumferential components add. That means a two-lane pair can still carry steady circumferential momentum and angular momentum around the torus.

The minimal balanced cell therefore contains four lanes:

1. right-handed helix, positive axial travel,
2. left-handed helix, negative axial travel,
3. left-handed helix, positive axial travel,
4. right-handed helix, negative axial travel.

Operated together, this cell can cancel to first order:

- net axial momentum,
- net circumferential momentum,
- net angular momentum about the torus,
- and first-order structural torque in symmetric operation.

At the same time it preserves:

- common-mode inflation pressure,
- controllable pressure trim,
- axial or tangential tug authority,
- and azimuthally selective moment generation.

This is not a decorative symmetry argument. It is the architecture that makes the helical torus usable as a control machine rather than merely a pressurized tube.

**Suggested Figure 6. Four-lane balanced cell.** Show the four lane helices in cross-section and in a short perspective cutaway, with arrows labeling handedness and travel direction. Use color-coded momentum vectors to show cancellation of axial, circumferential, and angular components. Then indicate the common-mode pressure channel that remains. The figure should make the cell feel like a genuine machine primitive.

---

## 7. Local rigidity is not global rigidity

At this point the architecture has solved an important local problem. The helical lanes can inflate and prestress the fabric torus, and the four-lane cell can remove hidden steady momentum and torque channels.

But a locally stiff torus is not yet a globally well-aligned orbital ring.

A 100 m diameter prestressed membrane can still be flexible at long wavelength. The ring still has to respond to tether loads, payload-launch impulses, gravity-gradient effects, construction asymmetries, and wobble modes. So the next question is the decisive one: can the helical lane architecture produce a real macro-scale control channel?

That is the paper's main result.

---

## 8. Distributed tug fields and macro-scale ring control

This is the second major payoff of the architecture, and arguably the main result of the paper.

The inflated torus makes a locally stiff substrate. The four-lane balanced cell makes that substrate actively controllable at long wavelength.

### 8.1 Stationary spatial speed gradients act on momentum flux

The quantity being controlled is momentum flux along the ring centerline direction \(s\).

Let one lane in a balanced cell have signed centerline speed

\[
V_s(s) = \sigma u(s)
\]

with \(\sigma = \pm 1\) for the two travel directions. Here \(u=v\cos\alpha\) is the scalar ring-centerline speed component.

For a stationary speed field, the convective acceleration along \(s\) is

\[
a_s = V_s \frac{dV_s}{ds} = u \frac{du}{ds}.
\]

The key point is that \(a_s\) is independent of \(\sigma\). A fixed spatial speed gradient acts the same way on counter-propagating lanes when projected onto the stationary structure.

For one lane with scalar mass flux \(\dot m\), the structural force per unit ring length is therefore

\[
q_{s,\mathrm{lane}} = -\dot m \frac{du}{ds}.
\]

If \(\alpha\) is locally constant so that \(u=v\cos\alpha\), this may also be written as

\[
q_{s,\mathrm{lane}} = -\dot m \cos\alpha \frac{dv}{ds}.
\]

That is the basic tug-field law.

### 8.2 Why counter-propagating lanes add instead of canceling

Now consider a mirrored pair in the same fixed spatial speed gradient. If \(du/ds>0\), the \(+s\)-traveling lane accelerates through the section while the counter-propagating lane decelerates through the same section. Yet their structural force densities are the same, because both are governed by the same stationary gradient law above.

So for one mirrored pair,

\[
q_{s,\mathrm{pair}} = -2\dot m \frac{du}{ds}.
\]

This is the real reason the pair adds instead of cancels. It is not that both lanes slow down in their own direction of travel. It is that a fixed spatial speed gradient produces the same structural reaction for both travel directions.

Integrating across a control section from \(u_1\) to \(u_2\) gives

\[
F_{\mathrm{pair}} = -2\dot m (u_2-u_1).
\]

For \(N_s\) participating paired modules in one azimuthal sector,

\[
F_{\mathrm{sector}} = -2N_s\dot m (u_2-u_1).
\]

If one only needs the magnitude, this becomes

\[
|F_{\mathrm{sector}}| = 2N_s\dot m |\Delta u|.
\]

For constant \(\alpha\), \(|\Delta u| = \cos\alpha\,|\Delta v|\).

**Suggested Figure 7. Why the pair adds instead of cancels.** Draw two mirrored counter-moving lanes passing through the same stationary speed-gradient section from opposite directions. Show one lane accelerating and the other decelerating, while the structural reaction arrows point the same way. The figure should make clear that the common sign comes from the fixed spatial gradient, not from two same-direction braking events.

### 8.3 Distributed tug fields

The control section need not be a hard boundary. In fact, a distributed transition is usually better because it lowers peak local force density.

For one mirrored pair,

\[
q_{s,\mathrm{pair}}(s) = -2\dot m \frac{du}{ds}.
\]

For \(N_s\) participating paired modules,

\[
q_{s,\mathrm{sector}}(s) = -2N_s\dot m \frac{du}{ds}.
\]

Integrating over the transition width gives

\[
F_{\mathrm{sector}} = \int q_{s,\mathrm{sector}}(s)\,ds = -2N_s\dot m \Delta u.
\]

So a distributed tug field preserves the same integrated authority as a hard transition while spreading the load over a useful finite distance.

### 8.4 Why fill and drain are not required

The remaining concern is whether such speed modulation requires literal insertion and removal of slugs at every ordinary control section. For the architecture considered here, the answer is no.

Let slug number flux be \(J\), so that

\[
\dot m = J m_s
\]

where \(m_s\) is mass per slug. In steady flow through a lane with local speed \(v(s)\), number continuity gives

\[
n(s) = \frac{J}{v(s)}
\]

where \(n(s)\) is slug number density along the lane. Equivalently, if \(h=1/J\) is time headway, then the center-to-center spacing in a locally uniform region is

\[
s(s) = \frac{1}{n(s)} = v(s)h.
\]

So a region with lower speed automatically compresses spacing and raises local occupancy, while a region with higher speed automatically expands spacing and lowers it. No source term is required. The lane stores more or less slug inventory simply because the same flux is moving more slowly or more quickly through that region.

That is the clean kinematic reason why ordinary tug fields do not require fill-and-drain hardware.

The main constraints are instead collision and delay limits. For a monotone low-speed region with minimum speed \(v_1\), the minimum spacing becomes

\[
s_\mathrm{min} = h v_1
\]

so collision avoidance requires

\[
h v_1 \ge \ell_s + g_\mathrm{min}
\]

where \(\ell_s\) is slug length and \(g_\mathrm{min}\) is the minimum allowable gap.

For an upward ramp, incomplete actuation can let a trailing slug catch a slower incumbent. A useful first delay bound is

\[
\tau_d < \frac{h v_0 - (\ell_s + g_\mathrm{min})}{v_1-v_0}
\]

where \(\tau_d\) is total sensing, computation, actuation, and field-establishment delay.

So the issue is not that mass must be added or removed in ordinary control sections. The issue is that the speed profile has to respect spacing and delay constraints.

**Suggested Figure 8. Distributed tug field without fill and drain.** Show a low-speed region in which slug spacing compresses smoothly as slugs enter, followed by a higher-speed region where spacing re-expands. Label \(n=J/v\) and \(s=vh\). The figure should make clear that local occupancy changes because transport speed changes, not because slugs are literally injected or removed inside the control section.

### 8.5 The tug actuator is also a high-power energy exchanger

The tug equations are momentum-flux equations, but a reviewer will immediately ask about power, and rightly so.

For one lane, the power transferred into or out of the stream by a speed change is approximately

\[
P_{\mathrm{lane}} \approx \dot m u \, \Delta u.
\]

Using the force magnitude \(|F_{\mathrm{lane}}| = \dot m |\Delta u|\), this is

\[
P_{\mathrm{lane}} \approx |F_{\mathrm{lane}}| \, u.
\]

At \(u \sim 10\,\mathrm{km/s}\), even modest structural tug implies enormous power exchange. A 1 MN tug at 10 km/s corresponds to roughly 10 GW.

That does not by itself kill the architecture, because a mirrored pair in a fixed gradient can ideally exchange energy locally: one lane is accelerated while the other is decelerated. But it does mean the tug-field actuator is not a gentle trim system. It is a very high-power bidirectional momentum-and-energy exchanger.

Any serious realization would therefore require bidirectional power electronics, local energy buffering, phase-managed transfer between accelerating and decelerating lanes, and heat rejection for conversion losses.

### 8.6 Opposed sectors create bending moments

Now place such tug fields in opposed azimuthal sectors of a torus of radius \(a\). Then the sector tugs form a couple.

At the level of order of magnitude,

\[
M \sim 2a |F_{\mathrm{sector}}|.
\]

A more explicit finite-sector estimate is

\[
M_{\mathrm{pair}} = 4aN_s\dot m |\Delta u|\,C_\mathrm{sec}(\Delta\phi)
\]

with

\[
C_\mathrm{sec}(\Delta\phi) = \frac{\sin(\Delta\phi/2)}{\Delta\phi/2}
\]

where \(\Delta\phi\) is sector width and \(C_\mathrm{sec}\) accounts for finite angular extent.

This is the macro-control mechanism. It turns distributed speed modulation in balanced helical lanes into a real bending moment on the torus.

### 8.7 Global bookkeeping and compensating zones

The ring is not creating net momentum from nowhere. A tugging sector must be paired with other sectors or stations that close the momentum and energy bookkeeping.

What the architecture offers is not free net force. It offers a way to **redistribute** momentum flux and the associated structural reaction in space. That is exactly what a shape-control system needs.

The important result is that this redistribution can be accomplished internally, in balanced four-lane cells, by smooth spatial speed fields. One does not need monolithic moving hoops or routine fill-and-drain hardware throughout the ring to generate useful macro moments.

### 8.8 What this control channel is for

The point is not only to suppress abstract wobble. The same mechanism is the natural candidate for handling:

- long-wavelength orbital-ring alignment,
- tether loads,
- payload-launch impulses,
- construction asymmetries,
- thermal distortion,
- and other slow or moderate disturbances that act on the ring at large scale.

A useful way to say it is this: the helical lanes pay twice. First they inflate and prestress the torus. Then, because they are grouped into balanced cells, they provide a distributed internal actuation system for macro-scale shape control.

**Suggested Figure 9. Opposed tug sectors generating a ring-scale moment.** Show a torus cross-section with two opposed azimuthal sectors highlighted, each containing distributed speed-gradient zones in the participating lanes. Draw the resulting axial tug vectors and the net bending couple. Add a second panel showing the same mechanism acting on a long orbital-ring arc to oppose a tether load or wobble mode.

---

## 9. What this architecture still does not solve automatically

The paper's claim is architectural novelty, not practical closure. Several severe screens remain.

### 9.1 Macro lift is still a separate burden

The helical torus gives local prestress. It does not, by itself, loft the entire ring around Earth. Macro lift comes from turning the ring-tangential component of stream momentum around Earth.

Let \(u=v\cos\alpha\) be ring-tangential speed and let the ring radius be \(R\). For one slug lane with mass flux \(\dot m\), the net outward lift per unit ring length is

\[
q_\mathrm{lift,lane} = \dot m\left(\frac{u}{R} - \frac{g_h}{u}\right),
\]

where \(g_h\) is gravity at altitude.

For \(N_p\) paired modules,

\[
q_\mathrm{lift} = 2N_p\dot m\left(\frac{u}{R} - \frac{g_h}{u}\right).
\]

The lift changes sign at

\[
u_\mathrm{orb} = \sqrt{g_hR}.
\]

If \(u<u_\mathrm{orb}\), the moving stream loads the ring downward overall. Only for \(u>u_\mathrm{orb}\) does it contribute net outward lift.

This is why the helical angle has to stay small at full scale. The ring needs its speed mostly in the ring-tangential direction.

### 9.2 The full system faces a closure loop

Let passive structural and hardware weight per unit ring length be \(w_p\). The lift requirement can be written as

\[
A_\mathrm{pair} = N_p \dot m \, u \ge \frac{w_p}{2\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}
\]

where \(A_\mathrm{pair}\) is the paired-module momentum-flux scale and the total paired-lane contribution is \(2A_\mathrm{pair}\).

That sounds like a simple scaling law, but it closes several hard subsystems into one loop:

\[
w_p \to A_\mathrm{pair} \to \left(E_{\mathrm{kin}},\; P_{\mathrm{loss}}\right) \to \left(w_{\mathrm{contain}},\; w_{\mathrm{thermal}},\; w_{\mathrm{power}}\right) \to w_p
\]

In words:

1. more passive hardware raises ring weight,
2. more weight requires more momentum flux,
3. more momentum flux raises stored energy per metre and usually raises losses,
4. those burdens demand more containment, thermal hardware, and power infrastructure,
5. which raises ring weight again.

The concept stands or falls on whether this loop converges.

### 9.3 The 80 km screening case has a serious environment caveat

The 80 km altitude used in the screening case is not ordinary dense atmosphere, but it is not clean vacuum either. A 40,000 km class stationary structure at roughly that altitude would face atmospheric interaction, drag variability, upper-atmosphere heating, atomic-oxygen or reactive-species exposure, materials degradation, and possibly large station-keeping loads.

The present paper does not close that environment problem. The 80 km case should therefore be read only as a geometric and momentum-flux screening case, not as a settled operating altitude.

### 9.4 Fault domains still need an explicit architecture

The helical fabric torus should not be interpreted as a containment solution by itself. Any serious version of the architecture would still require physical segmentation into independently isolated sectors, energy-isolating gates, sacrificial catchers, controlled dump paths, distributed braking, and faulted-section bypass.

This paper does not develop that system in detail, but it must be named explicitly because the moving-energy scale is far too large for containment to be left implicit.

**Suggested Figure 10. Macro-lift versus local-control separation.** Show a large Earth-centered orbital ring with one local inset. In the large view, highlight the ring-tangential momentum component responsible for macro lift. In the inset, highlight the shallow helical lanes and opposed-sector tug fields responsible for local prestress and macro-shape control. The figure should remind the reader that this paper mainly solves a control architecture, not the entire full-scale closure problem.

---

## 10. Conclusion

This paper argues for a specific architectural idea, not for immediate engineering closure.

The first key idea is that shallow-angle helical slug streams in a lightweight fabric torus can convert momentum redirection into distributed inflation pressure and hoop prestress. That provides a way to make a huge membrane tube locally stiff enough to serve as the structural substrate for its own guide hardware, while stopping short of claiming that prestress by itself proves local dynamic stability.

The second key idea is that the same helical geometry enables a four-lane balanced cell whose lanes can be modulated to produce distributed tug fields for macro-scale orbital-ring control. That gives the ring an internal actuation system for alignment, wobble suppression, tether-load management, and useful work, while preserving first-order momentum balance.

Those two ideas belong together. The inflated torus without the balanced control cell is only a locally stiff membrane. The balanced control cell without the toroidal prestressed substrate lacks a good structural medium through which to act. Together they form a coherent architecture.

A major motivation for this architecture is that straight high-speed lanes and simple monolithic rotors are not passively self-stabilizing under curvature perturbation. The stream pushes into existing curvature. The helical fabric torus is therefore not merely a convenient geometry. It is a way to supply the reaction structure and control channels that a viable ring would need anyway.

The main control result can be stated compactly. A stationary spatial speed gradient changes lane momentum flux. In a mirrored counter-moving pair, one lane accelerates while the other decelerates through the same fixed section, yet their structural reactions add rather than cancel. In a four-lane balanced cell, those pairwise tug fields can be placed in opposed sectors to generate controlled ring-scale moments while maintaining first-order steady momentum balance. That is the paper's strongest claim.

That does not make the full orbital ring easy. Macro lift still demands superorbital ring-tangential momentum flux, and the full closure problem remains severe. The honest conclusion is therefore two-sided.

- As a **control-capable architecture**, this concept is substantially stronger than a simple rotor-around-Earth picture.
- As a **practical megastructure**, it still faces severe closure problems.

That is a useful result. Even if the full orbital ring proves too hard, the paper identifies a new family of active-support structures in which moving momentum, tensile membranes, and distributed control are tightly integrated.
