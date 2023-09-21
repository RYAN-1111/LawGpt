import streamlit as st
import pandas as pd
import json
import openai

# Read data from CSV file
df = pd.read_csv('legal_text_classification.csv')

# Convert DataFrame to list of dictionaries
legal_cases = df.to_dict(orient='records')

# Set up OpenAI API
openai.api_key = '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'  # Replace with your actual API key

# Define a function to get legal answers
def get_legal_answer(question, cases):
    relevant_cases = []

    for case in cases:
        case_title = str(case['case_title']) if not pd.isna(case['case_title']) else ''
        case_text = str(case['case_text']) if not pd.isna(case['case_text']) else ''
        case_outcome = str(case['case_outcome']) if not pd.isna(case['case_outcome']) else ''

        # Check if the question keywords are present in any of the columns
        if any(keyword in case_title.lower() or keyword in case_text.lower() or keyword in case_outcome.lower() for keyword in question.lower().split()):
            relevant_cases.append(case_title + '\n\n' + case_text + '\n\n' + case_outcome)
        if len(relevant_cases) >= 10:  # Limit to 10 relevant cases
            break

    context = '\n\n'.join(relevant_cases)
    context = context[:4096]  # Limit context to 4096 tokens
    prompt = f"Question: {question}\n\nContext: {context}\nAnswer:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
    )
    return response.choices[0].text.strip()



# Streamlit App
def main():
    st.title("Legal Chatbot")

    # User Input
    user_question = st.text_input("Ask a legal question:")

    if st.button("Get Answer"):
        if user_question:
            answer = get_legal_answer(user_question, legal_cases)
            st.subheader("Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

if __name__ == '__main__':
    main()

