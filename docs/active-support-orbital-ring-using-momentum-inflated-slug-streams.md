# Helical Slug Streams in an Inflated Fabric Torus: A Control-Capable Architecture for Active-Support Orbital Rings

## Abstract

This paper proposes an orbital-ring architecture built from magnetically guided high-speed slug streams running in small-helix-angle lanes around a very large lightweight toroidal guide structure. The paper's main claim is that this architecture introduces two linked ideas that are genuinely useful at the concept level.

The first is that helical slug streams can do more than circulate momentum. By forcing the streams to follow curved helical paths on a large toroidal membrane, the design converts momentum redirection into distributed outward pressure, hoop prestress, and local structural rigidity. The result is best understood as a prestressed membrane guide shell, intuitively a giant fabric torus, whose local stiffness is created by internal moving mass.

The second is that the same helical geometry enables a four-lane balanced cell that can generate distributed tug fields for macro-scale control of the orbital ring. In a fixed spatial speed gradient, one counter-propagating lane accelerates while its mirrored partner decelerates. Their structural reactions add, and a co-located bidirectional power path can exchange power between the two streams. That makes the control system a momentum-flux actuator and a high-power energy exchanger at the same time.

A central motivation for this architecture is that simple straight-lane or monolithic-rotor orbital-ring concepts do not provide passive self-centering by momentum redirection alone. A fast mass stream pushes into existing curvature. Without a surrounding structure and active control system that can react against that tendency, perturbations are anti-restored rather than damped away. The helical toroidal guide architecture is therefore not cosmetic. It supplies the reaction substrate and prestress channel that the control system can work through.

After presenting the force mechanism, lane-level guide requirements, perturbation argument, helical membrane architecture, and four-lane macro-control scheme, the paper turns to feasibility screens. Full-scale macro lift requires superorbital ring-tangential momentum flux, failures are energetically extreme, and losses, thermal rejection, and containment all feed back into passive structural weight. The architecture should therefore be understood as a new way to make an orbital ring controllable and structurally legible in principle.

---

## 1. Introduction

The usual picture of an orbital ring is seductively simple: put a very fast moving mass around Earth, let curvature redirect momentum, and use the resulting reaction force to support a ring. But that picture leaves out two problems that are not secondary.

First, a fast moving mass stream does not provide passive self-centering by momentum redirection alone. If its path develops a curvature perturbation, the stream pushes further into that curvature. A simple straight lane or monolithic rotor therefore does not merely need support force. It needs a surrounding architecture that can resist and control a fundamentally anti-restoring tendency.

Second, even if one has enough moving momentum to loft a ring, that does not by itself provide a good mechanism for local structural rigidity or macro-scale alignment control. A ring around Earth has to survive construction tolerances, tether loads, payload impulses, gravity-gradient effects, and long-wavelength wobble. A concept that only says "there is a rotor going around the planet" has not yet explained how the machine is to be controlled.

This paper proposes a specific answer to both problems.

1. **Helical small-\(\alpha\) slug streams in a prestressed membrane guide shell.** The lanes are wrapped helically around a very large tensile membrane tube. Their curvature creates outward pressure that inflates and prestresses the torus, turning moving momentum into local structural stiffness.
2. **A four-lane balanced cell for macro-scale control.** The same helical geometry allows balanced groups of lanes whose momentum components cancel in steady operation but can be modulated through fixed spatial speed gradients to produce distributed tug fields and ring-scale bending moments.

Those are the two main novelties of the paper.

The cleanest way to say the thesis is this:

> Earth-scale curvature supplies macro lift, tube-scale helical curvature supplies local membrane prestress, and controlled spatial gradients in lane momentum flux supply macro-shape actuation. A four-lane balanced cell allows those three functions to coexist while cancelling first-order steady momentum and torque channels.

The claim envelope should be stated early. This paper does not claim closure of the full orbital-ring system. It claims that shallow helical momentum streams plus four-lane balanced cells define a plausible internal prestress and actuation primitive. Dynamic stability, guide technology, thermal rejection, fault isolation, and passive-mass closure remain explicit closure requirements.

The main fatal risks are also worth naming early: follower-force instability, unacceptable guide loss, impossible thermal rejection, unmanageable fault-domain energy, and a passive-mass closure loop that fails to converge.

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

### 1.2 Reference bookkeeping case

To keep later screens anchored, the paper uses one primary bookkeeping case unless otherwise stated.

| Quantity | Baseline value | Role in the paper |
| --- | --- | --- |
| Altitude | 500 km | Primary reference case |
| Ring-tangential speed \(u\) | 10 km/s | Macro-lift and control screens |
| Torus radius \(a\) | 50 m | Helix-curvature and shell screens |
| Passive supported weight \(w_p\) | 10 kN/m | Notional support burden |
| Lane count | about 300 | Discrete-lane and balanced-cell screens |
| Prestress ratio \(\Gamma\) | 10 baseline, 30 to 100 sensitivity | Lower-bound shell-prestress screen |

This is a bookkeeping case, not an optimized design. It is used to keep the paper's numbers internally consistent while making clear which burdens grow when the passive mass or prestress target rises.

**Suggested Figure 1. Overall concept sketch.** Show a world-encircling torus with roughly 100 m diameter, rendered as a lightweight fabric membrane rather than a solid pipe. Include a local cutaway showing several shallow-angle helical lanes attached to the membrane and one enlarged inset showing a four-lane balanced cell. The image should make the paper's core claim visible in one glance: the same helical lane system gives both local prestress and macro-control authority.

**Figure conventions used throughout.** Do not draw steep helices, a rigid pipe, or only a small number of lanes. Do not depict local prestress as a literal gas pressure unless the homogenization step is indicated. Do not draw the tug actuator as a single thruster or brake; it should appear as a distributed speed-gradient zone. If the reference case is drawn, show it as a low-orbit world ring, not as a tiny deep-space loop floating far from Earth.

The argument proceeds in six steps. First, momentum redirection is established as the basic force mechanism. Second, the paper asks what one lane demands from its magnetic guide. Third, it shows why a straight high-speed lane does not self-center under perturbation. Fourth, it introduces the helical toroidal guide architecture as a way to turn the dominant steady curvature load into useful local prestress while making the remaining stability problem explicit. Fifth, it develops the four-lane balanced cell and distributed tug fields as the main macro-control result. Only then does it turn to the harder practicality screens: macro lift throughput, atmospheric environment, fault-domain architecture, and closure.

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

### 3.2 Tugging also requires tangential traction

The guide-force screen is not only a normal-force screen. Any speed-gradient control section must also accelerate or decelerate the slugs longitudinally.

For one lane, a stationary speed gradient requires tangential force density

\[
q_\parallel = \dot m \frac{du}{ds}
\]

along the lane. The corresponding mean tangential traction scale is therefore roughly

\[
p_\parallel \sim \frac{\dot m |du/ds|}{A'}.
\]

The normal guide requirement from curvature following is still

\[
p_\perp \sim \frac{\dot m v\kappa}{A'},
\]

so a more honest first screen on the stator is a vector resultant,

\[
p_{\mathrm{req,total}} \sim \sqrt{p_\perp^2 + p_\parallel^2},
\]

before adding control margin, thermal margin, gap margin, and loss margin. A ring that can guide the lane laterally but cannot push and brake it longitudinally does not yet possess the proposed macro-control channel.

A representative numerical case is useful here. In the paper's notional 500 km, 10 kN/m passive-load example, the moving-stream line density is about 1600 kg/m. If that is spread across roughly 300 lanes, each lane carries about 5.4 kg/m, so at 10 km/s the mass flux per lane is about 5.4 × 10⁴ kg/s. With helix angle about 0.79 degrees and tube radius 50 m, the local helical curvature is about 3.8 × 10⁻⁶ per metre. The resulting normal guide load is then only about 2.1 kN per metre of lane. Even a 10 MN long-wave tug shared across 300 lanes corresponds to only about 33 kN integrated axial contribution per lane, or about 0.33 N/m if spread over a 100 km control sector. That is a helpful reality check. The lane-level distributed force densities are not obviously the dominant horror. The harsher burdens are the associated power exchange, synchronization, thermal management, and fault energy.

### 3.3 Convective local control

A lane is not merely static curvature plus average force. The stream is convected through the guide at high speed, so disturbances arrive on a timescale

\[
t_\mathrm{conv} \sim \frac{\lambda}{v},
\]

where \(\lambda\) is disturbance wavelength. At \(v=10~\mathrm{km/s}\), a 100 m disturbance convects past in 10 ms, a 10 m disturbance in 1 ms, and a 1 m disturbance in 0.1 ms. High speed helps force generation and hurts control.

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

## 4. Why straight lanes and monolithic rotors do not provide passive self-centering by momentum redirection alone

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

This is not yet a complete stability model. Real dynamics also involve beam stiffness, membrane stiffness, damping, actuator delay, boundary conditions, and control law. But it is enough to establish the key point: a straight high-speed lane does not passively self-center by momentum redirection alone. The moving stream behaves like an anti-restoring curvature follower unless the surrounding structure and controls provide compensating reaction.

That observation cuts directly against naive pictures of a single giant monolithic rotor or a set of parallel straight rotors simply going around Earth. Such concepts may contain enough momentum to generate support in principle, but they do not automatically contain a good structural answer to perturbations.

**Suggested Figure 4. Anti-restoring behavior of a perturbed straight lane.** Show a nominally straight lane with a small sinusoidal bend. Draw the local curvature and the stream reaction arrows pushing into the bend rather than away from it. Under the drawing, show the short derivation \(q_\mathrm{stream}\approx -T_\mathrm{eq}y_{xx}\rightarrow +T_\mathrm{eq}k^2y\). This figure should be the moment where the reader understands why a simple straight rotor picture is incomplete.

---

## 5. Helical lanes in a prestressed membrane guide shell

The helical toroidal guide architecture is the first major payoff of the paper.

Instead of asking a fast lane to remain straight in free space, the architecture places the lane on an intentionally curved helical path wrapped around a very large tensile membrane tube. The simplest intuition is a lightweight fabric torus, but the hardware should be pictured more technically as a prestressed membrane-and-rib guide carrier with discrete lane carriers, distributed stators, power buses, sensors, thermal paths, and fault segmentation.

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

The averaging is only justified when lane pitch, rib stiffness, and membrane shear transfer are fine enough that the discrete loads appear smooth at the wavelengths of interest. At \(a=50~\mathrm{m}\), the circumference is about

\[
2\pi a \approx 314~\mathrm{m}.
\]

If the torus carries on the order of 300 lanes, the pitch is about 1 m and a pressure-like description may be reasonable for long-wave structural modes. If it carries only a few tens of lanes, the loading is much less pressure-like and the discrete rib-and-membrane mechanics become first-order.

Equivalent pressure should therefore be read as a useful homogenized model, not as proof that the membrane literally feels a perfectly smooth gas-like pressure field.

### 5.3 Prestress creates a reaction substrate, not automatic stability

Equivalent pressure \(p_\mathrm{eq}\) creates hoop membrane force per unit ring length

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

A more review-proof way to write the screening condition is in the frequency domain. Define the total incremental stiffness as

\[
K_\mathrm{tot}(k,\omega) = K_\mathrm{membrane}(k,\omega) + K_\mathrm{guide}(k,\omega) + K_\mathrm{control}(k,\omega).
\]

Then, for a sinusoidal perturbation of wavenumber \(k\), the real part must satisfy

\[
\mathrm{Re} K_\mathrm{tot}(k,\omega) > T_\mathrm{eq} k^2.
\]

with positive damping and adequate phase margin required separately. In other words, the real difficulty is not merely static stiffness. It is whether the membrane, guide, and delayed controller together remain stabilizing over the disturbance band of interest.

Put differently, the torus gives the lane something real to push against. It does not let the paper claim that the instability problem has disappeared.

Lanes could in principle be mounted on the inner or outer surface of the membrane, or on shallow truss or rib hardware attached directly to it. The point is not the exact attachment detail at this stage. The point is that the prestressed membrane becomes the structural reaction surface for the helical lanes.

**Suggested Figure 5. Helical lane inflating the membrane guide shell.** Draw a cutaway of the torus wall with shallow-angle helical lanes attached to it. Show the lane reaction pressing outward, the membrane carrying hoop tension, and secondary hardware mounted to the now-prestressed wall. Add a second overlay showing a small perturbation about the nominal helical path, with labels indicating that the steady load becomes prestress but incremental stability still depends on membrane stiffness, guide stiffness, and active damping. The lanes should be drawn as nearly axial with only slight azimuthal drift, not as a steep barber-pole helix.

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

Using a reference case with a = 50 m, altitude 500 km, u = 10 km/s, and Gamma = 10, one gets an optimal helix angle of about 0.014 radians, or about 0.79 degrees.

That is a striking result. Once macro lift matters, the optimal helical bias may be very small. This supports exactly the picture advocated here: a large torus with many shallow-angle helical lanes, not a steeply wrapped screw conveyor.

At a = 50 m and alpha about 0.79 degrees, one full wrap pitch is about 23 km.

That is visually important. The intended architecture is not a steep screw or barber pole. It is a field of many nearly axial lanes with only a very slight azimuthal drift.

The more worrying point is not helix visibility. It is whether the associated prestress is actually enough. With passive supported weight of 10 kN per metre and prestress ratio Gamma equal to 10, the implied hoop-force target is only about 100 kN per metre. At a 50 m torus radius, that corresponds to only about 2 kPa of equivalent pressure. That is useful for roundness and wrinkle suppression, but it is not obviously enough to make a 100 m diameter shell behave like a stiff beam.

That observation suggests that \(\Gamma=10\) should be read as a lower-bound screening case, not as a settled design point. If shell-mode analysis demands higher prestress, the required helix angle rises only slowly. At the same 500 km, 10 km/s point, \(\Gamma=30\) gives about 1.38 degrees and a wrap pitch of about 13 km, while \(\Gamma=100\) gives about 2.51 degrees and a wrap pitch of about 7 km. The architecture therefore appears compatible with substantially higher prestress, but the real requirement has to come from shell stiffness, ovalization modes, rib spacing, and load-path analysis rather than from geometry alone.

### 5.5 What the prestressed shell does and does not solve

The prestressed membrane guide shell solves an important local problem. It gives the lanes a reaction structure, creates local prestress, and provides a platform for hardware.

It does **not** automatically create a globally rigid torus, and it does **not** by itself close the local stability problem. A 100 m diameter prestressed membrane can be locally round and still be very flexible at long wavelength, while local perturbations can still go unstable if the incremental guide-and-membrane stiffness is inadequate.

For the 500 km, \(u=10~\mathrm{km/s}\), \(\Gamma=10\) reference case, the equivalent pressure is only about 2 kPa and the corresponding hoop force is only about 100 kN/m. That may be enough to keep a ribbed membrane shell round and wrinkle-resistant. It is not enough to assume beam-like cross-sectional rigidity. If the useful shell needs something more like 0.3 to 1 MN/m of hoop force to control ovalization and rib-to-rib shear, then the prestress target must move into the \(\Gamma\sim 30\) to \(100\) range instead.

The homogenized shell picture should also be bounded in wavelength. With about 300 lanes around a 314 m circumference, the pitch is about 1 m, so pressure-like averaging may be reasonable for long-wave deformation. It should not be trusted blindly for metre-scale guide deformation, local rib failure, lane dropout, or sharp control-sector gradients. A useful rule of thumb is that the smoothed shell model belongs to wavelengths well above the torus diameter and preferably well above the circumference, while shorter scales require an explicitly discrete lane-and-rib treatment.

That is why the orbital ring still requires active macro-control, and why the four-lane balanced cell becomes essential.

---

## 6. The four-lane balanced cell

A simple mirrored pair is useful, but it is not enough for a helical architecture.

If one chooses a mirrored helical pair with tangent vectors

\[
t_x = \cos\alpha e_s + \sin\alpha e_\theta,
\]

\[
t_y = -\cos\alpha e_s + \sin\alpha e_\theta,
\]

then the axial components cancel, but the circumferential components add. That means a two-lane pair can still carry steady circumferential momentum and angular momentum around the torus.

The minimal balanced cell therefore contains four lanes. To keep the sign bookkeeping explicit, define handedness geometrically by the sign of \(d\theta/ds\) for the lane centerline itself: right-handed means positive azimuthal slope with increasing \(s\), and left-handed means negative azimuthal slope.

| Lane | Travel sign | Handedness | \(s\)-momentum | \(\theta\)-momentum | Role |
| --- | ---: | --- | ---: | ---: | --- |
| 1 | + | RH | + | + | pair A |
| 2 | - | LH | - | + | pair A |
| 3 | + | LH | + | - | pair B |
| 4 | - | RH | - | - | pair B |

Pair A therefore cancels \(s\)-momentum but retains positive \(\theta\)-momentum, pair B cancels \(s\)-momentum but retains negative \(\theta\)-momentum, and the four-lane cell cancels both together.

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

These cancellations are not automatic. They require equal mass flux, equal scalar speed profiles, matched helix angles, and symmetric placement of the four lanes within the cell. Flux mismatch, lane dropout, speed-trim error, or geometric asymmetry create residual force and torque channels.

### 6.1 Tolerance budget and degraded modes

The balanced cell is elegant, but it is not forgiving. In the 500 km, \(u=10~\mathrm{km/s}\), 300-lane reference case, one lane carries about 5.4 × 10⁴ kg/s of mass flux. Its ring-direction momentum flux is therefore about 5.4 × 10⁸ N, and its circumferential momentum flux at 0.79 degrees helix angle is about 7.6 × 10⁶ N.

That means even a small fractional mismatch creates a real residual channel:

| Fractional mismatch in one lane | Residual \(s\)-momentum-flux channel | Residual \(\theta\)-momentum-flux channel |
| --- | ---: | ---: |
| 0.01% | about 54 kN | about 0.76 kN |
| 0.1% | about 0.54 MN | about 7.6 kN |
| 1% | about 5.4 MN | about 76 kN |

So the cancellation tolerances are not cosmetic. A four-lane cell only behaves like the intended primitive if mass flux, speed profile, and phasing are held tightly enough that the residual channels remain small compared with the commanded ones.

Single-lane failure is harsher still. A lane dropout does not produce a slightly imperfect balanced cell. It destroys the symmetry class of that cell. The safe response is therefore not to keep operating the remaining three lanes as if nothing happened. It is to isolate the failed cell, dump or bleed its associated tug command, and transition neighboring cells into a degraded but still symmetric support mode. That degraded-mode architecture is a first-class requirement, not a later embellishment.

**Suggested Figure 6. Four-lane balanced cell.** Show the four lane helices in cross-section and in a short perspective cutaway, with arrows labeling handedness and travel direction. Use color-coded momentum vectors to show cancellation of axial, circumferential, and angular components. Then indicate the common-mode pressure channel that remains. The helices should be drawn with very shallow apparent winding, consistent with the small-\(\alpha\) regime. The figure should make the cell feel like a genuine machine primitive.

---

## 7. Distributed tug fields and macro-scale ring control

This is the second major payoff of the architecture, and arguably the main result of the paper.

The inflated torus makes a locally stiff substrate. The four-lane balanced cell makes that substrate actively controllable at long wavelength.

The right mental picture is not a rigid pipe with a single giant control thruster attached to it. It is a huge, lightly built but prestressed torus with many nearly axial lanes distributed around its wall, and selected neighborhoods of stator modules quietly speeding up or slowing down particular lanes over long distances. Those neighborhoods are what let the ring "lean" on itself internally.

At this point the architecture has solved an important local problem. The helical lanes can inflate and prestress the membrane guide shell, and the four-lane cell can remove hidden steady momentum and torque channels. But a locally stiff torus is not yet a globally well-aligned orbital ring. A 100 m diameter prestressed membrane can still be flexible at long wavelength. The ring still has to respond to tether loads, payload-launch impulses, gravity-gradient effects, construction asymmetries, and wobble modes.

So the decisive question is whether this lane architecture identifies a plausible macro-scale control channel. The claim of this section is narrower than full control closure: if one places spatial speed gradients in the right lanes, in the right sectors, then the torus can in principle develop distributed internal tugs and ring-scale bending moments. Whether the resulting shell, guide, controller, and power system can stabilize those modes in practice is a later question.

### 7.1 Stationary spatial speed gradients act on momentum flux

The quantity being controlled is momentum flux along the ring centerline direction \(s\).

Physically, one should imagine a control sector as a long run of stator hardware that does not grab the whole torus at once. Instead, it gently biases the speed of selected lanes over some distance, rather like a very long electromagnetic grade in a maglev line. The force on the structure comes from those distributed speed ramps.

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

### 7.2 Why counter-propagating lanes add instead of canceling

Now consider a mirrored pair in the same fixed spatial speed gradient. If \(du/ds>0\), the \(+s\)-traveling lane accelerates through the section while the counter-propagating lane decelerates through the same section. Yet their structural force densities are the same, because both are governed by the same stationary gradient law above.

So for one mirrored pair,

\[
q_{s,\mathrm{pair}} = -2\dot m \frac{du}{ds}.
\]

This is the real reason the pair adds instead of cancels. It is not that both lanes slow down in their own direction of travel. It is that a fixed spatial speed gradient produces the same structural reaction for both travel directions.

In more visual terms, a mirrored lane pair passing through one control sector behaves less like two carts hitting two brakes and more like two opposite traffic lanes passing through the same hill in the road. One stream is climbing while the other is descending, but the roadbed still feels the same net push in the same place.

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

For constant \(\alpha\), \(|\Delta u| = \cos\alpha |\Delta v|\).

**Suggested Figure 7. Why the pair adds instead of cancels.** Draw two mirrored counter-moving lanes passing through the same stationary speed-gradient section from opposite directions. Show one lane accelerating and the other decelerating, while the structural reaction arrows point the same way. The figure should make clear that the common sign comes from the fixed spatial gradient, not from two same-direction braking events.

### 7.3 Distributed tug fields

The control section need not be a hard boundary. In fact, a distributed transition is usually better because it lowers peak local force density.

That means the actuator is best imagined not as a point force but as a long, quiet patch of guideway that slightly changes lane speed over hundreds of metres or kilometres. The tug is smeared out along the structure instead of being applied at one violent station.

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
F_{\mathrm{sector}} = \int q_{s,\mathrm{sector}}(s) ds = -2N_s\dot m \Delta u.
\]

So a distributed tug field preserves the same integrated authority as a hard transition while spreading the load over a useful finite distance.

### 7.4 Opposed sectors create bending moments

Now place such tug fields in opposed azimuthal sectors of a torus of radius \(a\). Then the sector tugs form a couple.

At the level of order of magnitude,

\[
M \sim 2a |F_{\mathrm{sector}}|.
\]

A more explicit finite-sector estimate is

\[
M_{\mathrm{pair}} = 4aN_s\dot m |\Delta u| C_\mathrm{sec}(\Delta\phi)
\]

with

\[
C_\mathrm{sec}(\Delta\phi) = \frac{\sin(\Delta\phi/2)}{\Delta\phi/2}
\]

where \(\Delta\phi\) is sector width and \(C_\mathrm{sec}\) accounts for finite angular extent.

This is the macro-control mechanism. It turns distributed speed modulation in balanced helical lanes into a real bending moment on the torus.

The simplest mental picture is squeezing a hoop on two opposite sides, except here the squeeze is generated internally by momentum exchange inside the lane system rather than by external hands.

### 7.4.1 Load path from lane tug to ring bending

The couple estimate above is only useful if the torus can actually transmit sector forces as a ring-scale bending moment rather than merely ovalizing locally.

The intended free-body path is: lane force into lane carrier, lane carrier into rib or local cross-brace, rib into membrane hoop tension and circumferential shear, and then that distributed cross-sectional load closing against the opposed sector to create a couple about the ring centerline. In other words, the lane does not push directly on a rigid beam. It pushes on a ribbed shell that must redistribute the load around the torus cross-section before that load can look like ring-scale bending.

That means the simple couple law belongs to the long-wave regime. A more honest bookkeeping form is

\[
M_\mathrm{eff} \approx \eta_\mathrm{load} 2a |F_\mathrm{sector}|,
\]

where \(\eta_\mathrm{load}\) is a cross-sectional transfer efficiency between zero and one that absorbs ovalization, shear lag, local twist, and other non-ideal shell behavior. At wavelengths comparable with the torus diameter, rib spacing, or shell ovalization modes, one should expect \(\eta_\mathrm{load}\) to fall below unity and local distortion to appear before clean global bending emerges. The present paper therefore treats the tug-sector couple as a plausible long-wave actuation primitive, not as proof that every local shell mode cooperates automatically.

### 7.5 Why fill and drain are not required for steady speed fields

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

It is also important to state where the force actually comes from. The force is generated at the speed-gradient zones, not in a uniform low-speed pocket by itself. A closed low-speed pocket that returns to its starting speed has zero net integrated tug,

\[
\int -2\dot m \frac{du}{ds} ds = -2\dot m\Delta u = 0,
\]

so its entry and exit ramps produce equal and opposite tugs at different positions. Useful macro-control therefore comes from placing those opposite gradient zones deliberately in space, so they generate internal load, bending moment, or stress redistribution where desired.

So the useful mental picture is not "the ring has a slow patch." It is "the ring has a deliberately placed slow-down ramp here and a deliberately placed speed-up ramp somewhere else," with the separation between those ramps creating the useful internal couple.

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

For time-varying control profiles, the continuity constraint is stronger still. The slug density must satisfy

\[
\frac{\partial n}{\partial t} + \frac{\partial (nV)}{\partial s} = 0.
\]

So the no-fill/no-drain claim applies only to steady or slowly varying speed fields. A controller cannot arbitrarily command \(u(s,t)\) without launching density and headway waves through the lane. Dynamic control therefore requires phase and inventory management so that those waves do not create collision, starvation, or excessive headway error.

So the issue is not that mass must be added or removed in ordinary control sections. The issue is that the speed profile has to respect both static spacing limits and dynamic continuity.

**Suggested Figure 8. Distributed tug field without fill and drain.** Show a low-speed pocket in which slug spacing compresses smoothly as slugs enter, followed by a higher-speed return where spacing re-expands. Label \(n=J/v\) and \(s=vh\). Mark the entry and exit ramps as the actual tug-generating zones, with opposite force signs, and make clear that useful macro-control comes from placing those gradients at deliberately chosen positions. The figure should also show that local occupancy changes because transport speed changes, not because slugs are literally injected or removed inside the control section.

### 7.6 The tug actuator is also a high-power energy exchanger

The tug equations are momentum-flux equations, but a reviewer will immediately ask about power, and rightly so.

For one lane, the exact finite power transfer across a section that changes speed from \(u_1\) to \(u_2\) is

\[
P_{\mathrm{lane}} = \frac{1}{2}\dot m\left(u_2^2-u_1^2\right) = \dot m \bar u \Delta u
\]

where \(\bar u=(u_1+u_2)/2\). For small \(\Delta u\), this reduces to

\[
P_{\mathrm{lane}} \approx \dot m u   \Delta u.
\]

Using the force magnitude \(|F_{\mathrm{lane}}| = \dot m |\Delta u|\), this is

\[
P_{\mathrm{lane}} \approx |F_{\mathrm{lane}}|   u.
\]

At \(u \sim 10~\mathrm{km/s}\), even modest structural tug implies enormous power exchange. A 1 MN tug at 10 km/s corresponds to roughly 10 GW.

For the notional ring used throughout the paper, the more relevant number is larger. Take the screening passive load to be

\[
w_p = 10~\mathrm{kN/m}.
\]

Then a 100 km arc with a 1% local weight-or-lift mismatch carries an unbalanced load of about 10 MN.

So the grounded long-wave control example for this hypothetical ring is 10 MN, not 1 MN. At 10 km/s, that implies about 100 GW of exchanged power.

If the notional 300-lane cross-section participates broadly in that correction, the mean integrated axial contribution is only about 33 kN per lane. The surprising quantity is therefore not force per lane. It is the power associated with making even a small speed change at 10 km/s.

That does not by itself kill the architecture, but it does mean the tug-field actuator is not a gentle trim system. It is a very high-power bidirectional momentum-and-energy exchanger. The paired-gradient argument gives local power balance only if the accelerating and decelerating channels are physically co-located, phase-matched, and tied together by a bidirectional electrical or magnetic power-transfer path. Otherwise the control sector is not a locally self-balancing actuator. It is a high-power grid node that must exchange power with a bus, buffer, or some other part of the ring.

Any serious realization would therefore require bidirectional power electronics, local energy buffering, phase-managed transfer between accelerating and decelerating lanes, and heat rejection for conversion losses.

Again, the helpful mental model is not a small trim tab. It is a distributed, reversible linear-motor system moving very large power between lanes and sectors while only modestly changing speed.

### 7.7 Control-channel coupling and allocation

The tug channel is not dynamically independent. Spatial speed gradients generate structural tug, but the associated local speed field also changes helical prestress and Earth-scale lift.

This is the point where the machine stops looking like three separate knobs and starts looking like a coupled control surface. Turning the "tug" knob also nudges the local pressure and local lift channels because all three are functions of the same lane-speed field.

For the prestress channel,

\[
p_\mathrm{eq} \propto \dot m u \tan^2\alpha,
\]

so, at fixed \(\dot m\) and \(\alpha\), the first-order pressure sensitivity is simply

\[
\frac{\delta p_\mathrm{eq}}{p_\mathrm{eq}} = \frac{\delta u}{u}.
\]

For the lift channel,

\[
q_\mathrm{lift} = 2N_p\dot m\left(\frac{u}{R} - \frac{g_h}{u}\right),
\]

so the corresponding first-order sensitivity is

\[
\delta q_\mathrm{lift} = 2N_p\dot m\left(\frac{1}{R} + \frac{g_h}{u^2}\right)\delta u.
\]

The fractional lift sensitivity is therefore

\[
\frac{\delta q_\mathrm{lift}}{q_\mathrm{lift}} = \frac{\left(\frac{1}{R} + \frac{g_h}{u^2}\right)}{\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}\frac{\delta u}{u}.
\]

At the illustrative 500 km, \(u=10~\mathrm{km/s}\) reference point, that multiplier is about 3.8. So a 1% local speed modulation produces roughly a 3.8% local lift modulation in the participating lift stream.

The same speed field therefore actuates three coupled outputs: axial tug, local pressure, and local lift. A real machine would need a control-allocation layer that distributes commands across the four lanes and across neighboring sectors so that desired tug, pressure trim, and lift trim are separated as well as possible.

The right coupling metric is not just the local gradient. It is the speed-offset area associated with the tug command. Define

\[
\beta = \frac{1}{R} + \frac{g_h}{u^2}.
\]

For the participating lane pairs in one control sector, the integrated lift side-effect is

\[
\Delta W_{\mathrm{lift,sector}} = 2N_s\dot m\beta \int \delta u(s) ds.
\]

The associated tug from one gradient zone is still

\[
F_{\mathrm{sector}} = -2N_s\dot m \Delta u.
\]

So the coupling ratio becomes

\[
\frac{\Delta W_{\mathrm{lift,sector}}}{F_{\mathrm{sector}}} = -\beta \frac{\int \delta u(s) ds}{\Delta u}.
\]

If one defines an effective speed-offset length, called \(L_\mathrm{eff}\), as the speed-offset area divided by the speed step, then the earlier \(\beta L\) estimate is just the special case in which that effective length happens to equal the physical sector length. A triangular ramp gives about \(L_\mathrm{eff}=L/2\). A long low-speed pocket is dominated by its plateau length. An antisymmetric profile can partly cancel its own lift side-effect.

So the honest statement is this: the control coupling is governed by the speed-offset area associated with the tug command, not by the gradient alone.

At the illustrative 500 km, u = 10 km/s point, beta is about 2.3 × 10⁻⁷ per metre, and the corresponding inverse length scale is about 4,350 km. Commands whose effective offset length is far shorter than a few thousand kilometres therefore sit in a weak-coupling regime.

It is useful to separate three different smallness claims.

First, the required speed trim for a long-wave tug can be small because the moving mass flux is enormous. A 10 MN tug spread across 300 participating lanes is only about 33 kN per lane. With about 5.4 × 10⁴ kg/s per lane, that implies a speed step of only about 0.61 m/s, or about 6 × 10⁻⁵ of the 10 km/s operating speed.

Second, the integrated lift side-effect per tug is small only when the effective speed-offset length is short compared with about 4,350 km. For a conservative 100 km box-like offset profile, the coupling factor is about 0.023, so a 10 MN tug carries about 230 kN of integrated lift side-effect. For a triangular profile of the same span, the side-effect is about half that.

Third, the resulting compensation burden can also be small, but only if the controller has spare lift and pressure trim authority. Spreading the conservative 230 kN side-effect over a 1000 km neighboring compensation arc gives only about 0.23 N/m, which is 2.3 × 10⁻⁵ of the screening 10 kN/m supported load. With the 3.8 lift sensitivity, the required common-mode speed correction is then only about 6 × 10⁻⁶. But that compensation is not free. It consumes trim margin and may introduce lower-frequency interactions between sectors.

That is why the coupling can converge rather than blow up. The strong inner-loop channel is axial tug. Pressure and lift correction are weaker outer-loop trims only if the speed-offset area is short enough and spare trim authority exists.

A useful way to name that problem is with a local linearized control map. Write

\[
\delta y = \mathbf{M} \delta u
\]

with output vector

\[
\delta y = \left(\delta F_s,  \delta p_\mathrm{eq},  \delta q_\mathrm{lift}\right)^T
\]

and lane-command vector

\[
\delta u = \left(\delta u_1,  \delta u_2,  \delta u_3,  \delta u_4\right)^T.
\]

Here \(\mathbf{M}\) depends on lane placement, handedness, sector participation, and operating point. The present paper does not solve that allocation problem, but naming it explicitly makes clear what the next control-theory step must be.

In plain language, the controller is trying to combine four lane-speed trims into three useful local effects, while suppressing the residual unwanted ones. That is a recognizable control-allocation problem, not handwaving.

### 7.8 Global bookkeeping and compensating zones

The ring is not creating net momentum from nowhere. A tugging sector must be paired with other sectors or stations that close the momentum and energy bookkeeping.

What the architecture offers is not free net force. It offers a way to **redistribute** momentum flux and the associated structural reaction in space. That is exactly what a shape-control system needs.

The important result is that this redistribution can be accomplished internally, in balanced four-lane cells, by smooth spatial speed fields. One does not need monolithic moving hoops or routine fill-and-drain hardware throughout the ring to generate useful macro moments.

In practice, one should picture families of cooperating sectors around the ring, not a single magic control patch acting in isolation. One sector borrows momentum and another pays it back.

### 7.9 What this control channel is for

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

## 8. Remaining closure screens

The paper's claim is architectural coherence at the control-primitive level. Several closure screens are still decisive.

### 8.1 Macro lift is still a separate burden

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

### 8.2 The full system faces a closure loop

Let passive structural and hardware weight per unit ring length be \(w_p\). The lift requirement can be written as

\[
A_\mathrm{pair} = N_p \dot m   u \ge \frac{w_p}{2\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}
\]

where \(A_\mathrm{pair}\) is the paired-module momentum-flux scale and the total paired-lane contribution is \(2A_\mathrm{pair}\).

That sounds like a simple scaling law, but it closes several hard subsystems into one loop:

\[
w_p \to A_\mathrm{pair} \to \left(E_{\mathrm{kin}},  P_{\mathrm{loss}}\right) \to \left(w_{\mathrm{contain}},  w_{\mathrm{thermal}},  w_{\mathrm{power}}\right) \to w_p
\]

In words:

1. more passive hardware raises ring weight,
2. more weight requires more momentum flux,
3. more momentum flux raises stored energy per metre and usually raises losses,
4. those burdens demand more containment, thermal hardware, and power infrastructure,
5. which raises ring weight again.

The concept stands or falls on whether this loop converges.

One brutal scale number is worth stating explicitly. In the illustrative 500 km, \(u=10~\mathrm{km/s}\) reference case,

\[
\frac{u^2}{R} - g_h \approx 6.1~\mathrm{m/s^2}.
\]

So supporting even

\[
w_p = 10~\mathrm{kN/m}
\]

of passive weight requires moving-stream line density of about

\[
\lambda_\mathrm{stream} \approx \frac{w_p}{u^2/R-g_h} \approx \frac{10{,}000}{6.1} \approx 1600~\mathrm{kg/m}.
\]

The corresponding kinetic energy per metre is then

\[
E' \approx \frac{1}{2}\lambda_\mathrm{stream}u^2 \approx 82~\mathrm{GJ/m}.
\]

For a full 40,000 km class ring, that implies total moving-stream kinetic energy on the order of 3.3 × 10¹⁸ J in this notional case. That is the energy scale associated with the notional \(10~\mathrm{kN/m}\) passive load case. It does not refute the architecture, but it should stop the reader from underestimating the closure burden.

The harder message is that the moving-energy burden scales linearly with passive weight. A crude closure worksheet therefore looks like this:

| Passive weight assumption | Moving-stream line density | Moving kinetic energy per metre |
| --- | ---: | ---: |
| 10 kN/m | about 1,600 kg/m | about 82 GJ/m |
| 30 kN/m | about 4,900 kg/m | about 245 GJ/m |
| 100 kN/m | about 16,000 kg/m | about 820 GJ/m |

So the closure loop is not a subtle second-order effect. If containment, thermal hardware, guide modules, ribs, and fault isolation drive passive weight up by a factor of only a few, the moving-energy burden rises by the same factor.

### 8.3 Reference altitude choice: 500 km primary, 80 km stress-test

The 80 km altitude used in earlier drafts is better read as a stress-test case than as a credible operating reference. A 40,000 km class stationary structure at roughly that altitude would face atmospheric interaction, drag variability, upper-atmosphere heating, reactive-species exposure, materials degradation, and likely large station-keeping loads.

For the present draft, the primary numerical example is therefore moved to 500 km altitude, which removes most of the atmospheric objection while leaving the basic macro-lift screening surprisingly similar. At 10 km/s, the net outward acceleration is about 5.9 m/s² at 80 km and about 6.1 m/s² at 500 km. The throughput problem therefore does not disappear at higher altitude, but the environment becomes less obviously self-defeating.

That said, 500 km is not environment-free. A world-scale active structure there would still face orbital debris, atomic oxygen, radiation, thermal cycling, station-keeping demands, collision avoidance, and maintenance burden. So the altitude change removes one severe objection, but it does not solve the space-environment problem.

The 80 km case remains useful only as a lower-altitude stress test. The 500 km case is the more reasonable notional reference for the rest of the paper.

### 8.4 Fault domains still need an explicit architecture

The helical membrane guide shell should not be interpreted as a containment solution by itself. Any serious version of the architecture would still require physical segmentation into independently isolated sectors, energy-isolating gates, sacrificial catchers, controlled dump paths, distributed braking, and faulted-section bypass.

Fault-domain length must be set by allowable segment energy, not by construction convenience. If the moving stream stores energy per unit length \(E'\), then each isolated domain inherits

\[
E_{\mathrm{segment}} = E' L_{\mathrm{segment}},
\]

and the isolation architecture has to be sized from that energy, not merely named.

At the notional 82 GJ/m energy density, even a 1 km isolated fault domain still contains about 82 TJ. So "small" domains are still enormous energetic objects. This paper does not develop that system in detail, but the energy scale has to be stated explicitly because containment cannot be left implicit.

**Suggested Figure 10. Macro-lift versus local-control separation.** Show a large Earth-centered orbital ring with one local inset. In the large view, highlight the ring-tangential momentum component responsible for macro lift. In the inset, highlight the shallow helical lanes and opposed-sector tug fields responsible for local prestress and macro-shape control. The figure should remind the reader that this paper mainly solves a control architecture, not the entire full-scale closure problem.

---

## 9. Conclusion

This paper argues for a specific architectural idea: shallow-angle helical slug streams running in a prestressed membrane guide shell can provide both a local structural substrate and a plausible macro-scale actuation primitive for an active-support orbital ring.

The first key result is local. Helical curvature converts momentum redirection into distributed inflation pressure and hoop prestress, giving the membrane guide shell something closer to a real structural reaction surface than a bare straight lane or monolithic rotor picture provides.

The second key result is global. The same helical geometry enables a four-lane balanced cell whose lanes can be modulated to produce distributed tug fields for orbital-ring alignment, wobble suppression, tether-load management, and other long-wave control tasks while preserving first-order steady momentum balance.

Those two results belong together. The prestressed shell without the balanced control cell is only a locally stiff carrier. The balanced control cell without the prestressed shell lacks a good medium through which to act. Together they form a coherent architecture.

A major motivation for the architecture is that straight high-speed lanes and simple monolithic rotors do not provide passive self-centering by momentum redirection alone. The stream pushes into existing curvature. The helical guide shell is therefore not merely a convenient geometry. It is a way to supply the reaction structure and control channels that a viable ring would need anyway.

The main control result can be stated compactly. A stationary spatial speed gradient changes lane momentum flux. In a mirrored counter-moving pair, one lane accelerates while the other decelerates through the same fixed section, yet their structural reactions add rather than cancel. In a four-lane balanced cell, those pairwise tug fields can be placed in opposed sectors to generate ring-scale moment commands while maintaining first-order steady momentum balance.

The next crux is no longer whether that primitive exists. It is whether a distributed stator, power, and control system can command useful momentum-flux gradients while simultaneously maintaining lane phase, headway, lift, prestress, power balance, thermal rejection, and fault isolation. That is the natural next battlefield for the concept.

Macro lift still demands superorbital ring-tangential momentum flux, and the closure screens remain harsh. The present draft therefore does not claim a physically closed, dynamically proven, thermally solved, fault-tolerant machine. It claims something narrower and, I think, more durable: this architecture identifies a plausible internal actuation primitive that simple rotor-around-Earth sketches do not have. Even if the full orbital ring proves too hard, the paper identifies a new family of active-support structures in which moving momentum, tensile membranes, and distributed control are tightly integrated.

---

## Appendix A. Minimal dynamic stability model

The anti-restoring follower-force argument in Section 4 is a structural warning, not yet a stability proof. A minimal linearized model for one lane carrier relative to the prestressed shell can be written more safely by keeping the stream reaction explicit on the right-hand side:

\[
m_\mathrm{eff} y_{tt} + c_\mathrm{eff} y_t + B_\mathrm{eff} y_{ssss} + K_\mathrm{shell} y + K_\mathrm{guide} y + K_\mathrm{ctrl} y(t-\tau_c) = q_\mathrm{stream},
\]

with

\[
q_\mathrm{stream} = -T_\mathrm{eq} y_{ss}.
\]

Here \(m_\mathrm{eff}\) is effective moving-plus-supported mass per lane length, \(c_\mathrm{eff}\) is passive and active damping, \(B_\mathrm{eff}\) is short-wave bending or rib stiffness, \(K_\mathrm{shell}\) is the restoring contribution of the prestressed shell, \(K_\mathrm{guide}\) is local guide stiffness, \(K_\mathrm{ctrl}\) is delayed feedback stiffness, and \(T_\mathrm{eq}\) is the moving-stream follower-force scale.

Moving the stream reaction to the left gives the equivalent homogeneous form

\[
m_\mathrm{eff} y_{tt} + c_\mathrm{eff} y_t + B_\mathrm{eff} y_{ssss} + K_\mathrm{shell} y + K_\mathrm{guide} y + K_\mathrm{ctrl} y(t-\tau_c) + T_\mathrm{eq} y_{ss} = 0,
\]

so for a Fourier mode \(y \propto e^{i(ks-\omega t)}\), the characteristic balance becomes

\[
-m_\mathrm{eff}\omega^2 + i c_\mathrm{eff}\omega + B_\mathrm{eff}k^4 + K_\mathrm{shell}(k) + K_\mathrm{guide}(k) + K_\mathrm{ctrl}(k)e^{-i\omega\tau_c} - T_\mathrm{eq}k^2 = 0.
\]

This makes the control partition explicit.

- At short wavelength, the delayed controller cannot be the main stabilizer. One needs enough passive shell and guide stiffness that \(B_\mathrm{eff}k^4 + K_\mathrm{guide}(k)\) beats the follower term even before large delayed feedback enters.
- At longer wavelength, the shell, neighboring lanes, and sector-level control loops can contribute meaningful damping and restoring action.
- The dangerous boundary is the regime in which \(T_\mathrm{eq}k^2\) is already large while \(\omega\tau_c\) is no longer small.

The convective times in Section 3.3 show how severe that is. At 10 km/s, a 100 m disturbance passes in 10 ms, a 10 m disturbance in 1 ms, and a 1 m disturbance in 0.1 ms. If one wants feedback phase lag well below about 30 degrees at the disturbance passage rate, the effective delay budget must be well below about 0.8 ms at 100 m wavelength and well below about 0.08 ms at 10 m wavelength. That is why meter-to-hundred-meter stabilization has to be a local guide problem, not a ring-scale supervisory control problem.

So this appendix still does not prove stability. But it does name the minimum technical burden more concretely: any viable design needs a stability map over wavelength showing where passive shell stiffness dominates, where local guide control dominates, and where slower sector-level control can safely enter.

## Appendix B. Slug discreteness screen

The fixed-flux treatment is useful, but the slugs themselves cannot stay abstract. In the 500 km, 10 km/s, 300-lane, 10 kN/m reference case, each lane carries about 5.4 × 10⁴ kg/s of mass flux. The table below shows what that means for several representative slug masses.

| Slug mass | Slugs per second per lane | Spacing at 10 km/s | Time headway | Kinetic energy per slug |
| ---: | ---: | ---: | ---: | ---: |
| 0.1 kg | about 5.4 × 10⁵ /s | about 1.8 cm | about 1.8 µs | about 5 MJ |
| 1 kg | about 5.4 × 10⁴ /s | about 18 cm | about 18 µs | about 50 MJ |
| 10 kg | about 5.4 × 10³ /s | about 1.8 m | about 0.18 ms | about 500 MJ |
| 100 kg | about 5.4 × 10² /s | about 18 m | about 1.8 ms | about 5 GJ |

This is a genuine design fork.

- Small slugs reduce individual projectile energy, but demand extreme event rate, timing accuracy, sensing bandwidth, and electromagnetic switching frequency.
- Large slugs relax rate and timing, but make each slug an individually catastrophic object.

For the rest of the screening discussion, it is useful to keep one bookkeeping row in mind. A 10 kg slug is not claimed to be optimal, but it is a workable reference because it implies about 5.4 × 10³ slugs per second per lane, about 1.8 m spacing, about 0.18 ms headway, and about 500 MJ per slug. That is already severe while remaining easier to visualize than the lighter-slug rows.

The no-fill/no-drain argument in Section 7.5 remains kinematically sound for steady speed fields, but it only works if headway compression and expansion stay inside collision margins. If a controller is allowed only 10% headway error, then the 1 kg row above implies a timing tolerance of only a few microseconds, while the 0.1 kg row pushes into the sub-microsecond regime. That does not kill the concept by itself, but it means slug discreteness has to become a first-class design variable rather than a hidden detail.

## Appendix C. Power-flow, guide, and thermal screen

The local guide-force density is not obviously the worst number. In the 500 km reference case, one lane sees only about 2.1 kN/m of helical normal load, and a 10 MN ring correction shared across 300 lanes corresponds to only about 0.33 N/m of average tangential force per lane over a 100 km sector. The guide burden becomes terrifying because velocity is so high.

For the 10 MN long-wave correction used in the main text, the sector power throughput is about 100 GW. Even small inefficiency therefore becomes a large thermal burden:

| Effective conversion loss | Waste heat at 100 GW | Heat per metre over a 100 km sector |
| ---: | ---: | ---: |
| 1% | 1 GW | 10 kW/m |
| 0.1% | 100 MW | 1 kW/m |
| 0.01% | 10 MW | 100 W/m |

So the actuator can be quiet in force density and still be violent in power flow. The real guide-technology screen is therefore not just magnetic pressure. It is whether a planetary-scale electromagnetic guide can simultaneously deliver acceptable gap control, switching rate, bidirectional power exchange, loss per metre, quench safety, and fault isolation.

The guide technology is deliberately left unspecified in this paper. Any future implementation, whether based on superconducting suspension, inductive reaction, permanent-magnet carriers, conductive slugs, or some hybrid architecture, would still have to satisfy the same envelope: high-bandwidth gap control, low-loss bidirectional tangential actuation, acceptable thermal burden, and survivable fault behavior at the relevant slug rate.

A useful module-scale view makes the same point. Spread over 100 km, the average power transfer is about 1 MW per metre of sector across all participating lanes, or about 10 MW for each 10 m slice of the sector. A 10 m slice of one lane carries only about 33 kW of average control power, but at slug rates that may range from kilohertz to hundreds of kilohertz depending on slug mass. So the difficulty is not one giant generator. It is a huge distributed array of moderate-force, high-rate, high-efficiency bidirectional modules.

## Appendix D. Fault-domain and degraded-mode screen

At the 500 km reference point, the moving stream stores about 82 GJ/m. That makes allowable fault energy the key quantity for architecture. If one chooses an allowable released energy \(E_\mathrm{allow}\), the corresponding maximum isolated domain length is roughly

\[
L_\mathrm{iso} \approx \frac{E_\mathrm{allow}}{82~\mathrm{GJ/m}}.
\]

The result is brutal:

| Allowable released energy | Maximum isolation length | Stream transit time across that length at 10 km/s |
| ---: | ---: | ---: |
| 1 GJ | about 1.2 cm | about 1.2 µs |
| 10 GJ | about 12 cm | about 12 µs |
| 100 GJ | about 1.2 m | about 0.12 ms |
| 1 TJ | about 12 m | about 1.2 ms |
| 10 TJ | about 120 m | about 12 ms |
| 82 TJ | about 1 km | about 0.10 s |

So if tolerable fault release is only gigajoule-scale, the implied isolation lengths are absurdly short. Even if one accepts terajoule-scale domains, the required gates, dump paths, catchers, and bypass logic still have to operate on millisecond-to-tens-of-milliseconds timescales.

This is also where four-lane degraded mode becomes inseparable from containment. A lane dropout is not just a control nuisance. It is a fault-domain event that may force local cell isolation, rapid unloading of neighboring cells, and transfer of support demand to a wider region. The safe machine is therefore not merely a balanced nominal lattice. It is a balanced lattice plus an explicit fault-response architecture.
