import streamlit as st
from orchestrator import orchestrator, init_text_to_sql


def app(sql_engine, database, openai_llm, obj_retriever, table_context_creator):
    st.title("Text To Sql Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask what you want?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = orchestrator(
            llm=openai_llm,
            db=database,
            obj_retriever=obj_retriever,
            context_creator=table_context_creator,
            dialect=sql_engine.dialect.name,
            question=prompt,
            verbose=True,
        )

        response = f"Assistant: {response}"

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    engine, db, llm, retriever, context_creator = init_text_to_sql()
    app(engine, db, llm, retriever, context_creator)
