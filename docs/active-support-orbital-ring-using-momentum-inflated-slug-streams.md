# Helical Slug Streams as a Prestress and Actuation Primitive for Active-Support Orbital Ring Concepts

## Abstract

This paper proposes an orbital-ring architecture built from magnetically guided high-speed slug streams running in lanes set at small helix angle around a very large lightweight toroidal guide structure. The paper's main claim is narrower than feasibility: it identifies two linked ideas that are genuinely useful at the concept level and may serve as an internal prestress-and-actuation primitive for active-support ring concepts.

The first is that helical slug streams can do more than circulate momentum. By forcing the streams to follow curved helical paths on a large toroidal membrane, the design converts momentum redirection into distributed outward pressure, hoop prestress, and local structural rigidity. The result is best understood as a prestressed membrane guide shell, intuitively a giant fabric torus, whose local stiffness is created by internal moving mass.

The second is that the same helical geometry enables a four-lane balanced cell that can generate distributed tug fields for macro-scale ring-shape actuation. In a fixed spatial speed gradient, one counter-propagating lane accelerates while its mirrored partner decelerates. Their structural reactions add, and a co-located bidirectional power path can exchange power between the two streams. That makes the cell a momentum-flux actuator and a high-power energy exchanger at the same time.

A central motivation for this architecture is that simple straight-lane or monolithic-rotor orbital-ring concepts do not provide passive self-centering by momentum redirection alone. A fast mass stream pushes into existing curvature. Without a surrounding structure and active control system that can react against that tendency, perturbations are anti-restored rather than damped away. The helical toroidal guide architecture is therefore not cosmetic. It supplies the reaction substrate and prestress channel that the control system can work through.

After presenting the force mechanism, lane-level guide requirements, perturbation argument, helical membrane architecture, and four-lane macro-actuation scheme, the paper turns to closure screens. Full-scale macro lift requires superorbital ring-tangential momentum flux, failures are energetically extreme, and losses, thermal rejection, timing, and containment all feed back into passive structural weight. The architecture should therefore be understood as a concept-level prestress and actuation primitive, not as a closed feasibility demonstration.

---

## 1. Introduction

The usual picture of an orbital ring is seductively simple: put a very fast moving mass around Earth, let curvature redirect momentum, and use the resulting reaction force to support a ring. But that picture leaves out two problems that are not secondary.

First, a fast moving mass stream does not provide passive self-centering by momentum redirection alone. If its path develops a curvature perturbation, the stream pushes further into that curvature. A simple straight lane or monolithic rotor therefore does not merely need support force. It needs a surrounding architecture that can resist and control a fundamentally anti-restoring tendency.

Second, even if one has enough moving momentum to loft a ring, that does not by itself provide a good mechanism for local structural rigidity or macro-scale alignment actuation. A ring around Earth has to survive construction tolerances, tether loads, payload impulses, gravity-gradient effects, and long-wavelength wobble. A concept that only says "there is a rotor going around the planet" has not yet explained how the machine is to be actuated, much less closed in feedback.

This paper proposes a specific answer to both problems.

1. **Helical slug streams at small \(\alpha\) in a prestressed membrane guide shell.** The lanes are wrapped helically around a very large tensile membrane tube. Their curvature creates outward pressure that inflates and prestresses the torus, turning moving momentum into local structural stiffness.
2. **A four-lane balanced cell for macro-scale actuation.** The same helical geometry allows balanced groups of lanes whose momentum components cancel in steady operation but can be modulated through fixed spatial speed gradients to produce distributed tug fields and ring-scale bending moments.

Those are the two main novelties of the paper.

The cleanest way to say the thesis is this:

> Earth-scale curvature supplies macro lift, tube-scale helical curvature supplies local membrane prestress, and controlled spatial gradients in lane momentum flux supply macro-shape actuation. A four-lane balanced cell allows those three functions to coexist while cancelling first-order steady momentum and torque channels.

The claim envelope should be stated early. This paper does not claim closure of the full orbital-ring system, nor does it claim demonstrated closed-loop controllability. It claims that shallow helical momentum streams plus four-lane balanced cells define a plausible internal prestress and actuation primitive. Dynamic stability, guide technology, thermal rejection, timing precision, fault isolation, startup, deployment, and passive-mass closure remain explicit closure requirements.

The main fatal risks are also worth naming early: follower-force instability, unacceptable guide loss, impossible thermal rejection, unmanageable fault-domain energy, and a passive-mass closure loop that fails to converge.

Figure 1a gives the global geometry of the orbital ring concept and the local section chosen for closer inspection. Figure 1b then shows the corresponding local guide-shell geometry and representative helical lanes used throughout the paper.

<figure style="margin: 1.15em auto 1.35em auto; text-align: center; page-break-inside: avoid; break-inside: avoid-page;">
  <img src="../figures/figure-1a-orbital-ring-global-geometry.svg" alt="Figure 1a, global geometry of the orbital ring around Earth, with the local section shown in detail in Figure 1b." style="width: 76%; height: auto;" />
  <figcaption style="margin-top: 0.55em; font-size: 0.92em; line-height: 1.35; color: #4b5563;">
    <strong>Figure 1a.</strong> Global geometry of the orbital ring around Earth, with the local section shown in detail in Figure 1b.
  </figcaption>
</figure>

<figure style="margin: 1.15em auto 1.35em auto; text-align: center; page-break-inside: avoid; break-inside: avoid-page;">
  <img src="../figures/figure-1b-orbital-ring-local-helical-lanes.svg" alt="Figure 1b, local guide-shell segment with representative helical lanes and local coordinates." style="width: 92%; height: auto;" />
  <figcaption style="margin-top: 0.55em; font-size: 0.92em; line-height: 1.35; color: #4b5563;">
    <strong>Figure 1b.</strong> Local guide-shell segment with representative helical lanes and local coordinates.
  </figcaption>
</figure>

### 1.1 Paper structure

The argument proceeds in six steps. First, momentum redirection is established as the basic force mechanism. Second, the paper asks what one lane demands from its magnetic guide. Third, it shows why a straight high-speed lane does not self-center under perturbation. Fourth, it introduces the helical toroidal guide architecture as a way to turn the dominant steady curvature load into useful local prestress while making the remaining stability problem explicit. Fifth, it develops the four-lane balanced cell and distributed tug fields as the main macro-scale actuation result. Only then does it turn to the harder practicality screens: macro lift throughput, fault-domain architecture, and closure.

### 1.2 Coordinate convention

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

### 1.3 Reference bookkeeping case

To keep later screens anchored, the paper uses one primary bookkeeping case unless otherwise stated.

| Quantity | Baseline value | Role in the paper |
| --- | --- | --- |
| Altitude | 500 km | Primary reference case |
| Ring-tangential speed \(u\) | 10 km/s | Macro-lift and actuation screens |
| Torus radius \(a\) | 50 m | Helix-curvature and shell screens |
| Net inward non-stream load \(w_p\) | 10 kN/m | Notional support burden |
| Lane count | about 300 | Discrete-lane and balanced-cell screens |
| Prestress ratio \(\Gamma\) | 10 baseline, 30 to 100 sensitivity | Lower-bound shell-prestress screen |

This is a bookkeeping case, not an optimized design. The 500 km altitude is only a convenient reference point, and none of the other ring parameters in this test case are claimed to be optimal. The case is used to keep the paper's numbers internally consistent while making clear which burdens grow when the passive mass or prestress target rises.

Throughout the paper, \(w_p\) should be read as the **net inward non-stream load per metre**. It includes whatever passive structural burden, tether load, payload load, drag-like disturbance, or other non-stream loading the moving stream must support. For the guide shell's own mass, that bookkeeping can include gravity minus the guide's small centrifugal relief from Earth co-rotation. At 500 km altitude that relief is small, but defining \(w_p\) this way keeps the lift comparison unambiguous.

Because the local numbers are easy to underestimate, the corresponding whole-ring inventory is worth stating early:

| Reference-case inventory item | Approximate value |
| --- | ---: |
| Ring radius at 500 km altitude | about 6,871 km |
| Circumference | about 43,000 km |
| Passive mass for \(w_p=10~\mathrm{kN/m}\) | about \(5\times10^{10}\) kg |
| Moving-stream mass for \(\lambda_\mathrm{stream}\approx 1600~\mathrm{kg/m}\) | about \(6.9\times10^{10}\) kg |
| Total moving kinetic energy | about \(3.5\times10^{18}\) J |
| Total slug count for 10 kg slugs | about \(6.9\times10^9\) |

That table does not refute the architecture, but it does place the reference case firmly in the megastructure regime. Even the paper's nominally light reference point already involves tens of billions of kilograms of passive and moving inventory.

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

---

## 3. What one lane requires from its guide

Before discussing orbital-ring architecture, it is worth asking what one lane demands from its stator.

### 3.1 Magnetic reaction scale

A rough upper bound on magnetic normal stress is

\[
p_\mathrm{mag,max} \sim \frac{B^2}{2\mu_0},
\]

where \(B\) is field strength and \(\mu_0\) is the permeability of free space. The ideal upper-bound values from \(B^2/(2\mu_0)\) are:

| Field strength \(B\) | Ideal upper-bound normal stress |
| ---: | ---: |
| 0.5 T | about 0.10 MPa |
| 1 T | about 0.40 MPa |
| 2 T | about 1.59 MPa |
| 3 T | about 3.58 MPa |

Real delivered traction will be lower because of gap, fringing, force margin, thermal limits, imperfect field topology, and control requirements.

If \(A'\) is effective magnetic interaction area per unit lane length, then the required mean traction is

\[
p_\mathrm{req} = \frac{f}{A'}.
\]

For a fixed-flux slug lane this becomes

\[
p_\mathrm{req} = \frac{\dot m v\kappa}{A'}.
\]

So tight curvature, high speed, and small interaction perimeter all make the lane harder to guide.

It is tempting to look for a simple square-cube optimum in slug size here, but this particular screen does not produce one cleanly. The relevant quantity is \(A'\), effective interaction area per unit lane length, not the perimeter of one isolated slug. If a slug family is scaled uniformly at fixed aspect ratio and lane fill fraction, then per-slug mass scales like \(L^3\) while slug count per unit lane length scales like \(1/L\), so moving mass per unit lane length scales like \(L^2\), just as interaction area per unit lane length does. On that simplified scaling, \(p_\mathrm{req} = \dot m v\kappa/A'\) does not by itself force a single geometric optimum. The sharper slug-size trade appears later through switching rate, timing precision, gap control, eddy-current loss, and per-slug fault energy rather than through this one ratio alone.

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

before adding control margin, thermal margin, gap margin, and loss margin. A ring that can guide the lane laterally but cannot push and brake it longitudinally does not yet possess the proposed macro-scale actuation channel.

A representative numerical case is useful here. In the paper's notional 500 km, 10 kN/m passive-load example, the moving-stream line density is about 1600 kg/m. If that is spread across roughly 300 lanes, each lane carries about 5.4 kg/m, so at 10 km/s the mass flux per lane is about 5.4 × 10⁴ kg/s. With helix angle about 0.79 degrees and tube radius 50 m, the local helical curvature is about 3.8 × 10⁻⁶ per metre. The resulting normal guide load is then only about 2.1 kN per metre of lane. Even a 10 MN long-wave tug shared across 300 lanes corresponds to only about 33 kN integrated axial contribution per lane, or about 0.33 N/m if spread over a 100 km control sector.

A useful caveat is

\[
q_{\parallel,\mathrm{lane}} \sim \frac{F_{\mathrm{sector}}}{N_{\mathrm{lanes}}L_{\mathrm{sector}}}.
\]

So the mild force-density result depends on broad participation and long actuation length. If only 30 lanes participate, or if the actuation length is 10 km instead of 100 km, the average tangential force density rises by about two orders of magnitude. The lane-level distributed force densities are therefore not automatically benign. They are merely not the dominant horror under the broad-participation reference case used here. The harsher burdens remain the associated power exchange, synchronization, thermal management, and fault energy.

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

A more honest way to write the screening condition is in the frequency domain. Define the total incremental stiffness as

\[
K_\mathrm{tot}(k,\omega) = K_\mathrm{membrane}(k,\omega) + K_\mathrm{guide}(k,\omega) + K_\mathrm{control}(k,\omega).
\]

Then, for a sinusoidal perturbation of wavenumber \(k\), the real part must satisfy

\[
\mathrm{Re} K_\mathrm{tot}(k,\omega) > T_\mathrm{eq} k^2.
\]

with positive damping and adequate phase margin required separately. In other words, the real difficulty is not merely static stiffness. It is whether the membrane, guide, and delayed controller together remain stabilizing over the disturbance band of interest.

Put differently, the torus gives the lane something real to push against. It does not make the instability problem disappear.

Lanes could in principle be mounted on the inner or outer surface of the membrane, or on shallow truss or rib hardware attached directly to it. The point is not the exact attachment detail at this stage. The point is that the prestressed membrane becomes the structural reaction surface for the helical lanes.

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
\tan^2\alpha_\mathrm{cross} = 2\pi a\Gamma\left(\frac{1}{R} - \frac{g_h}{u^2}\right)
\]

with

\[
\Gamma = \frac{N_{\theta,\mathrm{req}}}{w_p}.
\]

For small angles,

\[
\alpha_\mathrm{cross} \approx \sqrt{2\pi a\Gamma\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}.
\]

Using a reference case with a = 50 m, altitude 500 km, u = 10 km/s, and Gamma = 10, one gets a screening crossover angle of about 0.014 radians, or about 0.79 degrees. So once macro lift matters, the preferred helical bias is very shallow. At a = 50 m and alpha about 0.79 degrees, one full wrap pitch is about 23 km, which means the intended architecture is a field of many nearly axial lanes with only slight azimuthal drift, not a steep screw conveyor.

The more important question is whether that shallow helix produces enough prestress. With passive supported weight of 10 kN per metre and prestress ratio Gamma equal to 10, the implied hoop-force target is only about 100 kN per metre. At a 50 m torus radius, that corresponds to only about 2 kPa of equivalent pressure. That is useful for roundness and wrinkle suppression, but it is not obviously enough to make a 100 m diameter shell behave like a stiff beam.

So \(\Gamma=10\) should be read as a lower-bound screening case, not as a settled design point. If shell-mode analysis demands higher prestress, the required helix angle rises only slowly. At the same 500 km, 10 km/s point, \(\Gamma=30\) gives about 1.38 degrees and a wrap pitch of about 13 km, while \(\Gamma=100\) gives about 2.51 degrees and a wrap pitch of about 7 km. The geometry therefore remains in the shallow-helix regime even for substantially higher prestress targets. The real requirement has to come from shell stiffness, ovalization modes, rib spacing, and load-path analysis rather than from geometry alone.

### 5.5 What the prestressed shell does and does not solve

The prestressed membrane guide shell solves an important but limited problem. It gives the lanes a reaction structure, creates local prestress, and provides a platform for hardware. It does **not** automatically create a globally rigid torus, and it does **not** by itself close the local stability problem.

For the 500 km, \(u=10~\mathrm{km/s}\), \(\Gamma=10\) reference case, the equivalent pressure is only about 2 kPa and the corresponding hoop force is only about 100 kN/m. That may be enough to keep a ribbed membrane shell round and wrinkle-resistant. It is not enough to assume beam-like cross-sectional rigidity. If the useful shell needs something more like 0.3 to 1 MN/m of hoop force to control ovalization and rib-to-rib shear, then the prestress target must move into the \(\Gamma\sim 30\) to \(100\) range instead.

The homogenized shell picture should also be bounded in wavelength. With about 300 lanes around a 314 m circumference, the pitch is about 1 m, so pressure-like averaging may be reasonable for long-wave deformation. It should not be trusted blindly for metre-scale guide deformation, local rib failure, lane dropout, or sharp control-sector gradients. A useful rule of thumb is that the smoothed shell model belongs to wavelengths well above the torus diameter and preferably well above the circumference, while shorter scales require an explicitly discrete lane-and-rib treatment.

That is why the orbital ring still requires active macro-scale actuation, and why the four-lane balanced cell becomes essential.

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

The minimal balanced cell therefore contains four lanes. To keep the sign bookkeeping explicit, define handedness geometrically by the sign of \(d\theta/ds\) for the lane centerline itself: right-handed means positive azimuthal slope with increasing \(s\), and left-handed means negative azimuthal slope. **This definition is geometric, not based on the slug's direction of travel.**

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

This is not a decorative symmetry argument. It is the architecture that makes the helical torus usable as an actuation machine rather than merely a pressurized tube.

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

Slug discreteness makes the same point in time-domain form. In the 10 kg bookkeeping row developed later, one lane carries about 5.4 × 10³ slugs/s, so the nominal headway is about 0.185 ms. That means any short-time cancellation budget is quantized by individual slug arrivals.

| Averaging window in one lane | Expected slug count | One extra or missing slug implies average flux error of |
| ---: | ---: | ---: |
| 1 ms | about 5.4 | about 18.5% |
| 10 ms | about 54 | about 1.85% |
| 100 ms | about 540 | about 0.185% |
| 1 s | about 5,400 | about 0.0185% |

So a millisecond-scale controller cannot rely on statistical averaging to preserve 0.01% to 0.1% balance. It needs explicit synchronization, timing discipline, and local bookkeeping of actual slugs, not just average mass flux.

The same severity appears as phase tolerance. In the 10 kg row, 1% headway accuracy means about 1.8 µs timing precision, while 0.1% headway accuracy means about 0.18 µs. That does not automatically kill the concept, but it does mean the four-lane cell is as much a synchronization architecture as it is a symmetry argument.

Single-lane failure is harsher still. A lane dropout does not produce a slightly imperfect balanced cell. It destroys the symmetry class of that cell. The safe response is therefore not to keep operating the remaining three lanes as if nothing happened. It is to isolate the failed cell, dump or bleed its associated tug command, and transition neighboring cells into a degraded but still symmetric support mode. That degraded-mode architecture is a first-class requirement, not a later embellishment.

---

## 7. Distributed tug fields and macro-scale ring actuation

This is the second major payoff of the architecture, and arguably the main result of the paper.

The inflated torus makes a locally stiff substrate. The four-lane balanced cell gives that substrate a distributed long-wave actuation channel.

The right mental picture is not a rigid pipe with a single giant control thruster attached to it. It is a huge, lightly built but prestressed torus with many nearly axial lanes distributed around its wall, and selected neighborhoods of stator modules quietly speeding up or slowing down particular lanes over long distances. Those neighborhoods are what let the ring "lean" on itself internally.

At this point the architecture has solved an important local problem. The helical lanes can inflate and prestress the membrane guide shell, and the four-lane cell can remove hidden steady momentum and torque channels. But a locally stiff torus is not yet a globally well-aligned orbital ring. A 100 m diameter prestressed membrane can still be flexible at long wavelength. The ring still has to respond to tether loads, payload-launch impulses, gravity-gradient effects, construction asymmetries, and wobble modes.

So the decisive question is whether this lane architecture identifies a plausible macro-scale actuation channel. The claim of this section is narrower than full control closure: if one places spatial speed gradients in the right lanes, in the right sectors, then the torus can in principle develop distributed internal tugs and ring-scale bending moments. Whether the resulting shell, guide, controller, and power system can stabilize those modes in practice is a later question.

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

This is the macro-scale actuation mechanism. It turns distributed speed modulation in balanced helical lanes into a real bending moment on the torus.

The simplest mental picture is squeezing a hoop on two opposite sides, except here the squeeze is generated internally by momentum exchange inside the lane system rather than by external hands.

### 7.4.1 Load path from lane tug to ring bending

The couple estimate above is only useful if the torus can actually transmit sector forces as a ring-scale bending moment rather than merely ovalizing locally.

The intended free-body path is: lane force into lane carrier, lane carrier into rib or local cross-brace, rib into membrane hoop tension and circumferential shear, and then that distributed cross-sectional load closing against the opposed sector to create a couple about the ring centerline. In other words, the lane does not push directly on a rigid beam. It pushes on a ribbed shell that must redistribute the load around the torus cross-section before that load can look like ring-scale bending.

That means the simple couple law belongs to the long-wave regime. A more honest bookkeeping form is

\[
M_\mathrm{eff} \approx \eta_\mathrm{load} 2a |F_\mathrm{sector}|,
\]

where \(\eta_\mathrm{load}\) is a cross-sectional transfer efficiency between zero and one that absorbs ovalization, shear lag, local twist, and other non-ideal shell behavior. At wavelengths comparable with the torus diameter, rib spacing, or shell ovalization modes, one should expect \(\eta_\mathrm{load}\) to fall below unity and local distortion to appear before clean global bending emerges. The present paper therefore treats the tug-sector couple as a plausible long-wave actuation primitive, not as proof that every local shell mode cooperates automatically.

A crude screening estimate helps pin that down. In the illustrative 10 MN tug example spread over a 100 km sector, the average structural load is only about 100 N/m along that sector. If ribs or cross-braces are spaced every 10 m, that corresponds to only about 1 kN of incremental axial transfer per rib bay before azimuthal sharing. Even if only a minority of the circumference participates efficiently, the average per-bay transfer still lands in the kilonewton range rather than the meganewton range. That does not prove that \(\eta_\mathrm{load}\) is near unity, but it does suggest that long-wave load transfer is not obviously absurd provided rib spacing is on the order of metres to tens of metres and the hoop prestress is already in the \(\Gamma\sim30\) to 100 regime rather than the bare \(\Gamma=10\) lower bound.

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

so its entry and exit ramps produce equal and opposite tugs at different positions. Useful macro-scale actuation therefore comes from placing those opposite gradient zones deliberately in space, so they generate internal load, bending moment, or stress redistribution where desired.

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

### 7.6 The tug actuator is also a high-power energy exchanger

The tug equations are momentum-flux equations, but the next question is about power, and rightly so.

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

---

## 8. Remaining closure screens

The paper's claim is architectural coherence at the actuation-primitive level. Several closure screens are still decisive.

Before going through them one by one, the main unresolved closure gates can be named compactly:

| Closure gate | Representative screening variable | Why it is central |
| --- | --- | --- |
| Passive-mass convergence | supported passive weight per metre \(w_p\) | It closes directly into required momentum flux, stored energy, thermal hardware, and containment burden. |
| Guide feasibility | allowable loss, gap-control bandwidth, and bidirectional power-transfer efficiency | The lane can look gentle in force density while still being extreme in switching rate, synchronization, and power flow. |
| Four-lane balance | timing, mass, and speed mismatch budget | The balanced cell is only useful if residual momentum channels stay well below commanded tug channels. |
| Shell load transfer | cross-sectional transfer efficiency \(\eta_\mathrm{load}\) and rib spacing | Opposed sector tugs matter only if lane loads can be redistributed into a real long-wave bending couple rather than local ovalization. |
| Fault containment | isolated domain energy and response time | The stored energy density is high enough that fault handling is likely a dominant feasibility gate rather than a secondary detail. |
| Startup and reconfiguration | partial-commissioning support path and lane-phase initialization | The present paper treats startup, commissioning, and shutdown as open architectural problems rather than solved parts of the concept. |

### 8.1 Macro lift is still a separate burden

The helical torus gives local prestress. It does not, by itself, loft the entire ring around Earth. Macro lift comes from turning the ring-tangential component of stream momentum around Earth.

For the symmetric counter-propagating pairs used throughout the paper, the guide-relative expression below should be read as the leading-order form derived from the explicit inertial-frame bookkeeping in Appendix E.

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

Let \(w_p\) denote the net inward non-stream load per unit ring length. The lift requirement can be written as

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

For a full 43,000 km class ring, that implies total moving-stream kinetic energy on the order of 3.5 × 10¹⁸ J in this notional case. That is the energy scale associated with the notional \(10~\mathrm{kN/m}\) passive load case. It does not refute the architecture, but it should stop the reader from underestimating the closure burden.

The harder message is that the moving-energy burden scales linearly with passive weight. A crude closure worksheet therefore looks like this:

| Passive weight assumption | Moving-stream line density | Moving kinetic energy per metre |
| --- | ---: | ---: |
| 10 kN/m | about 1,600 kg/m | about 82 GJ/m |
| 30 kN/m | about 4,900 kg/m | about 245 GJ/m |
| 100 kN/m | about 16,000 kg/m | about 820 GJ/m |

So the closure loop is not a subtle second-order effect. If containment, thermal hardware, guide modules, ribs, and fault isolation drive passive weight up by a factor of only a few, the moving-energy burden rises by the same factor.

### 8.3 Fault domains still need an explicit architecture

The helical membrane guide shell should not be interpreted as a containment solution by itself. Any serious version of the architecture would still require physical segmentation into independently isolated sectors, energy-isolating gates, sacrificial catchers, controlled dump paths, distributed braking, and faulted-section bypass.

Fault-domain length must be set by allowable segment energy, not by construction convenience. If the moving stream stores energy per unit length \(E'\), then each isolated domain inherits

\[
E_{\mathrm{segment}} = E' L_{\mathrm{segment}},
\]

and the isolation architecture has to be sized from that energy, not merely named.

At the notional 82 GJ/m energy density, even a 1 km isolated fault domain still contains about 82 TJ. So "small" domains are still enormous energetic objects. This paper does not develop that system in detail, but the energy scale has to be stated explicitly because containment cannot be left implicit.

The right conclusion is not merely that fault isolation is required. It is that fault isolation is likely one of the dominant feasibility gates for any real machine built around this primitive.

The helical geometry may, however, offer real dump-path degrees of freedom. A deliberately opened path can in principle eject a failed slug stream outward from the torus rather than through the ring body itself, which is locally valuable. But safe disposal is still an orbital-mechanics problem, not just a local containment problem. At the 500 km reference point, the stream speed relative to the guide is 10 km/s and the guide's inertial ring-tangential speed is about 0.5 km/s. The inertial prograde and retrograde stream speeds are therefore roughly 10.5 km/s and 9.5 km/s, while local escape speed is about 10.8 km/s. So a prograde dump can be near escape while a retrograde dump remains a very energetic bound-orbit release. Depending on inertial velocity, direction, and dump impulse, unguided slugs may enter atmosphere, escape, or occupy long elliptical trajectories that re-cross the ring altitude. Emergency dumping therefore requires dedicated debris-trajectory and range-safety analysis. The present paper does not analyze that trade in detail.

### 8.4 Startup, deployment, shutdown, and reconfiguration remain open

The present paper is still strongly steady-state. That is a real limitation and should be admitted directly.

The paper does not yet answer how billions of slugs are inserted, how the stream is accelerated to operating speed, how partially commissioned sectors are supported before full lift is available, how lane phases are initialized, or how the ring is safely spun down. Those are not secondary implementation details. They are part of the architecture.

At the same time, the helical membrane concept may create deployment options that more monolithic orbital-ring sketches do not obviously possess. A membrane-and-lane system could in principle be assembled in a compact geometry, perhaps even a very large folded terrestrial or near-terrestrial staging geometry, brought to partial prestress at comparatively high helix angle, and then unfolded or reconfigured as more ring-tangential throughput comes online. In that picture, some commissioning cells might temporarily favor higher \(\alpha\) for prestress and handling margin, then later be reconfigured toward shallower steady-state \(\alpha\) once enough lift throughput exists elsewhere in the ring.

That idea is speculative, and this paper does not claim it as solved. But it is a real architectural question raised by the helical torus concept: the geometry that is best for deployment or early commissioning may not be the geometry that is best for final orbital operation. Modular lane segments and staged reconfiguration could therefore matter as much as the steady-state actuation primitive itself.

---

## 9. Conclusion

This paper argues for a specific architectural idea: shallow-angle helical slug streams running in a prestressed membrane guide shell can provide both a local structural substrate and a plausible macro-scale actuation primitive for an active-support orbital ring concept.

The first key result is local. Helical curvature converts momentum redirection into distributed inflation pressure and hoop prestress, giving the membrane guide shell something closer to a real structural reaction surface than a bare straight lane or monolithic rotor picture provides.

The second key result is global. The same helical geometry enables a four-lane balanced cell whose lanes can be modulated to produce distributed tug fields for orbital-ring alignment, wobble suppression, tether-load management, and other long-wave actuation tasks while preserving first-order steady momentum balance.

Those two results belong together. The prestressed shell without the balanced control cell is only a locally stiff carrier. The balanced control cell without the prestressed shell lacks a good medium through which to act. Together they form a coherent architecture.

A major motivation for the architecture is that straight high-speed lanes and simple monolithic rotors do not provide passive self-centering by momentum redirection alone. The stream pushes into existing curvature. The helical guide shell is therefore not merely a convenient geometry. It is a way to supply the reaction structure and actuation channels that a viable ring would need anyway.

The main actuation result can be stated compactly. A stationary spatial speed gradient changes lane momentum flux. In a mirrored counter-moving pair, one lane accelerates while the other decelerates through the same fixed section, yet their structural reactions add rather than cancel. In a four-lane balanced cell, those pairwise tug fields can be placed in opposed sectors to generate ring-scale moment commands while maintaining first-order steady momentum balance.

The next crux is no longer whether that primitive exists. It is whether a distributed stator, power, and synchronization system can command useful momentum-flux gradients while simultaneously maintaining lane phase, headway, lift, prestress, power balance, thermal rejection, fault isolation, and acceptable degraded modes. That is the natural next battlefield for the concept.

Macro lift still demands superorbital ring-tangential momentum flux, and the closure screens remain harsh. The present paper therefore does not claim a physically closed, dynamically proven, thermally solved, fault-tolerant machine. It claims something narrower and, I think, more durable: this architecture identifies a plausible internal prestress and actuation primitive that simple rotor-around-Earth sketches do not have. Even if the full orbital ring proves too hard, the paper identifies a new family of active-support structures in which moving momentum, tensile membranes, and distributed control are tightly integrated.

---

## Appendix A. Minimal dynamic stability model

The anti-restoring follower-force argument in Section 4 is a structural warning, not yet a stability proof. A minimal linearized model for one lane carrier relative to the prestressed shell should retain not only the curvature-follower term but also the moving-stream inertial and convective terms. For one lane with moving-stream line density \(\lambda_\mathrm{lane}\) and guide-frame speed \(v\), the constrained-stream reaction may be written as

\[
q_\mathrm{stream} = -\lambda_\mathrm{lane}\left(y_{tt} + 2v y_{st} + v^2 y_{ss}\right)
= -\lambda_\mathrm{lane} y_{tt} - 2\lambda_\mathrm{lane} v y_{st} - T_{\mathrm{eq,lane}} y_{ss},
\]

where

\[
T_{\mathrm{eq,lane}} = \lambda_\mathrm{lane} v^2.
\]

The first term can be absorbed into an effective mass only under stated assumptions, but the mixed convective term cannot simply be discarded. It is the non-self-adjoint transport term that can affect directional wave response, phase margin, and stability. Keeping the stream reaction explicit on the right-hand side gives

\[
m_\mathrm{eff} y_{tt} + c_\mathrm{eff} y_t + B_\mathrm{eff} y_{ssss} + K_\mathrm{shell} y + K_\mathrm{guide} y + K_\mathrm{ctrl} y(t-\tau_c) = q_\mathrm{stream},
\]

Here \(m_\mathrm{eff}\) is effective supported mass per lane length exclusive of any moving-stream inertia that one chooses to leave explicit, \(c_\mathrm{eff}\) is passive and active damping, \(B_\mathrm{eff}\) is short-wave bending or rib stiffness, \(K_\mathrm{shell}\) is the restoring contribution of the prestressed shell, \(K_\mathrm{guide}\) is local guide stiffness, \(K_\mathrm{ctrl}\) is delayed feedback stiffness, and \(T_{\mathrm{eq,lane}}\) is the lane-level moving-stream follower-force scale.

Moving the stream reaction to the left gives the equivalent homogeneous form

\[
(m_\mathrm{eff}+\lambda_\mathrm{lane}) y_{tt} + 2\lambda_\mathrm{lane}v y_{st} + c_\mathrm{eff} y_t + B_\mathrm{eff} y_{ssss} + K_\mathrm{shell} y + K_\mathrm{guide} y + K_\mathrm{ctrl} y(t-\tau_c) + T_{\mathrm{eq,lane}} y_{ss} = 0,
\]

so for a Fourier mode \(y \propto e^{i(ks-\omega t)}\), the characteristic balance becomes

\[
-(m_\mathrm{eff}+\lambda_\mathrm{lane})\omega^2 + 2\lambda_\mathrm{lane}vk\omega + i c_\mathrm{eff}\omega + B_\mathrm{eff}k^4 + K_\mathrm{shell}(k) + K_\mathrm{guide}(k) + K_\mathrm{ctrl}(k)e^{-i\omega\tau_c} - T_{\mathrm{eq,lane}}k^2 = 0.
\]

This makes the control partition explicit. If one deliberately drops the \(-\lambda_\mathrm{lane}y_{tt}\) and \(-2\lambda_\mathrm{lane}v y_{st}\) terms, the appendix reduces to the simpler quasi-static follower-stiffness toy model used only for intuition, not for a complete lane-dynamics claim.

This makes the three-band stability picture more explicit.

- **Metre-to-100 m band:** local guide stiffness, passive carrier stiffness, and very fast damping dominate. Ring-scale control is too slow to matter directly.
- **100 m-to-several-km band:** this is likely the hardest band. Convective transport, guide delays, shell modes, and local cell coordination all interact here, and the system may sit in an awkward gap between purely local guide control and truly distributed tug control.
- **Hundreds-to-thousands of km band:** distributed tug fields and sector-level coordination plausibly matter, which is the band targeted by the actuation primitive in the main text.

The convective times in Section 3.3 show how severe that is. At 10 km/s, a 100 m disturbance passes in 10 ms, a 10 m disturbance in 1 ms, and a 1 m disturbance in 0.1 ms. If one wants feedback phase lag well below about 30 degrees at the disturbance passage rate, the effective delay budget must be well below about 0.8 ms at 100 m wavelength and well below about 0.08 ms at 10 m wavelength. That is why meter-to-hundred-meter stabilization has to be a local guide problem, not a ring-scale supervisory control problem.

So this appendix still does not prove stability. But it does name the minimum technical burden more concretely: any viable design needs a stability map over wavelength showing where passive shell stiffness dominates, where local guide control dominates, and where slower sector-level control can safely enter.

### Appendix A.1. Toy long-wave closure example

It is still useful to ask whether the actuation channel is at least numerically commensurate with some long-wave disturbances. A deliberately crude screen can do that without pretending to prove closed-loop stability.

Take the 500 km reference case with a total moving-stream line density of about 1,600 kg/m and ring-tangential speed of 10 km/s. Define the whole-stream long-wave follower-force scale as

\[
T_{\mathrm{eq,tot}} = \lambda_{\mathrm{stream,total}}u^2.
\]

For the reference case that gives roughly 1.6 × 10¹¹ N.

For a sinusoidal long-wave displacement \(y = Y\sin(ks)\), the destabilizing follower contribution per unit ring length is of order

\[
q_\mathrm{follow} \sim T_{\mathrm{eq,tot}}k^2Y.
\]

That gives the following screening values for one metre of displacement amplitude:

| Wavelength \(\lambda\) | \(k=2\pi/\lambda\) | \(q_\mathrm{follow}/Y = T_{\mathrm{eq,tot}}k^2\) |
| ---: | ---: | ---: |
| 1000 km | about \(6.3\times10^{-6}\,\mathrm{m^{-1}}\) | about 6.3 N/m per metre of displacement |
| 100 km | about \(6.3\times10^{-5}\,\mathrm{m^{-1}}\) | about 630 N/m per metre of displacement |
| 10 km | about \(6.3\times10^{-4}\,\mathrm{m^{-1}}\) | about \(6.3\times10^4\) N/m per metre of displacement |

Now compare that with the paper's illustrative 10 MN tug command spread over a 100 km control sector. Its average structural load is about 100 N/m.

So a controller with that order of authority is plainly not a short-wave stabilizer. It is, however, numerically relevant to wavelengths in the several-hundred-kilometre to thousand-kilometre regime, which is exactly the band in which the paper intends the balanced-cell tug field to operate.

This is not a proof of control closure. Mass participation, damping, sensing, delay, actuator saturation, and shell transfer all still matter. But it does sharpen the claim. The architecture is at least consistent with a multiband picture in which short waves are a local guide-and-shell problem, the middle band is likely the hardest closure problem, and very long waves are the band where the distributed tug primitive may actually matter.

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

The 10 kg bookkeeping row also gives a simple cancellation-budget screen:

| Quantity for the 10 kg row | Approximate value |
| --- | ---: |
| Slug rate per lane | about 5.4 × 10³ /s |
| Headway | about 0.185 ms |
| Timing error for 1% headway error | about 1.8 µs |
| Timing error for 0.1% headway error | about 0.18 µs |
| Averaging time needed for one-slug count error to fall below 0.1% | about 0.19 s |

That last line is especially sobering. If balance is judged purely by counts, a one-slug mismatch does not average below 0.1% until the window is of order 0.2 s. But the lane and shell dynamics of concern are much faster than that. So precise four-lane balance is not just a matter of good average throughput accounting. It requires real-time synchronization, phase control, and fast local state estimation.

## Appendix C. Power-flow, guide, and thermal screen

The local guide-force density is not obviously the worst number. In the 500 km reference case, one lane sees only about 2.1 kN/m of helical normal load, and a 10 MN ring correction shared across 300 lanes corresponds to only about 0.33 N/m of average tangential force per lane over a 100 km sector. That is a broad-participation example, not a universal lane burden. The guide burden becomes terrifying because velocity is so high.

For the 10 MN long-wave correction used in the main text, the sector power throughput is about 100 GW. Even small inefficiency therefore becomes a large thermal burden:

| Effective conversion loss | Waste heat at 100 GW | Heat per metre over a 100 km sector |
| ---: | ---: | ---: |
| 1% | 1 GW | 10 kW/m |
| 0.1% | 100 MW | 1 kW/m |
| 0.01% | 10 MW | 100 W/m |

So the actuator can be quiet in force density and still be violent in power flow. The real guide-technology screen is therefore not just magnetic pressure. It is whether a planetary-scale electromagnetic guide can simultaneously deliver acceptable gap control, switching rate, bidirectional power exchange, loss per metre, quench safety, and fault isolation.

The guide technology is deliberately left unspecified in this paper because the present goal is to define the architecture-level prestress and actuation primitive, not to argue for one lane implementation over another. Any future implementation, whether based on superconducting suspension, inductive reaction, permanent-magnet carriers, conductive slugs, or some hybrid architecture, would still have to satisfy the same envelope: high-bandwidth gap control, low-loss bidirectional tangential actuation, acceptable thermal burden, and survivable fault behavior at the relevant slug rate.

A useful module-scale view makes the same point. Spread over 100 km, the average power transfer is about 1 MW per metre of sector across all participating lanes, or about 10 MW for each 10 m slice of the sector. Under this broad-participation example, a 10 m slice of one lane carries only about 33 kW of average control power, but at slug rates that may range from kilohertz to hundreds of kilohertz depending on slug mass. So the difficulty is not one giant generator. It is a huge distributed array of moderate-force, high-rate, high-efficiency bidirectional modules.

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

A simple worked screen shows how quickly the numbers become uncomfortable. In the 10 kg bookkeeping row, one lane carries about 5.4 × 10³ slugs/s, so a 10 ms loss-of-guidance event sweeps about 54 slugs into the faulted region. That packet contains roughly 540 kg of moving mass and about 27 GJ of kinetic energy. If one simply loses one lane of a balanced cell for those same 10 ms without immediately unloading its mirrored partners, the missing ring-direction momentum-flux channel implies an uncompensated impulse of about 5.4 × 10⁶ N s.

That is not yet a complete fault simulation, but it is enough to show the architecture's character. Even sub-second degraded events are already too energetic to be treated as routine control glitches. They are containment-and-reconfiguration events.

## Appendix E. Reference-frame lift bookkeeping for a co-rotating guide

The main text uses a guide-relative lift screen because the guide shell's inertial speed is small compared with the slug speed in the reference case. Since that bookkeeping can be easy to misread, this appendix states the inertial-frame result explicitly and shows why the simpler expression is a good leading-order approximation for the symmetric lane pairs used in the paper.

Even a ring intended to remain stationary relative to the ground is not inertially stationary. An equatorial ring that supports ground-referenced tethers must co-rotate with Earth so that those tethers do not sweep across the surface. The guide shell therefore carries a real inertial ring-tangential speed set mainly by Earth rotation, even though the slug streams move much faster relative to the guide.

Let the local guide shell have inertial ring-tangential speed \(U_g\), and let each lane have guide-relative speed \(\sigma u\) with \(\sigma = \pm 1\) for the two travel directions. The inertial lane speed is then

\[
U_\sigma = U_g + \sigma u.
\]

If \(\dot m\) is the guide-frame mass flux in one lane, then the mass per unit guide length is \(\lambda = \dot m/u\). The outward reaction per unit guide length from that lane is therefore

\[
q_{\mathrm{lift},\sigma} = \frac{\dot m}{u}\left(\frac{(U_g+\sigma u)^2}{R} - g_h\right).
\]

For a symmetric counter-propagating pair, the sum becomes

\[
q_{\mathrm{lift,pair}} = \frac{2\dot m}{u}\left(\frac{u^2 + U_g^2}{R} - g_h\right)
= 2\dot m\left(\frac{u}{R} - \frac{g_h}{u}\right) + 2\dot m\frac{U_g^2}{uR}.
\]

So the pair-averaged lift law used in the main text,

\[
q_{\mathrm{lift,pair}} \approx 2\dot m\left(\frac{u}{R} - \frac{g_h}{u}\right),
\]

is the leading-order result when \(U_g \ll u\). The first-order \(\pm 2U_g u/R\) correction cancels between the two travel directions. For an Earth-fixed equatorial guide at 500 km altitude, \(U_g\) is about 0.50 km/s, so the retained correction is only about 0.25% of the main ring-curvature term in the reference case.

This does not solve the broader orbital-dynamics problem. Station-keeping, tether interaction, nodal precession, non-equatorial geometries, and deployment dynamics remain open. It only shows why the guide-relative lift expression used in the main text is a reasonable leading-order screen for symmetric lane pairs.
