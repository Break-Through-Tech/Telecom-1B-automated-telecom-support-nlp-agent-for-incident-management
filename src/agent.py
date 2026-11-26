import streamlit as st

from smolagents import CodeAgent, LiteLLMModel
from tools.preprocess_data import run_preprocess_and_training_pipeline
from tools.make_prediction import run_model_prediction_pipeline
from prompt import PROMPT

@st.cache_resource
def get_agent() -> CodeAgent:
    model = LiteLLMModel(model_id="ollama_chat/qwen3:1.7b")
    agent =  CodeAgent(tools=[run_preprocess_and_training_pipeline, run_model_prediction_pipeline],
        model=model,
        use_structured_outputs_internally=True,
        max_steps=4,
    )
    agent.prompt_templates["system_prompt"] += "\n\n" + PROMPT
    return agent
