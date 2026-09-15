"""
Optional LLM adapter.
The core project does not require an API key. This file shows where an LLM
can be added without giving it unrestricted database access.
"""
def explain_with_llm(question, structured_result):
    # Production version: call an approved LLM here and provide only
    # the structured semantic result, not unrestricted raw-table access.
    return structured_result["answer"]
