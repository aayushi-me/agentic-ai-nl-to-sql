import gradio as gr
from agent1_server import agent1_nl2sql

def gradio_nl2sql(nl_query, schema):
    return agent1_nl2sql(nl_query, schema)

demo = gr.Interface(
    fn=gradio_nl2sql,
    inputs=[
        gr.Textbox(label="Natural Language Query", placeholder="Show all users who registered in 2024"),
        gr.Textbox(label="Database Schema", placeholder="users(id, name, email, registration_date)")
    ],
    outputs=gr.Textbox(label="SQL Translation"),
    title="Agentic AI NL-to-SQL (gRPC Two-Agent System)",
    description="This demo uses two real agent processes communicating over gRPC."
)

if __name__ == "__main__":
    print("Starting Gradio UI. Make sure Agent1 and Agent2 are running on their respective ports.")
    demo.launch(share=True)
