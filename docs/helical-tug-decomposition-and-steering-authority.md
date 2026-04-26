# Helical Tug Decomposition and Steering Authority Memo

## Status
First-pass memo following Hudson's observation that macro control may come less from pressure in the selected fast section and more from the momentum reactions at the section boundaries.

The goal here is to answer a narrower question:

If a paired slug-train module is built from mirrored helices, what direction do the boundary tug forces actually point, and what kind of macro-scale control authority do they plausibly create?

## 1. Geometry and notation
Take a cylindrical tube of radius $a$ with axis along $z$.
Use the standard local cylindrical basis:
- $\mathbf{e}_r$ radial outward
- $\mathbf{e}_\theta$ circumferential
- $\mathbf{e}_z$ axial

Let the helix angle $\alpha$ be measured relative to the tube axis.
Then the unit tangent vectors for the two mirrored helix families are:

$$\mathbf{t}_{R+} = \cos\alpha \, \mathbf{e}_z + \sin\alpha \, \mathbf{e}_\theta$$
$$\mathbf{t}_{R-} = -\cos\alpha \, \mathbf{e}_z - \sin\alpha \, \mathbf{e}_\theta$$
$$\mathbf{t}_{L+} = \cos\alpha \, \mathbf{e}_z - \sin\alpha \, \mathbf{e}_\theta$$
$$\mathbf{t}_{L-} = -\cos\alpha \, \mathbf{e}_z + \sin\alpha \, \mathbf{e}_\theta$$

where:
- $R/L$ denotes right-handed / left-handed helix family
- $+/-$ denotes direction of travel with positive/negative axial component

## 2. The correct mirrored traveling pair for axial tug
For the boundary-tug concept, the useful pairing is:
- one lane traveling through the selected section on $\mathbf{t}_{R+}$
- the other lane traveling through the selected section on $\mathbf{t}_{L-}$

These are mirrored helices with opposite axial directions.

Their tangent vectors are:

$$\mathbf{t}_x = \mathbf{t}_{R+} = \cos\alpha \, \mathbf{e}_z + \sin\alpha \, \mathbf{e}_\theta$$
$$\mathbf{t}_y = \mathbf{t}_{L-} = -\cos\alpha \, \mathbf{e}_z + \sin\alpha \, \mathbf{e}_\theta$$

Important property:
- axial components are opposite
- circumferential components are equal

This turns out to be exactly what is needed for the boundary tug decomposition.

## 3. Boundary station force law
If a lane with mass flux $\dot m$ changes speed magnitude by $\Delta v = v_1 - v_0$ across a boundary station while keeping the same tangent direction $\mathbf{t}$ through that station, the reaction on the stator is

$$\mathbf{F}_{\mathrm{react}} = -\dot m \, \Delta v \, \mathbf{t}$$

for an acceleration station, and

$$\mathbf{F}_{\mathrm{react}} = +\dot m \, \Delta v \, \mathbf{t}$$

for a deceleration station.

At boundary $A$ of a selected fast section:
- lane $x$ is accelerated from $v_0$ to $v_1$
- lane $y$ is decelerated from $v_1$ to $v_0$

So

$$\mathbf{F}_{A,x} = -\dot m \, \Delta v \, \mathbf{t}_x$$
$$\mathbf{F}_{A,y} = +\dot m \, \Delta v \, \mathbf{t}_y$$

and therefore

$$\mathbf{F}_A = \dot m \, \Delta v \, (\mathbf{t}_y - \mathbf{t}_x)$$

Substitute the mirrored tangents:

$$\mathbf{t}_y - \mathbf{t}_x = (-\cos\alpha \, \mathbf{e}_z + \sin\alpha \, \mathbf{e}_\theta) - (\cos\alpha \, \mathbf{e}_z + \sin\alpha \, \mathbf{e}_\theta)$$

so

$$\mathbf{t}_y - \mathbf{t}_x = -2 \cos\alpha \, \mathbf{e}_z$$

Hence

$$\mathbf{F}_A = -2 \dot m \, \Delta v \, \cos\alpha \, \mathbf{e}_z$$

Similarly at the far boundary $B$,

$$\mathbf{F}_B = +2 \dot m \, \Delta v \, \cos\alpha \, \mathbf{e}_z$$

This is the first major result.

For the mirrored helical pair, the boundary tug is **purely axial**.
The circumferential components cancel exactly at first order.

## 4. Why that cancellation is so good
This is exactly what we want from a clean actuator.

The boundary station pair gives:
- no first-order twist injection into the tube
- no first-order circumferential drive
- a clean axial load transfer channel

So the paired mirrored helix is not just aesthetically symmetric.
It gives the right control-vector decomposition.

## 5. What happens if the pairing is wrong
If a different local pairing is chosen, the force decomposition changes.

Example: pair $\mathbf{t}_{R+}$ with $\mathbf{t}_{R-}$.
Then

$$\mathbf{t}_{R-} - \mathbf{t}_{R+} = -2 \cos\alpha \, \mathbf{e}_z - 2 \sin\alpha \, \mathbf{e}_\theta$$

which means the station injects both:
- axial tug
- circumferential twist drive

That is probably undesirable for a macro-control primitive.

So the mirrored-helix pairing is not optional detail.
It is part of making the actuator clean.

## 6. Tug authority of one paired module
The magnitude of the axial boundary tug from one paired module is

$$F_{\mathrm{tug,1}} = 2 \dot m \, \Delta v \, \cos\alpha$$

where:
- $\dot m$ is the mass flux in each lane
- $\Delta v = v_1 - v_0$ is the speed increase inside the selected section

If $N_s$ paired modules are modulated together in one azimuthal sector, the total axial tug is

$$F_{\mathrm{tug,sector}} = 2 N_s \dot m \, \Delta v \, \cos\alpha$$

This is the basic steering-force scale.

## 7. Pressure change in the same selected section
From the previous slug-train memo, for fixed mass flux the local support-force density and pressure scale linearly with speed.
So if the baseline speed is $v_0$ and the selected section speed is $v_1 = v_0 + \Delta v$, then to first order

$$\frac{\delta p}{p_0} \approx \frac{\Delta v}{v_0}$$

for a slug train with fixed mass flux.

That means the same command does two things at once:
- creates a distributed pressure increase inside the selected section
- creates concentrated axial tug forces at the section boundaries

So the control primitive is a hybrid one, not a pure pressure actuator.

## 8. Straight-tube interpretation
For a straight long tube, the boundary tug pair is an internal axial force dipole:
- one station pulls one way
- the other pulls the opposite way

This can:
- redistribute axial load
- stretch/compress selected long regions in a controlled way
- couple into global bending if applied asymmetrically around the circumference

But it does not create a net external force on the whole structure.

## 9. Cross-section bending moment from sector actuation
Suppose the boundary tug is applied not uniformly around the whole circumference, but in a sector centered at azimuth $\phi$.
The local position vector of that sector is

$$\mathbf{r}(\phi) = a \, \mathbf{e}_r(\phi)$$

and the axial tug there is

$$\mathbf{F}(\phi) = F_{\mathrm{sector}} \, \mathbf{e}_z$$

The bending moment about the tube centerline is

$$\mathbf{M}(\phi) = \mathbf{r}(\phi) \times \mathbf{F}(\phi) = a F_{\mathrm{sector}} \, (\mathbf{e}_r \times \mathbf{e}_z)$$

So the magnitude is

$$M = a F_{\mathrm{sector}}$$

This is the second major result.

If axial tug is applied preferentially on one side of the tube, it creates a bending moment of order

$$M_{\mathrm{bend}} \sim a F_{\mathrm{tug,sector}}$$

For the paired mirrored modules,

$$M_{\mathrm{bend}} \sim 2 a N_s \dot m \, \Delta v \, \cos\alpha$$

That is the first clean estimate of steering authority in the local-structure sense.

## 10. What this means for macro control
This clarifies the control story a lot.

### Mode A: Uniform actuation around the circumference
If all sectors are commanded equally, the boundary stations create mostly axial load transfer and pressure changes, but no net bending moment of the cross-section.

This is useful for:
- global pressure adjustment
- load redistribution
- tension management along the long axis

### Mode B: Differential azimuthal actuation
If one side of the circumference is commanded harder than the other, then the boundary stations create a net bending moment.

This is useful for:
- steering
- sway correction
- long-wavelength shape control

This looks like a serious and useful actuation basis.

## 11. Curved ring interpretation
For an orbital ring, the tube axis itself is a closed curved path around Earth.
So an "axial" tug is really a tangential tug along the ring.

That means the boundary stations can:
- redistribute tangential load around the ring
- feed or absorb force at the places where external supports or tethers exist
- generate controlled spatial variations in tangential force that couple into ring shape through curvature and constraint geometry

So even though the tug is internal in the local tube coordinates, it can still be highly relevant to planetary-scale steering and stabilization.

This is especially important if grounded tether points are sparse.
The ring may need a way to transport control forces to and from those sparse external anchor locations, and axial/tangential tug stations look like a plausible mechanism.

## 12. Worked symbolic scaling summary
For one modulated sector of mirrored paired slug modules:

### Boundary tug
$$F_{\mathrm{tug}} \sim 2 N_s \dot m \, \Delta v \, \cos\alpha$$

### Sector bending moment
$$M_{\mathrm{bend}} \sim 2 a N_s \dot m \, \Delta v \, \cos\alpha$$

### Relative pressure change inside the section
$$\frac{\delta p}{p_0} \sim \frac{\Delta v}{v_0}$$

These are the three equations I would keep on the wall from this memo.

## 13. Design implications
1. Mirrored helices are not just for balancing support torque. They also create a clean axial tug channel.
2. Discrete slug trains remain much better suited than continuous cables for this kind of localized speed-pattern actuation.
3. Boundary stations are probably primary actuators, not just support hardware.
4. Macro control may work by commanding spatial patterns in sector tug forces, not only by commanding average pressure.
5. Demonstrator experiments should include explicit tug-station tests, not only inflation tests.

## 14. What I would test next
The next pass should derive or simulate:
1. finite-width azimuthal sectors rather than point-sector approximations
2. transient filling and draining of the fast section
3. realistic actuator power and regenerative coupling at the two boundaries
4. closed-loop bending control of a finite tube segment using opposed sectors
5. how tangential tug patterns on a curved ring couple into ring-shape correction and tether load transfer

## 15. Bottom line
The picture is now much cleaner.

For the mirrored paired helical slug architecture:
- the selected fast section creates higher local support pressure
- the boundary stations create clean axial momentum tugs
- those axial tugs can be turned into bending moments by azimuthally selective actuation
- in an orbital ring, the same tugs become tangential load-transfer actuators around the ring

My current judgment is:
- Hudson's boundary-tug intuition was correct and important
- the mirrored helical pairing gives exactly the kind of vector cancellation we want
- the macro-control problem is starting to look less like mysterious "steering pressure" and more like a distributed internal actuation system with well-defined force channels
