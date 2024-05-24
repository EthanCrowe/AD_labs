import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, CheckboxGroup
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

# Функція для генерації гармонічного сигналу з шумом
def generate_signal(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    t = np.linspace(0, 1, 1000)
    harmonic_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), t.shape)
    noisy_signal = harmonic_signal + noise
    if show_noise:
        return t, noisy_signal
    else:
        return t, harmonic_signal

# Початкові параметри
initial_amplitude = 1.0
initial_frequency = 5.0
initial_phase = 0
initial_noise_mean = 0
initial_noise_covariance = 0.1
initial_show_noise = [0]

# Створення початкового сигналу
t, signal = generate_signal(initial_amplitude, initial_frequency, initial_phase,
                            initial_noise_mean, initial_noise_covariance, initial_show_noise)

source = ColumnDataSource(data={'x': t, 'y': signal})

# Створення фігури
plot = figure(title="Harmonic Signal with Noise", x_axis_label='Time [s]', y_axis_label='Amplitude')
plot.line('x', 'y', source=source)

# Створення слайдерів та чекбокса
amplitude_slider = Slider(start=0, end=5, value=initial_amplitude, step=0.1, title="Amplitude")
frequency_slider = Slider(start=0, end=10, value=initial_frequency, step=0.1, title="Frequency")
phase_slider = Slider(start=0, end=2*np.pi, value=initial_phase, step=0.1, title="Phase")
noise_mean_slider = Slider(start=-1, end=1, value=initial_noise_mean, step=0.1, title="Noise Mean")
noise_covariance_slider = Slider(start=0, end=1, value=initial_noise_covariance, step=0.01, title="Noise Covariance")
show_noise_checkbox = CheckboxGroup(labels=["Show Noise"], active=initial_show_noise)

# Оновлення даних на основі нових значень параметрів
def update_data(attr, old, new):
    amplitude = amplitude_slider.value
    frequency = frequency_slider.value
    phase = phase_slider.value
    noise_mean = noise_mean_slider.value
    noise_covariance = noise_covariance_slider.value
    show_noise = show_noise_checkbox.active

    t, signal = generate_signal(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
    source.data = {'x': t, 'y': signal}

# Прив'язування функції оновлення до зміни значень слайдерів та чекбокса
amplitude_slider.on_change('value', update_data)
frequency_slider.on_change('value', update_data)
phase_slider.on_change('value', update_data)
noise_mean_slider.on_change('value', update_data)
noise_covariance_slider.on_change('value', update_data)
show_noise_checkbox.on_change('active', update_data)

# Розміщення елементів на сторінці
inputs = column(amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider, show_noise_checkbox)
layout = row(inputs, plot)

# Додавання до поточного документа Bokeh
curdoc().add_root(layout)
curdoc().title = "Harmonic Signal with Noise"
