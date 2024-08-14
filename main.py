import yaml
from src.pipeline.llm_pipeline import LLMPipeline
import streamlit as st

def load_config():
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    st.title("SQL Query Generator")
    config = load_config()
    pipeline = LLMPipeline(config)
    user_query = st.text_input("Enter your query:")

    if st.button("Generate SQL Query"):
        if user_query.strip():
            success, result, sql_query = pipeline.run(user_query)
            
            st.write(f"\nGenerated SQL Query:\n```\n{sql_query}\n```")

            if success:
                st.write("Query result:")
                st.table(result)
            else:
                st.error(f"Error executing query: {sql_query}, error: {result}")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
