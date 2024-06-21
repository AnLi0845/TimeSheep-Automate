# Example Code
```
# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the script with default varibales (from today to today and working hours is 8)
python timesheep_auto.py username@example.com password123

# Run the script with user-defined variables (default task progress: Execution)
python timesheep_auto.py username@example.com password123 --from_data_enter 21 --to_data_enter 21 --working_hour 8
```
