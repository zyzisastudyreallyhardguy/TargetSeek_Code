Target_Scoring Illustration:
    instructions.py --> agent instructions for doing scoring
    scoring_criteria.py --> the reference table for scoring
    output_format.py --> the agent output of rating needs to strictly follow the output format
    agent_instructions.py --> initialize the agent instructions by filling in key information like gene name, disease name, etc
    scoring_sections.py --> scoring for different section based on scoring scoring_criteria
    tools.py 

    to set up a scoring function, you need to:
    1. define the scoring_criteria
    2. define the output_format
    3. define the instructions
    4. set up a function in agent_instructions to do initialization
    5. set up a function in scoring_sections to do scoring