# Coaxial Active Support Concept Brief

## Working concept
An active structural member based on a magnetically levitated high-speed internal rotor moving within a stationary stator.

The moving rotor carries momentum.
The stator extracts controlled support forces from the rotor through magnetic coupling.
A network of these members may be combined to support large structures that would not stand as passive compression members.

## Candidate subsystem decomposition

### 1. Rotor
Questions:
- Cable, belt, chain, segmented train, or continuous loop?
- What is the rotor material?
- What tensile strength, fatigue life, and thermal limits are required?
- What linear speed range is required?
- How is the rotor joined, spooled, serviced, and replaced?

### 2. Stator / guideway
Questions:
- What is the stator cross-section?
- What structural loads must the outer housing resist?
- How are bends, junctions, and helical sections handled?
- How is vacuum, low-pressure gas, or ambient atmosphere handled internally?

### 3. Magnetic levitation and force transfer
Questions:
- Permanent magnets, electromagnets, superconductors, or hybrids?
- What levitation gap is required?
- What control bandwidth is required?
- What field strengths and power electronics are implied?
- What is the maximum lateral and axial force density achievable?

### 4. Structural architecture
Questions:
- Single mast, guyed mast, tripod, helical bundle, inflated shell, tensegrity hybrid, or fabric tower?
- How many active members are needed?
- Where are passive load paths retained for fault tolerance?

### 5. Dynamics and control
Questions:
- What are the dominant wobble modes?
- What disturbances matter most: wind, vortex shedding, seismic input, rotor imbalance, actuator lag, thermal drift?
- Is the control problem centralized, distributed, or hierarchical?
- What states must be measured directly?
- What happens under sensor loss or delayed actuation?

### 6. Power and thermal management
Questions:
- What is steady-state power draw?
- What transient power margin is needed during disturbances?
- Where are losses generated: bearings avoided, eddy currents, resistive heating, aerodynamic drag, inverter loss?
- How is waste heat rejected?

### 7. Safety and containment
Questions:
- What happens if a rotor snaps?
- What happens if levitation fails locally?
- Can the system fail soft, or only fail hard?
- How are fragments, fire, arcing, and cascading collapse prevented?

### 8. Construction and maintenance
Questions:
- Can modules be factory-built?
- What is the field assembly sequence?
- Can the structure stand partially complete?
- How are active members serviced at height?

## First-principles unknowns
The key unknown is not just whether magnetic levitation works.
It is whether the combined rotor, stator, envelope, and control system can remain stable, efficient, maintainable, and safe at architectural scale.

## Immediate modeling priorities
1. Force density achievable from magnetic coupling
2. Rotor material and speed envelope
3. Scaling laws for support force, power, and failure energy
4. Lowest structural modes of candidate large-scale geometries
5. Control authority required to suppress wobble
6. Fault-containment strategies

## Brutal truth
This concept lives or dies on dynamics, control, and failure handling, not on seductive renderings.
