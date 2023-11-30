import ipywidgets as widgets
from IPython.display import display, clear_output

button = widgets.Button(description="Click Me!")
output = widgets.Output()

def on_button_clicked(b):
    with output:
        clear_output()
        print("Button clicked!")
        # You can call any Python function here

button.on_click(on_button_clicked)

display(button, output)
