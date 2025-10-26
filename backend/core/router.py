from langchain_classic.schema import HumanMessage, AIMessage

def needs_real_time_data(question):
    """Determine if the question requires real time data such as weather or currency exchange rates."""
    
    keywords =['weather', 'temperature', 'forecast', 'climate',
        'hot', 'cold', 'rain', 'sunny',
        'convert', 'exchange', 'currency', 'usd', 'eur']
    
    result = any(word in question.lower() for word in keywords)
    print(f"🔍 Question: {question}")
    print(f"🔍 Needs real-time: {result}")
    return result

# Convert chat history from message objects to dict format for tool handler becuase Raw GROQ API expects dict format.
# While langchain chains support message objects.

def route_query(question,chat_history, rag_engine, tool_handler):
    """Route the query to either RAG engine or tool handler based on the content of the question."""
    
    if needs_real_time_data(question):

        tool_result = tool_handler.execute_tools(question)
        return tool_result
    else:
        return rag_engine.query(question, chat_history)
    