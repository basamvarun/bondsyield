import sys
import os

# This file acts as a "launcher" for Streamlit Cloud
# It ensures the 'src' and 'dashboard' folders are correctly recognized

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import and execute the main dashboard app
if __name__ == "__main__":
    # We use a sub-process or manual exec to ensure the dashboard runs in the correct context
    os.system(f"streamlit run {os.path.join(project_root, 'dashboard', 'app.py')}")

# Alternatively, for Streamlit Cloud's "Main file path", we can just point to dashboard/app.py
# But having this file in the root is a "fail-safe"
