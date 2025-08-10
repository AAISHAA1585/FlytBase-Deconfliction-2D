# Drone Conflict Detection & Visualization

This project checks if a drone’s planned mission will have a **spatial** and **temporal** conflict with other drones in the airspace.  
It was made as part of the FlytBase internship assignment.

---

## 1. What it does
- Reads the **primary drone** mission and **other drones** missions from JSON files.
- Calculates the position of each drone every second.
- Checks if any drone comes closer than a set **safety distance** at the **same time**.
- Prints details of the conflicts in the terminal.
- Creates an **animation** showing drone movement and marking conflict points in red.

---

## 2. Folder structure

flytbase_deconfliction/
│
├── run_deconflict.py # Main script
├── requirements.txt # Libraries needed
├── README.md # This file
│
├── deconflict/ # Code files
│ ├── io.py # Reads JSON input
│ ├── trajectory.py # Calculates positions
│ ├── detector.py # Checks conflicts
│ ├── visualizer.py # Draws and animates drones
│ ├── utils.py # (Optional) helper functions
│
├── scenarios/ # Input data
│ ├── primary.json
│ ├── others.json
│
├── demo/ # Output animations
│ ├── conflict_animation.gif
│
└── docs/ # Extra documents
├── reflection.pdf

3. Setup Instructions

1:Install dependencies
pip install -r requirements.txt

2:Run the simulation
python run_deconflict.py