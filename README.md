# virus_spread_simulator_2021

A agent-based modeling Python project simulating virus spread I did in 2021 for a univeristy course.

You can provide the simulation parameters either through command-line arguments or by answering the program's questions. Alternatively, you can specify the parameters in a YAML file (example in [sample_data.yaml](data/sample_data.yaml)) and pass the path to the file as a command-line argument.

The simulation will display an animation showing the spread of the virus over time. The figure will include a scatter plot representing the agents' locations, subplots showing the total cases, active cases, and deaths over time, and a legend indicating the color codes for each agent state.

## Dependencies

Python 3.x

matplotlib

numpy

PyYAML

You can install the required dependencies using pip:

    pip install -r requirements.txt

## Usage

To run the simulation, execute the `covid.py` file and follow the instructions:
    
    python src/covid.py