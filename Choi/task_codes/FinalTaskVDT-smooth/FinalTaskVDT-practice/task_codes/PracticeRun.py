import os
import shutil
import random
import warnings
from psychopy import visual, event, core, logging

# Suppress the warning about monitor specification not found
warnings.filterwarnings("ignore", message="Monitor specification not found.")

try:
    # Define the load_images_from_folder function
    def load_images_from_folder(win, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith(".png"):  # Only consider PNG files
                base_name = os.path.splitext(filename)[0]  # Get base name without extension
                if base_name.startswith("C") or base_name.startswith("R"):
                    img = visual.ImageStim(win, os.path.join(folder, filename), name=base_name)
                    images.append(img)
        return images

# Define stimuli folder
    stimuli_folder = "/Users/sepehrmortaheb/git_repo/Parabolic_Flight/Choi/task_codes/FinalTaskVDT-smooth/FinalTaskVDT-practice/task_codes/images2"

    # Define window size
    window_size = [1280, 720]  # Set the window size to match the screen resolution

    # Create PsychoPy window
    win = visual.Window(size=window_size, fullscr=True, units='pix', allowGUI=False)

    # Load images from folder
    stimuli_images = load_images_from_folder(win, stimuli_folder)

    # Shuffle the list of stimuli images randomly
    random.shuffle(stimuli_images)

    # Define the number of presentations for each image
    presentations_per_image = {}
    spacebar_presses_per_image = {}  # To store spacebar press counts
    for image in stimuli_images:
        if image.name.startswith('C'):
            presentations_per_image[image.name] = 1  # You can change the repetition count here
        elif image.name.startswith('R'):
            presentations_per_image[image.name] = 1  # You can change the repetition count here
        spacebar_presses_per_image[image.name] = 0  # Initialize spacebar press count

    # Initialize a text stimulus for displaying messages
    message_text = visual.TextStim(win, text="", pos=(0, 0), color="white", height=30)

    # Display instructions before starting the experiment
    instruction_text = visual.TextStim(win, text="INSTRUCTIONS:\n\n\nPress the spacebar when the ellipse appears vertically oriented.\n\nRespond as fast and accurate as possible.\n\nPress 's' when you are ready to begin.", pos=(0, 0), color="white", height=30)
    instruction_text.draw()
    win.flip()

    # Wait for 's' key press to start the experiment
    event.waitKeys(keyList=['s'])

    # Main presentation loop
    clock = core.Clock()
    for image in stimuli_images:
        num_presentations = presentations_per_image.get(image.name, 0)
        for _ in range(num_presentations):
            # Present the image for 750 ms
            image.draw()
            win.flip()
            core.wait(0.75)

            # Blank screen for 250 ms
            win.flip()
            core.wait(0.25)

            # Check for spacebar press within the 1-second interval
            for _ in range(60):  # 60 frames assuming 60Hz refresh rate
                keys = event.getKeys(keyList=['space', 'escape', 'q'])
                if 'escape' in keys:
                    raise KeyboardInterrupt  # Exit the program if escape is pressed
                elif 'q' in keys:
                    raise StopIteration  # Stop the experiment prematurely if 'q' is pressed
                elif 'space' in keys:
                    spacebar_presses_per_image[image.name] += 1  # Increment spacebar press count
                core.wait(1.0 / 60)  # Wait for 1/60th of a second

    # Calculate unique base image names and their total spacebar presses
    base_name_presses = {}
    for image_name, count in spacebar_presses_per_image.items():
        if count > 0:
            base_name = image_name.split('_',1)[0]
            if base_name in base_name_presses:
                base_name_presses[base_name] += count
            else:
                base_name_presses[base_name] = count

    # Display total spacebar press counts for each unique base image
    final_message = "Practice session finished.\nTotal spacebar press counts per image:\n\n"
    for base_name, total_presses in base_name_presses.items():
        final_message += f"{base_name}: {total_presses} spacebar press(es)\n"

    message_text.text = final_message
    message_text.draw()
    win.flip()
    event.waitKeys()

except KeyboardInterrupt:
    print("Experiment terminated by user.")
except StopIteration:
    print("Experiment stopped by user.")
except Exception as e:
    logging.error(f"Error: {e}")

finally:
    # Close the PsychoPy window
    win.close()










