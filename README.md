# ScriptWritingAssistant

## Overview
The Script Writing Assistant is an interactive tool designed to help users draft and finalize scripts. The platform leverages Streamlit for the user interface, FastAPI for backend APIs, and AWS Bedrock for script analysis and generation.

Flow diagram

![Screenshot 2024-07-16 150037](https://github.com/user-attachments/assets/56aa4c27-1883-4811-ba5a-329d7b015a4b)

## Features
- Script Analysis: Analyzes the input script and provides suggestions for improvements.
- Script Finalization: Finalizes the improved script based on previous suggestions.
- AWS Integration: Utilizes AWS Bedrock for generating suggestions and final scripts, and AWS S3 for saving the results.

## Installation
#### Prerequisites
- Python 3.12
- AWS account with appropriate permissions
- Streamlit
- Requests library
- Boto3 library

## Setup
1. Clone the repository:
```
git clone https://github.com/your-repo/script-writing-assistant.git
cd script-writing-assistant
```

2. Create environment
```
conda create -p venv python=3.12 -y
conda activate venv/
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Configure AWS credentials:
Ensure you have your AWS credentials configured properly

## Usage
#### Running the Application
To start the Streamlit application, run:

```
streamlit run app.py
```

This will launch the web interface where you can input your script and receive suggestions.