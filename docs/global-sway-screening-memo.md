# Global Sway Screening Memo

## Status
First-pass global sway screening for a tall helical active-support tube.
The goal is not a final wind design.
The goal is to establish whether global lateral loading is plausibly small, manageable, or overwhelmingly dominant for the landmark-scale demonstrator idea.

## 1. Why this memo exists
Previous work suggests:
- helical rotor inflation can create real equivalent pressure
- that pressure mainly stabilizes cross-section and local shell shape
- global bending and sway remain likely architecture gates

This memo turns that into back-of-envelope numbers.

## 2. Reference geometry
Take a notional demonstrator:
- height H = 2000 m
- diameter D = 100 m
- radius a = 50 m
- projected width to wind = D

We do not yet assume a particular fabric or truss mass.
The point here is loading scale, not final structural capacity.

## 3. Simple distributed wind load model
Use the classical drag estimate

w = (1/2) ρ_air C_D D U^2

where:
- w is lateral load per unit height (N/m)
- ρ_air ≈ 1.225 kg/m^3
- C_D is drag coefficient
- D is projected width
- U is wind speed

Take representative values:
- C_D = 1.0 as a blunt-envelope first pass
- D = 100 m

Then

w ≈ 61.25 U^2  N/m

with U in m/s.

Examples:
- U = 10 m/s -> w ≈ 6.1 kN/m
- U = 20 m/s -> w ≈ 24.5 kN/m
- U = 30 m/s -> w ≈ 55.1 kN/m
- U = 40 m/s -> w ≈ 98.0 kN/m
- U = 50 m/s -> w ≈ 153.1 kN/m

These are very large loads because the structure is very large.

## 4. Base shear and overturning moment for a cantilever-like tower
If w is uniform with height, then base shear is

V = w H

and base moment is

M = w H^2 / 2

For H = 2000 m:
- at U = 20 m/s: V ≈ 49 MN, M ≈ 49 GN·m
- at U = 30 m/s: V ≈ 110 MN, M ≈ 110 GN·m
- at U = 40 m/s: V ≈ 196 MN, M ≈ 196 GN·m

This is the core result of the memo.
A two-kilometer, 100-meter-diameter exposed structure lives in a regime of enormous overturning moments.

## 5. What equivalent internal pressure would be required to balance wind purely as membrane action?
This is not the correct full structural model, but it is a useful scaling check.
Suppose we try to resist lateral load only by pressure-created membrane force in the shell.
The characteristic hoop membrane force per unit height from internal equivalent pressure p_eq is

N_theta = p_eq a

Using the earlier example p_eq ≈ 13.5 kPa and a = 50 m gives

N_theta ≈ 675 kN/m

That sounds large, but compare it to wind loads:
- 20 m/s wind: w ≈ 24.5 kN/m
- 30 m/s wind: w ≈ 55.1 kN/m
- 40 m/s wind: w ≈ 98.0 kN/m

The hoop force is much larger than local lateral load per meter.
At first glance that sounds promising.

But this is misleading if taken too literally.
High hoop prestress does not directly cancel global overturning moment the way a rigid beam section would.
It mostly preserves shape and enables membrane stress redistribution.
The real issue is not simply whether p_eq a exceeds w locally.
The issue is whether the whole tall structure can develop a stable global load path for accumulated overturning moment.

## 6. Equivalent guy-force scale
Suppose instead we use guying at the top or near the top with lever arm L_g.
The required horizontal guy resultant to balance moment M is roughly

F_g ≈ M / L_g

If a guy system anchors with effective lever arm L_g ≈ 2000 m, then:
- 20 m/s case -> F_g ≈ 24.5 MN
- 30 m/s case -> F_g ≈ 55 MN
- 40 m/s case -> F_g ≈ 98 MN

Split across, say, 8 primary guys, that is:
- about 3.1 MN per guy at 20 m/s
- about 6.9 MN per guy at 30 m/s
- about 12.3 MN per guy at 40 m/s

These are large, but much more imaginable than asking an inflated fabric tube alone to absorb the entire overturning load as a free-standing column.

## 7. First architectural conclusion
This screening strongly supports the following conclusion:

A 2 km demonstrator is very unlikely to be sensible as a free-standing pressurized fabric tube whose only stiffness comes from helical active inflation.

Much more plausible options are:
- a guyed inflated active tube
- an inflated envelope wrapped around a deeper active-support truss
- a lower-height demonstrator if free-standing behavior is desired

## 8. Dynamic amplification warning
The numbers above are static-like mean-load estimates.
Real wind response may be worse because of:
- gusting
- vortex shedding
- aeroelastic coupling
- mode-locking with global sway modes
- active-system delay coupling into shell motion

So these loads should be interpreted as baseline, not worst-case.

## 9. What height scaling does to us
For fixed diameter and drag coefficient:
- distributed wind load per meter is proportional to U^2
- base moment scales as H^2

That H^2 scaling is brutal.
It means the leap from 200 m to 2000 m is not just 10x harder globally. It is about 100x harder in overturning moment.

This strongly argues for a laddered demonstrator program:
- tens of meters
- low hundreds of meters
- perhaps several hundred meters with guying
- only then consider kilometer scale

## 10. Back-solve for a more plausible early landmark size
If we reduce height from 2000 m to 300 m with the same diameter and wind model, base moment scales by (300/2000)^2 ≈ 0.0225.

So the 30 m/s case drops from about 110 GN·m to about 2.48 GN·m.
That is still large, but vastly more approachable.

A 500 m class structure would still be ambitious while being much less absurd as a first public landmark than 2000 m.

## 11. Relation to Eiffel-Tower framing
Hudson's Eiffel Tower analogy is strategically right, but the engineering lesson may be:

The first public landmark should probably be tall enough to create the "impossible" visual effect, but not so tall that global wind overturning dominates every other question.

That suggests a sweet spot may exist in the few-hundred-meter regime rather than immediately at 2 km.

## 12. Bottom line
The global-load sanity check is clear:
- helical active inflation can plausibly stabilize section and create useful prestress
- it does not make 2 km of exposed structure globally easy
- wind overturning is likely the principal architecture gate for a landmark demonstrator
- guying or a deeper macrostructure looks strongly favored
- a lower first-landmark height is probably the more credible path

My current judgment is:
- the technology may still be profound
- but the first flagship public structure should probably be sized by global wind sanity, not just by ambition
