import streamlit as st
import json
import os

class Agent:
    def __init__(self, name, role, prompt_template, model="gpt-3.5", tools=None):
        self.name = name
        self.role = role
        self.prompt_template = prompt_template
        self.model = model
        self.tools = tools if tools else []
        self.logs = []

    def run(self, input_text):
        response = f"[{self.role}] processed input: {input_text}"
        self.logs.append(response)
        return response

    def summarize(self):
        return f"Agent '{self.name}' ({self.role}) used model '{self.model}'"

    def log(self):
        return self.logs

st.set_page_config(page_title="AgentFlow Builder", layout="wide")
st.title("AgentFlow Builder")

workflow = []
saved_workflows_path = "saved_workflows.json"

def save_workflow(workflow_data):
    if os.path.exists(saved_workflows_path):
        with open(saved_workflows_path, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[workflow_data["name"]] = workflow_data
    with open(saved_workflows_path, "w") as f:
        json.dump(data, f)

def load_workflow(name):
    if os.path.exists(saved_workflows_path):
        with open(saved_workflows_path, "r") as f:
            data = json.load(f)
        return data.get(name, None)
    return None

workflow_name = st.text_input("Workflow Name", "MyWorkflow")
num_agents = st.slider("Number of agents in workflow", 1, 4, 2)

for i in range(num_agents):
    with st.expander(f"Agent {i+1} Configuration"):
        name = st.text_input(f"Agent {i+1} Name", f"Agent_{i+1}", key=f"name_{i}")
        role = st.selectbox(f"Agent {i+1} Role", ["Retriever", "Summarizer", "Critic", "Recommender"], key=f"role_{i}")
        prompt_template = st.text_area(f"Agent {i+1} Prompt", "Process the following input:", key=f"prompt_{i}")
        model = st.selectbox(f"Agent {i+1} Model", ["gpt-3.5", "claude-2", "llama-2"], key=f"model_{i}")
        tools = st.multiselect(f"Agent {i+1} Tools", ["Web Search", "Code Execution", "None"], key=f"tools_{i}")

        agent = Agent(name, role, prompt_template, model, tools)
        workflow.append(agent)

input_text = st.text_area("Input Text for Workflow", "The quick brown fox jumps over the lazy dog.")

final_output = ""

if st.button("Run Workflow"):
    st.subheader("Workflow Execution Monitor")
    for agent in workflow:
        st.markdown(f"Running {agent.name} ({agent.role})...")
        output = agent.run(input_text)
        st.markdown("Output:")
        st.code(output)
        st.markdown("Logs:")
        st.code("\n".join(agent.log()))
        input_text = output
    final_output = input_text
    st.session_state["final_output"] = final_output

if "final_output" in st.session_state:
    st.subheader("Final Output")
    st.text_area("Result", st.session_state["final_output"], height=150)
    st.download_button("Download Output", st.session_state["final_output"], file_name="workflow_output.txt")

if st.button("Save Workflow"):
    workflow_data = {
        "name": workflow_name,
        "agents": [
            {
                "name": agent.name,
                "role": agent.role,
                "prompt_template": agent.prompt_template,
                "model": agent.model,
                "tools": agent.tools
} for agent in workflow
        ]
}
    save_workflow(workflow_data)
    st.success(f"Workflow '{workflow_name}' saved.")

if st.button("Load Workflow"):
    loaded = load_workflow(workflow_name)
    if loaded:
        st.json(loaded)
    else:
        st.error(f"No workflow found with name '{workflow_name}'.")￼Enter
