from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, CheckboxGroup, Button, ColumnDataSource
from bokeh.plotting import figure
import numpy as np



def generate_clear_harmonic(
    amplitude,
    frequency,
    phase
):
    x_start = 0
    x_end = 10
    sampling_rate = 1000

    x = np.linspace(x_start, x_end, sampling_rate) #, endpoint=True)
    clear_harmonic = amplitude * np.sin(2 * np.pi * frequency * x + phase)
    return x, clear_harmonic



def generate_noise(
    noise_mean,
    noise_covariance,
    shape
):
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), shape)
    return noise

initial_amplitude = 2.0
initial_frequency = 4.5
initial_phase = 0
initial_noise_mean = 0
initial_noise_covariance = 0.1 
initital_show_noise = [0]


x, y = generate_clear_harmonic(
    initial_amplitude,
    initial_frequency,
    initial_phase
)

source = ColumnDataSource(data={'x': x, 'y': y})
initial_noise = generate_noise(initial_noise_mean, initial_noise_covariance, x.shape)

p = figure(
    height=500,
    width=1000,
    title="Harmonic graph",
    x_axis_label="X",
    y_axis_label="Y")

points = p.line('x', 'y', source=source)

amplitude_slider = Slider(
    start=-5,
    end=5,
    value=initial_amplitude,
    step=0.1,
    title="Amplitude",
)

frequency_slider = Slider(
    start=-10,
    end=10,
    value=initial_frequency,
    step=0.1,
    title="Frequency",
)

phase_slider = Slider(
    start=0,
    end=2*np.pi,
    value=initial_phase,
    step=0.1,
    title="Phase",
)

noise_mean_slider = Slider(
    start=0,
    end=1,
    value=initial_noise_mean,
    step=0.1,
    title="Noise mean",
)

noise_covariance_slider = Slider(
    start=0,
    end=1,
    value=initial_noise_covariance,
    step=0.1,
    title="Noise covarance",
)

show_noise_checkbox = CheckboxGroup(
    labels=["Show Noise"],
    active=initital_show_noise
)

reset_button = Button(
    label="Reset",
    button_type="success"
)


def update_data(attr, old, new):
    amplitude = amplitude_slider.value
    frequency = frequency_slider.value
    phase = phase_slider.value
    show_noise = show_noise_checkbox.active

    x, y = generate_clear_harmonic(amplitude, frequency, phase)
    y = y + initial_noise if show_noise else y
    source.data = {'x': x, 'y': y}

def update_noise(attr, old, new):
    global initial_noise
    noise_mean = noise_mean_slider.value
    noise_covariance = noise_covariance_slider.value
    initial_noise = generate_noise(noise_mean, noise_covariance, x.shape)
    update_data(attr, old, new)

amplitude_slider.on_change('value', update_data)
frequency_slider.on_change('value', update_data)
phase_slider.on_change('value', update_data)
noise_mean_slider.on_change('value', update_noise)
noise_covariance_slider.on_change('value', update_noise)
show_noise_checkbox.on_change('active', update_data)


def reset_parameters():
    amplitude_slider.value = initial_amplitude
    frequency_slider.value = initial_frequency
    phase_slider.value = initial_phase
    noise_mean_slider.value = initial_noise_mean
    noise_covariance_slider.value = initial_noise_covariance
    show_noise_checkbox.active = initital_show_noise

reset_button.on_click(reset_parameters)

inputs = column(amplitude_slider,
    frequency_slider,
    phase_slider,
    noise_mean_slider,
    noise_covariance_slider,
    show_noise_checkbox,
    reset_button
)

layout = row(p, inputs)

curdoc().add_root(layout)
curdoc().title = "Harmonic Signal with Noise"