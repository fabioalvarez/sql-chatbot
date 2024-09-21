from orchestrator import init_text_to_sql, orchestrator


if __name__ == "__main__":
    engine, db, llm, retriever, context_creator = init_text_to_sql()

    while True:
        prompt = "Give me the most sold categories"
        if prompt == "exit":
            break

        response = orchestrator(
            llm=llm,
            db=db,
            obj_retriever=retriever,
            context_creator=context_creator,
            dialect=engine.dialect.name,
            question=prompt,
            verbose=True,
        )

        print(response)
