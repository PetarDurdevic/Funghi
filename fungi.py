import matplotlib.pyplot as plt
import numpy as np
import os
import random

# Color interpolation function with clamping
def interpolate_color(start_color, end_color, position):
    r = start_color[0] + (end_color[0] - start_color[0]) * position
    g = start_color[1] + (end_color[1] - start_color[1]) * position
    b = start_color[2] + (end_color[2] - start_color[2]) * position
    return (np.clip(r, 0, 1), np.clip(g, 0, 1), np.clip(b, 0, 1))

# Recursive branching function for generating mycelium and hyphae
def generate_randomized_branch(ax, x, y, branch_length, angle, depth, branch_width, color, num_initial_branches, temperature_factor, growth_factor):
    if depth == 0 or branch_length < 0.005:
        return

    # Scale branch length based on growth factor
    branch_length *= 0.7 * np.random.normal(1, 0.2)
    end_x = x + branch_length * np.cos(angle)
    end_y = y + branch_length * np.sin(angle)
    ax.plot([x, end_x], [y, end_y], color=color, alpha=0.8, linewidth=branch_width)

    # Dynamically control sub-branching and branch depth
    num_sub_branches = np.random.poisson(3)
    new_branch_length = branch_length * (0.4 + np.random.uniform(0, 0.2))  * temperature_factor
    new_branch_width = branch_width * (0.6 + np.random.uniform(0, 0.4)) 

    for _ in range(num_sub_branches):
        new_angle = np.random.uniform(0, 2 * np.pi)
        generate_randomized_branch(ax, end_x, end_y, new_branch_length, new_angle, depth - 1, new_branch_width, color=color, num_initial_branches=0, temperature_factor=temperature_factor, growth_factor=growth_factor)

    # Initial branches, scaled by growth factor
    if num_initial_branches > 0:
        for _ in range(int(num_initial_branches * growth_factor)):
            new_angle = np.random.uniform(0, 2 * np.pi)
            generate_randomized_branch(ax, x, y, branch_length, new_angle, depth - 1, branch_width, color=color, num_initial_branches=0, temperature_factor=temperature_factor, growth_factor=growth_factor)

# Function to generate spore images
def generate_spore_image(ax, spores, num_spores=10, size_factor=1.0):
    for i in range(num_spores):
        if i < len(spores): 
         x, y = spores[i]
        color = interpolate_color((1, 1, 0), (1, 0.8, 0.3), y)
        spore_circle = plt.Circle((x, y), 0.02* size_factor, color=color)
        ax.add_patch(spore_circle)

# Function to generate hyphae with branching
def generate_hyphae_image(ax, hyphae_positions, num_hyphae=10, temperature_factor=1.0, growth_factor=0.5, size_factor=1.0):
    for x, y in hyphae_positions:
        color = interpolate_color((1, 0.8, 0.3), (1, 0.5, 0), y)
        hypha_circle = plt.Circle((x, y), 0.006 * size_factor, color=color)
        ax.add_patch(hypha_circle)
        generate_randomized_branch(
            ax, 
            x, 
            y, 
            branch_length=0.06 * size_factor,  # Scale branch length
            angle=np.random.uniform(0, 2 * np.pi), 
            depth=3, 
            branch_width=2 * size_factor,  # Scale branch width
            color=color, 
            num_initial_branches=4, 
            temperature_factor=temperature_factor, 
            growth_factor=growth_factor
        )
# Function to generate mycelium with gradual growth
def generate_mycelium_image(ax, mycelium_positions, num_mycelium=10, growth_factor=0.5, temperature_factor=1.0):
    for x, y in mycelium_positions:
        color = interpolate_color((1, 0.5, 0), (1, 0, 0), growth_factor)
        mycelium_circle = plt.Circle((x, y), 0.004 * (0.5 + growth_factor), color=color)
        ax.add_patch(mycelium_circle)
        branch_length = 0.02 + growth_factor * 0.18
        depth = 4
        generate_randomized_branch(ax, x, y, branch_length=branch_length, angle=np.random.uniform(0, 2 * np.pi), depth=depth, branch_width=2 * (0.5 + growth_factor), color=color, num_initial_branches=int(3 + growth_factor * 10), temperature_factor=temperature_factor, growth_factor=growth_factor)

# Main function to generate transition images
def generate_fungi_transition_images(output_dir, num_images=100, num_spore_only_images=5):
    temp_dir = os.path.join(output_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    all_images = []

    # Initial spore positions
    spores = [(np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9)) for _ in range(20)]
    hyphae_positions = []
    mycelium_positions = []

    for i in range(num_images):
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Compute the transition ratio
        transition_ratio = i / (num_images - 1)

        # Compute the number of spores, hyphae, and mycelium
        num_spores = int(len(spores) * (1 - transition_ratio))  # Fewer spores over time
        num_hyphae = int(len(hyphae_positions) * (1 - transition_ratio * 0.5))  # Gradually reduce hyphae count
        num_mycelium = int(len(hyphae_positions) * transition_ratio * 0.5)  # Increase mycelium count

        # Convert spores to hyphae gradually
        if transition_ratio > 0.1 and len(spores) > 0:
            num_to_convert = max(1, int(len(spores) * transition_ratio * 0.1))  # Few spores transition each step
            hyphae_positions.extend(spores[:num_to_convert])  # Add to hyphae
            spores = spores[num_to_convert:]  # Remove from spores

        # Convert hyphae to mycelium gradually
        if transition_ratio > 0.5 and len(hyphae_positions) > 0:
            num_to_convert = max(1, int(len(hyphae_positions) * (transition_ratio - 0.5) * 0.1))  # Gradual transition
            mycelium_positions.extend(hyphae_positions[:num_to_convert])  # Add to mycelium
            hyphae_positions = hyphae_positions[num_to_convert:]  # Remove from hyphae

        # Size factors for spores, hyphae, and mycelium
        spore_size_factor = max(0, 1 - transition_ratio * 1.2)  # Gradually reduce spore size
        hyphae_size_factor = 1 - transition_ratio * 0.5  # Hyphae shrink over time
        growth_factor = min(1, max(0, transition_ratio - 0.5) * 2)  # Growth factor for mycelium

        # Generate spores, hyphae, and mycelium
        generate_spore_image(ax, spores, num_spores=num_spores, size_factor=spore_size_factor)
        generate_hyphae_image(
            ax, 
            hyphae_positions, 
            num_hyphae=num_hyphae, 
            temperature_factor=np.random.normal(1.0, 0.1), 
            growth_factor=transition_ratio, 
            size_factor=hyphae_size_factor
        )
        generate_mycelium_image(
            ax, 
            mycelium_positions, 
            num_mycelium=num_mycelium, 
            growth_factor=growth_factor, 
            temperature_factor=np.random.normal(1.0, 0.1)
        )

        # Save the image
        image_filename = f"fungi_transition_{i+1}.png"
        image_path = os.path.join(temp_dir, image_filename)
        fig.savefig(image_path, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        all_images.append(image_path)

        # Update spore positions (optional, for animation effect)
        spores = [(x + np.random.uniform(-0.01, 0.01), y + np.random.uniform(-0.01, 0.01)) for x, y in spores]

    print(f"Generated {len(all_images)} images in {output_dir}")
    return all_images


# Specify the main output directory
output_dir = "/home/dnn/git/CLIP_July/dataset/dataset_fungi_abs"  # Replace with your preferred path

# Generate and save images showing fungi transition from spores to hyphae to mycelium gradually
image_paths = generate_fungi_transition_images(output_dir, num_images=100, num_spore_only_images=5)
print(f"Images saved to {output_dir}/temp")