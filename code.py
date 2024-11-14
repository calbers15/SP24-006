import time
import board
import displayio
import analogio
from adafruit_matrixportal.matrix import Matrix

# Initialize the matrix
matrix = Matrix()
display = matrix.display


# Set up the analog input pin (e.g., A1)
analog_input = analogio.AnalogIn(board.A1)
threshold_yellow = 2  # Threshold for transitioning from green to yellow
threshold_red = 3     # Threshold for transitioning from yellow to red

# Initialize a displayio group to hold the background color
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_tile = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)
group = displayio.Group()
group.append(color_tile)
display.root_group = group  # Set the root group to show the background color


# Smooth transition settings
transition_steps = 100  # Number of steps for smooth transition
step_delay = 0.05       # Delay per step

# Helper function to blend between two colors
def blend_colors(color1, color2, blend_factor):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * blend_factor)
    g = int(g1 + (g2 - g1) * blend_factor)
    b = int(b1 + (b2 - b1) * blend_factor)
    return (r << 16) | (g << 8) | b

def get_voltage(pin):
    return (pin.value / 65536) * 3.3

def sample_signal(analog_input):
    samples = []        # declare a list for sampling our inputs
    sample_size = 10    # set the sample size
    for i in range(sample_size):
        sample = analog_input  # grab the voltage from analog pin
        samples.append(sample)              # add the voltage to the list of samples
    return sum(samples) / len(samples)      # return the average of the

# Variable to track current state
current_state = "green"

# Main loop: control transitions based on analog input
while True:
    sensor_value = sample_signal(get_voltage(analog_input))

    print("Sensor value is: ", sensor_value)
    print((sensor_value,))
    
    if sensor_value < threshold_yellow:
        color_palette[0] = (0, 255, 0)
    elif sensor_value > threshold_yellow and sensor_value < threshold_red:
        color_palette[0] = (255, 255, 0)
    else:
        color_palette[0] = (255, 0, 0)
        time.sleep(.05)
        color_palette[0] = (255, 255, 0)
    
    

    # Check the current state and sensor value

    # Short delay to avoid rapid polling
    time.sleep(1)
