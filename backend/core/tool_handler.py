from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

class ToolHandler:
    def __init__(self, llm, tool_schemas, available_functions):
        """
        llm: ChatGroq instance
        tool_schemas: List of tool definitions (JSON schemas)
        available_functions: Dict mapping function names to actual functions
        """
        self.llm = llm
        self.tool_schemas = tool_schemas  # The schemas
        self.functions = available_functions  # The actual functions
        
    def execute_tools(self, question, messages_dict=None):
        print(f"🛠️ ToolHandler called with: {question}")
        
        # Bind tools (schemas) to LLM
        llm_with_tools = self.llm.bind_tools(self.tool_schemas)
        
        # Call LLM with question
        response = llm_with_tools.invoke([HumanMessage(content=question)])
        
        print(f"🔍 Tool calls detected: {len(response.tool_calls) if response.tool_calls else 0}")
        
        if response.tool_calls:
            results = []
            for tool_call in response.tool_calls:
                func_name = tool_call['name']
                func_args = tool_call['args']
                
                print(f"🔧 Calling: {func_name}({func_args})")
                
                if func_name in self.functions:
                    # Execute the actual function
                    result = self.functions[func_name](**func_args)
                    results.append(result)
                    print(f"✅ Result: {result}")
                else:
                    print(f"❌ Function {func_name} not found!")
            
            return {
                'answer': self._format_tool_results(results, question),
                'tool_results': results
            }
        
        print("⚠️ No tool calls detected")
        return None
    
    def _format_tool_results(self, results, question):
        """Format tool results into a natural response"""
        if not results:
            return "I couldn't fetch that information."
        
        # Let LLM format the results naturally
        context = f"Question: {question}\n\nTool Results:\n{json.dumps(results, indent=2)}"
        
        format_prompt = f"""Based on the following tool results, provide a natural, helpful answer to the user's question.

        {context}

        Answer naturally and conversationally:"""
        
        response = self.llm.invoke([HumanMessage(content=format_prompt)])
        return response.content