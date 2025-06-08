from report_sec_output_format import genetic_evidence, safety_format, get_format


def editor_instruction(section_name, output_format = None):
    editor_instruction = '''
    You are a genetic expert and an editor who is responsible for reviewing a section of submitted target gene analysis reports.

    Now you are focusing on {section_name} section.
    This section's format is shown as follow:
    '''.format(section_name=section_name)

    editor_instruction += '\n' + get_format(section_name)

    # if section_name == 'genetic_evidence':
    #     editor_instruction += '\n' + genetic_evidence()
    # elif section_name == 'safety':
    #     editor_instruction += '\n' + safety_format()
 
    editor_instruction += '''
    ***Your job is to find out the incorrect part of the submitted report.***
        '''

    if output_format != None:
        editor_instruction += '''
        Output Format:
        '''
        editor_instruction += output_format
    
    return editor_instruction


def rebuttal_instruction(section_name, output_format = None):
    rebuttal_instruction = '''
    You are a genetic expert and an editor who is responsible for reviewing a section of submitted target gene analysis reports.

    Now you are focusing on {section_name} section.
    This section's format is shown as follow:
    '''.format(section_name=section_name)

    rebuttal_instruction += '\n' + get_format(section_name)

    # if section_name == 'genetic_evidence':
    #     rebuttal_instruction += '\n' + genetic_evidence()
    # elif section_name == 'safety':
    #     rebuttal_instruction += '\n' + safety_format()
 
    rebuttal_instruction += '''
***Your task is to review the content of the report I \
provided based on the following list of questions, checking each point for accuracy. Please respond according to the output format.***
        '''

    if output_format != None:
        rebuttal_instruction += '''
        Output Format:
        '''
        rebuttal_instruction += output_format
    
    return rebuttal_instruction


def rebuttal_instruction_update(section_name, report, output_format = None):
    rebuttal_instruction = '''
    You are a genetic expert and an editor who is responsible for reviewing a section of submitted target gene analysis reports.

    Now you are focusing on {section_name} section.
    This section's original report is shown as follow:
    '''.format(section_name=section_name)

    # if section_name == 'genetic_evidence':
    #     rebuttal_instruction += '\n' + report +'\n'
    rebuttal_instruction += '\n' + report + '\n'
 
    rebuttal_instruction += '''
***Your task is to review the content of the report I \
provided based on the following list of questions, checking each point for accuracy. Please respond according to the output format.***
        '''

    if output_format != None:
        rebuttal_instruction += '''
        Output Format:
        '''
        rebuttal_instruction += output_format
    
    return rebuttal_instruction


def rebuttal_summary_instructions(section_name, output_format = None):
    summary_instruction = '''
    You are a biologist and a reviewer who is responsible for reviewing a section of submitted target gene analysis reports.

    Now you are focusing on {section_name} section.
    This section's format is shown as follow:
    '''.format(section_name=section_name)

    summary_instruction += '\n' + get_format(section_name)

    # if section_name == 'genetic_evidence':
    #     summary_instruction += '\n' + genetic_evidence()
    # elif section_name == 'safety':
    #     summary_instruction += '\n' + safety_format()
 
#     summary_instruction += '''
# ***Your task is to review the content of the report and feedbacks from other experts I \
# provided and summarize the feedbacks.***
# ***You should remember: The gain of function and loss of function tables should only include the single gene that we are concerned about.***
#         '''

    summary_instruction += '''
***Your task is to review the content of the report and feedbacks from other experts I \
provided and summarize the feedbacks.***
'''

    if output_format != None:
        summary_instruction += '''
        Output Format:
        '''
        summary_instruction += output_format
    
    return summary_instruction


def mistake_pool_instructions(mistake_pool,report,summarized_feedback):
    instruction = f'''\
    You are a gene and drug expert. Your task is to summarize the mistakes in the original report based on the feedback I provided and update the mistakePool.
    You need to summarize the mistakes made in the original report and store them in a dictionary called 'mistakePool'. The key of the dictionary should be a simple mistake type, and the value should be a description of this mistake type, followed by the action to be taken for this type of error, separated by '||'.
    Currently, the mistakePool dictionary looks like this: mistakePool: {mistake_pool};
    If the report you are given contains new mistakes, you can extract a keyword as the key to update the mistakePool, write a simple description to remind future agents what types of errors fall under this category, and specify the action to be taken for this type of error.
    If there are no new mistakes, you can keep the mistakePool unchanged.
    '''

    prompt = f'''\
    Original Report: {report}, Feedback: {summarized_feedback}
    You need to **directly** return the updated mistakePool in the form of a dictionary, or keep the mistakePool unchanged if there are no new mistakes.
    RETURN FORMAT:
    mistakePool = {{key:value||Action:xx}}
    Note: When adding new mistakes, include the action to be taken for this type of error, separated by '||'.
    '''
    return instruction,prompt