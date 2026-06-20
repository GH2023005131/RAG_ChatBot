import ollama

FIND_PROMPT = """
You are given two pieces of information:
1. A list of valid section names.
2. A user question.

Your task is to:
- Identify exactly one `section_name` from the provided list that seems related to the user question.
- Return the `section_name` exactly as it appears in the list.
- Do NOT answer the question.
- Do NOT return any additional text, explanation, or formatting.
- Do NOT combine multiple section names into a single response.

Here is the list of valid section names:

```
{SECTIONS}
```

Now, based on the following question, return the single most relevant `section_name` from the list.
"""

ANSWER_PROMPT = """
You are a rigorous assistant answering questions.
You must only answer based on the current information available which is:

```
{CURRENT_INFO}
```

If the current information available is not enough to answer the question,
you must return "I need more info" and nothing else.
"""


def get_matching_section(response, section_names):
    from rapidfuzz import process

    return process.extractOne(response, section_names)[0]


def find_retrieve_answer(question, section_names, get_content_fn, max_sections=20):
    current_info = None
    current_section = None
    sections_checked: list = []
    names = list(section_names)
    max_attempts = min(max_sections, len(names)) if names else 0

    while len(sections_checked) <= max_attempts:
        if not current_info:
            if not names:
                return "No relevant sections found.", sections_checked
            messages = [
                {
                    "role": "system",
                    "content": FIND_PROMPT.format(SECTIONS="\n".join(names)),
                },
                {"role": "user", "content": question},
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": ANSWER_PROMPT.format(CURRENT_INFO=current_info),
                },
                {"role": "user", "content": question},
            ]

        try:
            response = ollama.chat(model="qwen2.5:1.5b", messages=messages)
            response = response["message"]["content"]
        except Exception as e:
            return f"Error generating answer: {e}", sections_checked

        if not current_info:
            response = response.strip()
            if not names:
                return "No relevant sections found.", sections_checked
            section_name = get_matching_section(response, names)
            current_section = section_name
            current_info = get_content_fn(section_name)
            sections_checked.append(section_name)
        else:
            if "MORE INFO" in response.upper():
                current_info = None
                if current_section in names:
                    names.remove(current_section)
                continue
            else:
                return response, sections_checked

    return "Could not find an answer in the available sections.", sections_checked
