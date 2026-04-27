# Helix Angle, Inflation, and Macro-Lift Constraints Memo

## Status
This memo adds an important missing constraint layer to the active-support tube concept.

So far we have treated two problems somewhat separately:
- local helical curvature of the rotor lanes inflates the tube and keeps the fabric taut
- macro-scale control of the tube can come from distributed slug-speed actuation and the resulting tug fields

But for an orbital-ring-like tube wrapped around Earth, there is another requirement:

The same moving mass streams must also generate enough net outward lift, through the large-radius curvature of the ring around Earth, to keep the whole tube lofted against gravity.

This memo asks how those two requirements interact through the helix angle $\alpha$.

## 1. Geometry and speed decomposition
Take a tube of radius $a$ whose centerline follows a ring of radius $R$ around Earth.
For an orbital ring at altitude $h$ above Earth,

$$R = R_E + h$$

Let a rotor lane follow a helical path on the tube with helix angle $\alpha$ measured relative to the ring tangent direction.

Let:
- $v$ = total lane speed along the helical path
- $u = v \cos\alpha$ = axial/tangential component along the ring centerline
- $v_\theta = v \sin\alpha$ = circumferential component around the tube

For a slender torus with $a \ll R$, the leading-order curvature decomposition is:
- local helical curvature on the tube:

$$\kappa_{\mathrm{loc}} \approx \frac{\sin^2\alpha}{a}$$

- macro curvature around Earth:

$$\kappa_{\mathrm{mac}} \approx \frac{\cos^2\alpha}{R}$$

The neglected cross-terms are order $a/R$, which is tiny for a 100 m tube wrapped around Earth.

## 2. Local inflation from a slug lane
For a slug train with mass flux $\dot m$ in one lane, the local guide-force density per lane length is

$$f = \dot m v \kappa$$

Applying this to the local helical curvature gives the lane-length radial support density

$$f_{\mathrm{loc}} = \dot m v \frac{\sin^2\alpha}{a}$$

To convert to force per unit ring length, multiply by the lane-length factor $\sec\alpha$.
Therefore one lane contributes local outward radial load per unit ring length

$$q_{\mathrm{loc,lane}} = \dot m v \frac{\sin^2\alpha}{a\cos\alpha}$$

Using $u = v\cos\alpha$, this simplifies nicely to

$$q_{\mathrm{loc,lane}} = \dot m u \frac{\tan^2\alpha}{a}$$

For one symmetric paired module, double it:

$$q_{\mathrm{loc,pair}} = 2 \dot m u \frac{\tan^2\alpha}{a}$$

Spread over the cylindrical surface area per ring length, $2\pi a$, the equivalent pressure from one pair is

$$p_{\mathrm{pair}} = \frac{\dot m u \tan^2\alpha}{\pi a^2}$$

If there are $N_p$ paired modules distributed around the tube, the total equivalent inflation pressure is

$$p_{\mathrm{eq}} = N_p \frac{\dot m u \tan^2\alpha}{\pi a^2}$$

This is the local-inflation constraint in the slug-train language.

## 3. Hoop force requirement for a taut fabric tube
Let the minimum required average inflation pressure to keep the fabric taut and structurally useful be $p_{\mathrm{req}}$.
Equivalently, define the required hoop membrane force per unit ring length

$$N_{\theta,\mathrm{req}} = p_{\mathrm{req}} a$$

Then the inflation requirement is

$$N_p \dot m u \frac{\tan^2\alpha}{\pi a} \ge N_{\theta,\mathrm{req}}$$

or

$$N_p \dot m u \ge \frac{\pi a N_{\theta,\mathrm{req}}}{\tan^2\alpha}$$

This is the first constraint.

## 4. Macro lift from curvature around Earth
Now consider the same lane moving along the ring around Earth.
Its macro turning load per unit ring length is

$$q_{\mathrm{turn,lane}} = \dot m \frac{u}{R}$$

because the ring-tangential component $u$ is what gets turned around Earth.

But the slug stream also has weight.
The slug mass per unit ring length is

$$\lambda_{\mathrm{slug,lane}} = \frac{\dot m}{u}$$

so the slug weight per unit ring length is

$$q_{g,\mathrm{lane}} = \lambda_{\mathrm{slug,lane}} g_h = \dot m \frac{g_h}{u}$$

where $g_h$ is gravity at ring altitude,

$$g_h = \frac{\mu_E}{R^2}$$

Therefore the **net outward lift** contributed to the tube by one lane is

$$q_{\mathrm{lift,lane}} = \dot m \left(\frac{u}{R} - \frac{g_h}{u}\right)$$

For one paired module, double it:

$$q_{\mathrm{lift,pair}} = 2 \dot m \left(\frac{u}{R} - \frac{g_h}{u}\right)$$

And for $N_p$ paired modules,

$$q_{\mathrm{lift}} = 2 N_p \dot m \left(\frac{u}{R} - \frac{g_h}{u}\right)$$

This is the second constraint.

## 5. Orbital-speed threshold
The lift expression changes sign when

$$\frac{u}{R} = \frac{g_h}{u}$$

which gives

$$u^2 = g_h R$$

Therefore the threshold speed is exactly the circular orbital speed at that altitude:

$$u_{\mathrm{orb}} = \sqrt{g_h R}$$

Interpretation:
- if $u < u_{\mathrm{orb}}$, the slug stream loads the tube downward overall
- if $u = u_{\mathrm{orb}}$, the slug stream contributes zero net lift to the tube
- if $u > u_{\mathrm{orb}}$, the slug stream lifts the tube upward

This is a very important result.

For an orbital-ring-like tube, **macro lift is controlled first by the axial/tangential component $u$, not by the helix angle alone**.

## 6. Positive-lift condition in terms of total lane speed
Because $u = v \cos\alpha$, positive lift requires

$$v \cos\alpha > u_{\mathrm{orb}}$$

So if the total slug speed $v$ is limited, the helix angle cannot be made arbitrarily steep.
The positive-lift condition becomes

$$\alpha < \arccos\left(\frac{u_{\mathrm{orb}}}{v}\right)$$

This is the hard geometric tradeoff:
- larger $\alpha$ helps inflation
- larger $\alpha$ hurts lift by stealing speed from the ring-tangential component

## 7. Passive structure weight requirement
Let the passive tube, fabric, stators, power systems, and other non-rotor hardware have weight per unit ring length

$$w_p$$

Then the lofting requirement is

$$2 N_p \dot m \left(\frac{u}{R} - \frac{g_h}{u}\right) \ge w_p$$

or, multiplying through by $u$,

$$2 N_p \dot m u \left(\frac{1}{R} - \frac{g_h}{u^2}\right) \ge w_p$$

Define the aggregate axial momentum-flux scale

$$A = N_p \dot m u$$

Then the two main constraints become:

### Inflation
$$A \ge \frac{\pi a N_{\theta,\mathrm{req}}}{\tan^2\alpha}$$

### Lift
$$A \ge \frac{w_p}{2\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}$$

This is the cleanest way to see the design trade.

## 8. What the helix angle actually does
This is now clearer than before.

### The axial speed $u$ controls lift
Lift comes from the excess of the ring-tangential speed above orbital speed.

### The helix angle $\alpha$ controls how much of that same momentum-flux budget is converted into local inflation
Inflation goes through $\tan^2\alpha$.

So the design strategy is not
"choose a big helix angle to get lift and inflation."

It is closer to
"choose enough axial speed to get lift, then choose the smallest helix angle that gives enough inflation."

That is a useful reframing.

## 9. Optimum helix angle for simultaneous satisfaction
If we want to satisfy both constraints with minimum aggregate momentum-flux $A$, the optimum occurs when the two constraints are equal:

$$\frac{\pi a N_{\theta,\mathrm{req}}}{\tan^2\alpha} = \frac{w_p}{2\left(\frac{1}{R} - \frac{g_h}{u^2}\right)}$$

Rearranging gives

$$\tan^2\alpha_{\mathrm{opt}} = 2\pi a \frac{N_{\theta,\mathrm{req}}}{w_p} \left(\frac{1}{R} - \frac{g_h}{u^2}\right)$$

Define the dimensionless structural-preload ratio

$$\Gamma = \frac{N_{\theta,\mathrm{req}}}{w_p}$$

Then

$$\tan^2\alpha_{\mathrm{opt}} = 2\pi a \Gamma \left(\frac{1}{R} - \frac{g_h}{u^2}\right)$$

If $\alpha$ is small, then

$$\alpha_{\mathrm{opt}} \approx \sqrt{2\pi a \Gamma \left(\frac{1}{R} - \frac{g_h}{u^2}\right)}$$

This is one of the key equations of the memo.

## 10. What the optimum formula implies
Because $R$ is enormous compared with $a$, and because $u$ is usually only somewhat above orbital speed, the quantity

$$\left(\frac{1}{R} - \frac{g_h}{u^2}\right)$$

is small.

Therefore the optimum helix angle is likely to be **surprisingly small** for many realistic design cases.

This means:
- the lanes may run almost axially along the ring
- only a modest circumferential component may be needed to produce enough local inflation once lift is already being provided
- the real brute-force requirement is likely the lift momentum flux, not the inflation angle

## 11. Numerical reference at 80 km altitude
Take a notional orbital ring at:
- altitude $h = 80\,\mathrm{km}$
- tube radius $a = 50\,\mathrm{m}$

Then approximately:
- $R \approx 6.45 \times 10^6\,\mathrm{m}$
- $g_h \approx 9.58\,\mathrm{m/s^2}$
- $u_{\mathrm{orb}} \approx 7.86\,\mathrm{km/s}$

Now choose a modest structural-preload ratio for illustration:

$$\Gamma = \frac{N_{\theta,\mathrm{req}}}{w_p} = 10$$

Then the optimum helix angle is approximately:
- for $u = 8.0\,\mathrm{km/s}$: $\alpha_{\mathrm{opt}} \approx 0.24^\circ$
- for $u = 10\,\mathrm{km/s}$: $\alpha_{\mathrm{opt}} \approx 0.78^\circ$
- for $u = 12\,\mathrm{km/s}$: $\alpha_{\mathrm{opt}} \approx 0.94^\circ$

If instead the preload ratio is much larger, say $\Gamma = 100$, then the optimum angle rises by about $\sqrt{10}$:
- at $u = 10\,\mathrm{km/s}$: $\alpha_{\mathrm{opt}} \approx 2.5^\circ$

These are still small angles.

This is a striking result.

It suggests that if the ring has enough moving momentum to loft itself, then only a small helical bias may be needed to keep the fabric tube taut.

## 12. A throughput sanity check
The previous result sounds encouraging, but there is a catch.

The **aggregate momentum-flux requirement for lift** can still be brutal.

Take a notional passive structure weight per ring length

$$w_p = 10\,\mathrm{kN/m}$$

and $u = 10\,\mathrm{km/s}$.
Then the lift constraint gives

$$A = N_p \dot m u \gtrsim \frac{10^4}{2\left(\frac{1}{R} - \frac{g_h}{u^2}\right)} \approx 8.4 \times 10^{10}\,\mathrm{N}$$

If there are $N_p = 150$ paired modules, then the required mass flux per pair is of order

$$\dot m \sim \frac{A}{N_p u} \approx 5.6 \times 10^4\,\mathrm{kg/s\,per\,pair}$$

That is enormous.

So the memo's honest conclusion is:

**inflation is not the hard part once lift is available. The hard part is getting enough superorbital axial momentum flux to loft the whole ring.**

## 13. Design implications
1. The helix angle should probably be treated as a trim variable, not the primary lift lever.
2. The primary lift lever is the aggregate axial momentum flux $A = N_p \dot m u$.
3. If total lane speed $v$ is capped, then the positive-lift condition constrains $\alpha$ from above.
4. Once the lift budget is met, only small helix angles may be needed for local inflation and hoop preload.
5. This strengthens the case for mirrored, nearly axial, distributed slug lanes rather than very steep helical windings.

## 14. What I would test next
The next pass should quantify:
1. passive structural weight per ring length for plausible fabric + stator + power + thermal hardware
2. how much hoop preload is actually required for useful tautness and local stiffness
3. whether multiple lane populations should be used, for example some optimized mainly for lift and others mainly for local inflation/control
4. how the distributed control architecture interacts with a very small nominal helix angle
5. whether the launch-loop and orbital-ring cases want different nominal helix angles because their macro support conditions differ drastically

## 15. Bottom line
The new constraint picture is:

- local inflation comes from the helical circumferential component
- macro lift comes from the superorbital axial component
- the same lane architecture must satisfy both

But the trade does **not** look symmetric.

My current judgment is:
- helix angle is a real and important design variable
- however, the dominant difficulty for an orbital-ring tube is likely **macro lift throughput**, not local inflation
- if the ring can already loft itself, then only a small helix angle may be needed to keep the tube taut
- therefore the first-order orbital-ring design problem is likely to be: can we afford the moving mass flux at superorbital axial speed?
