# Residency-Day-1-Group-Project-Proposal
Proposal for an Interactive Visa Support Chatbot Outlining a project to build a chatbot that offers step-by-step visa information and assistance.

### Local Development Setup
The MCQ-generation workflow uses Python >=3.10.  

```shell
# 1. Clone the repository
git clone https://github.com/NehaCodesAI/Residency-Day-1-Group-Project-Proposal.git

# 2. Move into the project
cd Residency-Day-1-Group-Project-Proposal

# 3. Install build environment tools
pip install --upgrade virtualenv

# 4. Create a virtual environment
python -m virtualenv .venv

# 5. Activate the virtual environment (Linux || Windows)
source .venv/bin/activate || source .venv/scripts/activate

# 6. Create an .env file.  Fill it in with the necessary values following this format: "OPENAI_API_KEY=XXXX"
touch .env

# 7. Install all the dependencies
pip install --editable .
```


# Run the demo app
1. run this command in the terminal: `streamlit run app_streamlit.py`