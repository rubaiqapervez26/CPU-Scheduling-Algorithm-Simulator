# CPU Scheduling Algorithm Simulator

### 🖥️ Project Overview
This project is an interactive simulator designed to bridge the gap between Operating System theory and practical understanding. It allows users to input process details and see exactly how different algorithms manage CPU time.

### 🎯 Key Objectives
* **Visualization:** Generate Gantt charts to show the order of process execution.
* **Calculation:** Automate the calculation of Completion Time (CT), Waiting Time (WT), and Turnaround Time (TAT).
* **Comparison:** Compare the efficiency of different algorithms based on Average Waiting and Turnaround times.

### 🚀 Algorithms Implemented
1.  **First Come First Serve (FCFS):** Executes processes in the order they arrive.
2.  **Shortest Job First (SJF):** Selects the process with the smallest burst time to reduce average waiting time.
3.  **Round Robin (RR):** Allocates a fixed time quantum to each process to ensure fairness.

### 🛠️ Technologies Used
* **Language:** Python
* **GUI Framework:** Tkinter
* **Development Environment:** VS Code / PyCharm

### 📊 Features
* **Dynamic Input:** Add processes with custom Arrival and Burst times.
* **Gantt Chart:** A visual timeline of CPU activity, including "IDLE" time tracking.
* **Tabular Results:** A clean data table showing all calculated metrics for every process.
* **Responsive UI:** Built with threading and Tkinter to ensure smooth performance during simulations.

### ⚠️ How to Run
1. Ensure Python 3.x is installed.
2. Run the main script: `python "OS PROJECT.py"`
3. Select an algorithm from the dropdown and enter process data.
