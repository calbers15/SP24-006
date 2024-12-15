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
threshold_yellow = 1.4  # Threshold for transitioning from green to yellow
threshold_red = 2.55    # Threshold for transitioning from yellow to red

# Initialize a displayio group to hold the background color
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_tile = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)
group = displayio.Group()
group.append(color_tile)
display.root_group = group  # Set the root group to show the background color


# Helper function to blend between two colors

def get_voltage(pin):
    return (pin.value / 65536) * 3.3

def sample_signal(signal, samples=5000):
    return sum(signal[:samples]) / samples

def find_delta(signal):
    return max(signal) - min(signal)

# Main loop: control transitions based on analog input
while True:
    signal = [get_voltage(analog_input) for _ in range(5000)]
    ########################DEBUG##################################
    #sensor_value = sample_signal(get_voltage(analog_input))      # 
    #sensor_value = get_voltage(analog_input)                     #
    #print("Sensor value is: ", sensor_value)                     #
    #print((sensor_value,))                                       #
    ###############################################################
    sensor_delta = find_delta(signal)
    print("Sensor delta is: ", sensor_delta)
    print((sensor_delta,))

    if sensor_delta < threshold_yellow:
        color_palette[0] = (0, 90, 0)
    elif threshold_yellow < sensor_delta < threshold_red:
        color_palette[0] = (90, 90, 0)
        time.sleep(1)

    else:
        color_palette[0] = (90, 0, 0)
        time.sleep(1)



    # Check the current state and sensor value

    # Short delay to avoid rapid polling
    time.sleep(.1)
