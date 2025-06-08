from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

def editor_self_developed_prompt(submitted_report):
    editor_self_developed = '''
    {submitted_report}
    -----------------------
    Above is the submitted report. Based on this report, you need to list a lot of "are you sure .... " questions.
    e.g., Are you sure amino acid changes p.I43V's genetic loci is rs71519934?
    
    Please consider both the table content and the reference.
    '''.format(submitted_report=submitted_report)


    editor_self_developed = '''
    {submitted_report}
    -----------------------
    Above is the submitted report. Based on this report, you need to list a lot of "are you sure .... " questions.
    e.g., Are you sure amino acid changes p.I43V's genetic loci is rs71519934?
    
    Note: Both the table content and references might contain errors.
    '''.format(submitted_report=submitted_report)
    return editor_self_developed

def editor_feedback_prompt(submitted_report, questions):
    editor_feedback = '''
    {submitted_report}
    -----------------------
    Above is the submitted report. To validate and modify this report, you need to answer the following questions:
    '''.format(submitted_report = submitted_report)

    editor_feedback += questions
    editor_feedback += '''
    **You have to search first before answering the question. You need to verify the authenticity of the references through search, rather than directly trusting the content quoted in the original report.**
    '''

    return editor_feedback

def editor_summary_prompt_with_mp(submitted_report, gene_name, rebuttals, mistake_pool):
    editor_summary = '''
    {submitted_report}
    -----------------------
    Here is the submitted report. Please summarize the content of the following feedbacks based on the report and the Q&A below:
    '''.format(submitted_report = submitted_report)

    editor_summary += rebuttals
    
    editor_summary += f'''
**Additional Action:** Refer to the mistake pool of common errors summarized from other reports: {mistake_pool}.\
If you find similar errors in the current report, include a request for the corresponding actions in the summary.
    '''
#     editor_summary += '''
# **Additional Action:** Ensure any references and content (i.e. gene functions) to other genes are removed.\
#     '''
    editor_summary += f'''
    **Summarize the feedbacks.**
    '''

    return editor_summary


def editor_summary_prompt(submitted_report, gene_name, rebuttals):
    editor_summary = '''
    {submitted_report}
    -----------------------
    Here is the submitted report. Please summarize the content of the following feedbacks based on the report and the Q&A below:
    '''.format(submitted_report = submitted_report)

    editor_summary += rebuttals

    
    editor_summary += '''
**Additional Action:** Ensure any references and content (i.e. gene functions) to other genes are removed.\
    '''
    editor_summary += f'''
    **Summarize the feedbacks.**
    '''

    return editor_summary


def mistake_pool_prompt(instruction, prompt):
    # Create the prompt template from messages
    prompt_template = ChatPromptTemplate.from_messages(
        messages=[
            SystemMessage(content=instruction),
            HumanMessage(content=prompt)
        ]
    )

    return prompt_template