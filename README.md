# Fungi Growth Dataset: 
This dataset captures the progressive stages of fungal growth, visualized through 100 high-resolution images. The dataset is divided into three primary growth stages:

1. **Spore Stage**:
   - Small, randomly distributed spores representing the initial stage of fungi.
   - Color: Bright yellow, symbolizing the vitality of fresh spores.

2. **Hyphal Growth**:
   - Branching structures (hyphae) emerge from the spores, creating a web-like network.
   - The branches grow recursively with dynamic angles, lengths, and widths.
   - Color: Gradually transitions from yellow to orange tones.

3. **Mycelium Formation**:
   - Dense fungal networks form, completing the fungi's life cycle.
   - Growth is influenced by temperature and environmental factors.
   - Color: Deep red hues represent mature fungal structures.

### Transition

The transition between these stages is gradual, and controlled by probabilistic modeling. For example:
- Spores convert to hyphae, and hyphae transition into interconnected mycelium.
- Growth dynamics are influenced by environmental factors like **temperature** and **growth scaling**.
![Fungi Tracking](track_fungi.pdf)
---

## How the Dataset is Generated

### Recursive Branching and Growth

The fungi growth is modeled using a recursive branching function. At each branching step:
- **Branch Length**: Scaled by growth factors and randomness to mimic natural variation.
- **Branch Width**: Decreases with depth to represent thinning as branches grow further.
- **Sub-Branches**: Dynamically generated, with their number influenced by a Poisson distribution.

### Mathematical Representation

1. **Branch Length Scaling**:
It is a normal distribution with mean=1 and standard deviation=0.2.

2. **Dynamic Color Interpolation**:
The color of each growth stage is interpolated based on position or growth factor. This ensures smooth transitions from yellow to orange to red.

3. **Growth Factor**:
   The growth factor scales the transition from hyphae to mycelium.
   
5. **Recursive Depth**:
   Branching depth reduces over iterations, limiting the recursion.

---

## Dataset Features

- **Visual Transition**:
  - Early stages dominated by bright yellow spores.
  - Intermediate stages show orange branching hyphae.
  - Final stages highlight dense, red mycelium.

- **Environmental Factors**:
  - Random environmental perturbations influence branching and growth.

- **Image Resolution**:
  - High-resolution images (15x15 grid), suitable for visualization and analysis.

---
### Directory Layout
├── temp/ │ ├── fungi_transition_1.png │ ├── fungi_transition_2.png │ ├── ... │ ├── fungi_transition_100.png └── README.md


- **`temp/`**: Contains 100 images representing the progressive growth of fungi.

---

## Applications

This dataset is suitable for:
- **Machine Learning**: Training models to classify fungal growth stages.
- **Biological Simulation**: Studying growth patterns in fungi.
- **Art and Design**: Generating biologically inspired visuals.

---
## Research Paper
To support the study of these time-dependent processes, we present a synthetic, time-aligned image dataset that models key stages of fungal growth. This dataset systematically captures phenomena such as spore size reduction, branching dynamics, and the emergence of complex mycelium networks.

[SYNTHETIC FUNGI DATASETS: A TIME-ALIGNED APPROACH](2501.02855v1.pdf)

---
## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Feel free to:
- Open issues for suggestions or bugs.
- Submit pull requests for improvements or additional features.

---

## Acknowledgments

This dataset generation script is inspired by the complexity and beauty of fungal growth patterns, blending biology and computational modeling.
