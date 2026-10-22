<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="assets/header-ocean-static.png">
    <img src="assets/header-ocean.gif" alt="Nam Tran — Hardware and embedded systems. Nanotechnology Engineering, University of Waterloo. Animated underwater flowers, jellyfish and bubbles." width="100%">
  </picture>
</p>

Trying to get better at hardware designing :DD

<p>
  <a href="#selected-projects">Selected projects</a> &nbsp; / &nbsp;
  <a href="#industry-experience">Industry experience</a> &nbsp; / &nbsp;
  <a href="#tools-i-work-with">Tools</a>
</p>

## Selected projects

### 01 · 48 V Rover Protection Board

<table>
<tr>
<td width="45%" valign="top">
<a href="https://github.com/macnamtran/ProtectionGateDriver">
<img src="https://raw.githubusercontent.com/macnamtran/ProtectionGateDriver/main/images/layout-iteration-2-3d.png" alt="CAD rendering of the second 48 V rover protection board layout; not fabricated" width="420">
</a>
<sub>Iteration 2 · CAD preview</sub>
</td>
<td width="55%" valign="top">
<p><strong>Switching and protection for one rover wheel module.</strong></p>
<p>I’m developing a low-side NMOS power-switch board with a 3.3 V STM32 enable interface, external 12 V gate-drive supply, fuse, bus TVS and gate-source clamp.</p>
<p>The work includes schematic capture, a project-local MOSFET footprint and a four-layer layout with attention to the gate-drive loop, power-current paths and ground connections.</p>
<p><sub>KiCad · MOSFET gate drive · Power distribution · PCB layout</sub></p>
<p><strong>Status:</strong> Second layout iteration; review and bench validation pending. Not released for fabrication.</p>
<a href="https://github.com/macnamtran/ProtectionGateDriver">Explore design files →</a>
</td>
</tr>
</table>

### 02 · 3.3 V LDO Power Supply

<table>
<tr>
<td width="45%" valign="top">
<a href="https://github.com/macnamtran/TLV767_LDO">
<img src="https://raw.githubusercontent.com/macnamtran/TLV767_LDO/main/images/3D.png" alt="CAD rendering of the TLV767 LDO board; not fabricated" width="420">
</a>
<sub>TLV767 · CAD preview</sub>
</td>
<td width="55%" valign="top">
<p><strong>A 5 V-to-3.3 V supply, from datasheet to transient simulation.</strong></p>
<p>I designed the schematic and PCB around TI’s adjustable TLV767 regulator, selected the feedback divider and evaluated startup and load-step response in PSpice.</p>
<p>A nominal 10–100 mA load step with a 1 µs edge produced approximately <strong>10.6 mV dip</strong> and <strong>11.0 mV overshoot</strong> in simulation. The repository includes waveforms, settings and rule-check reports.</p>
<p><sub>KiCad · PSpice · Analog circuits · Power supplies</sub></p>
<p><strong>Status:</strong> Schematic, layout and nominal simulations prepared; fabrication and bench testing pending.</p>
<a href="https://github.com/macnamtran/TLV767_LDO">Explore design and simulation →</a>
</td>
</tr>
</table>

### 03 · ESP32 Selective Lighting Prototype

**Exploring camera-based zone detection and wireless LED control.**

I developed Arduino C++ sketches for red-marker detection, left/centre/right classification and three-channel LED control over ESP-NOW. The camera-processing and wireless-control tests are documented separately in the repository; their combined integration remains the next documented milestone.

<sub>ESP32 · C++ / Arduino · ESP-NOW · Camera processing · GPIO</sub>

[Explore firmware and test plan →](https://github.com/macnamtran/MatrixLEDSystem)

## Industry experience

### KA Imaging

**Detector testing, automation and board debugging**

- Built a Python detector-verification tool around a vendor SDK for configuration, image capture and test reporting.
- Worked on configuration readback, error handling and repeatable test sequences.
- Used continuity checks, current-limited voltage injection and thermal imaging to investigate board faults and support repairs.

### Teledyne DALSA

**Camera characterization and test development**

- Built and validated a light-uniformity station for camera pixel-defect testing.
- Developed Python test cases and TestStand sequences, checking illumination conditions and repeatability.

### TechInsights

**Transistor-level circuit analysis**

- Identified more than 50 logic cells in advanced-node semiconductor layouts.
- Reconstructed CMOS schematics and hierarchical circuit relationships using KLayout and internal analysis tools.
- Communicated findings through technical reports and diagrams.

## Tools I work with

| Area | Tools and experience |
| :--- | :--- |
| Circuit design and layout | KiCad, Altium, PSpice, KLayout |
| Embedded and automation | Python, C/C++, ESP32, Arduino, PlatformIO, TestStand |
| Bench work | Oscilloscope, multimeter, bench supply, function generator, soldering and rework, thermal imaging |
| Engineering workflow | Git / GitHub, technical documentation, SOLIDWORKS |

---

<sub>Currently developing my PCB design and hardware-validation skills. Project repositories contain the current files, results and limitations.</sub>
