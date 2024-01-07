import os
import dotenv
from openai import OpenAI
import requests
import re
import csv


# In[36]:


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # if the key already exists in the environment variables, it will use that, otherwise it will use the .env file to get the key
if not OPENAI_API_KEY:
    dotenv.load_dotenv(".env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# In[37]:


# ps_pair should be a single string connect the "problem" and "solution" value by a newline 
def identify_domain(ps_pair, api_key):
    
    client = OpenAI(
        api_key = api_key
    )
    
    prompt_text = f"""
    You are a text classifier model. Given the following domains, identify which domains of expertise the following problem solution pairs fall into and output should only be the identified domains separating each with commas (no other text).
    
Domains:
    
Fashion
Water
Energy
Manufacturing
Waste Management
Construction
Technology
Transportation
Agriculture
Education 

Problem-Solution Pair:
{ps_pair}
    """
    
    # Call the OpenAI API
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # Choose the appropriate engine
      messages=[{"role": "user", "content": prompt_text}],
    )

    # Return the text part of the response
    return response.choices[0].message.content
    


# In[38]:


# Create prompt to evaluate an idea
def prompt_for_domain_expert_idea_evaluation(category, ps_pair, rubric, api_key):
    
    client = OpenAI(
        api_key = api_key
    )

    # Format the prompt to ask GPT to pretend to be an expert in the given category
    prompt_text = f"""
    
    You are an expert in {category}. You have been asked to evaluate the following circular economy idea containing an identified problem and solution:
    
    {ps_pair}
    
    Based on the following rubric in a CSV format, rate the idea on each of the criteria (where row 1 is the option of points per criteria and the remaining rows represents the criteria itself) based on the point system defined: 
    
    {rubric}
    
    The output should be in the following format:
    
    Originality: [chosen number rating] - [reason for rating]
    Feasibiltiy: [chosen number rating] - [reason for rating]
    Impact: [chosen number rating] - [reason for rating]
    Development & Research: [chosen number rating] - [reason for rating]
    Scalability: [chosen number rating] - [reason for rating]
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # Choose the appropriate engine
      messages=[{"role": "user", "content": prompt_text}],
    )

    # Return the text part of the response
    return response.choices[0].message.content


# In[39]:


# Given then output above, extract the numbers to calculate the total score by this expert
def extract_total_score(evaluation, api_key):
    # Extract numbers between a colon and a dash using regular expression
    numbers = re.findall(r':\s*(\d+)\s*-', evaluation)
    print(numbers)
    # Convert extracted numbers to integers and calculate the sum
    total = sum(int(number) for number in numbers)
    
    return total


# In[40]:


def prompt_for_business_team_evaluation(team_role, ps_pair, rubric, api_key):
    
    client = OpenAI(
        api_key = api_key
    )

    # Format the prompt to ask GPT to pretend to be an expert in the given category
    prompt_text = f"""
    
    You are an a experienced {team_role}. You have been asked to evaluate the following circular economy idea containing an identified problem and solution:
    
    {ps_pair}
    
    Based on the following rubric in a CSV format, rate the idea on each of the criteria (where row 1 is the option of points per criteria and the remaining rows represents the criteria itself) based on the point system defined: 
    
    {rubric}
    
    The output should be in the following format:
    
    Originality: [chosen number rating] - [reason for rating]
    Feasibiltiy: [chosen number rating] - [reason for rating]
    Impact: [chosen number rating] - [reason for rating]
    Development & Research: [chosen number rating] - [reason for rating]
    Scalability: [chosen number rating] - [reason for rating]
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # Choose the appropriate engine
      messages=[{"role": "user", "content": prompt_text}],
    )

    # Return the text part of the response
    return response.choices[0].message.content


# In[41]:


def summarize_reasoning(combined_evals, api_key):
    client = OpenAI(
        api_key = api_key
    )

    # Format the prompt to ask GPT to pretend to be an expert in the given category
    prompt_text = f"""
    Given the following evaluations of a business idea by different experts, summarize the main critiques or highlights in a few sentences.
    
    All Evaluations:
    {combined_evals}
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # Choose the appropriate engine
      messages=[{"role": "user", "content": prompt_text}],
    )

    # Return the text part of the response
    return response.choices[0].message.content



if os.path.exists(os.path.join(os.getcwd(), "rubric.txt")):
    with open(os.path.join(os.getcwd(), "rubric.txt"),"r") as f: 
        sample_rubric = f.read()
else:
    sample_rubric = """
    Originality, Idea has common elements with no unique differentiation. (1), Idea shows some novel thinking and differentiation. (2), Idea is largely original, showing significant new thinking. (3), Idea is completely unique demonstrating groundbreaking thinking. (4)
    Feasibility, Idea has significant practical or technical obstacles. (1), Idea is somewhat practical but faces notable challenges. (2), Idea is fairly practical with manageable challenges. (3), Idea is highly practical and can be implemented smoothly. (4)
    Impact, Idea has a limited or unclear impact. (1), Idea has a moderate impact with some tangible benefits. (2), Idea has a significant impact with clear benefits. (3), Idea has a transformative impact with far-reaching benefits. (4)
    Development & Research, Idea is underdeveloped with minimal research or supporting data. (1), Idea is somewhat developed with some research or supporting data. (2), Idea is well-developed with substantial research or supporting data. (3), Idea is fully developed with extensive research or supporting data. (4)
    Scalability, Idea shows little to no potential for growth or adaptation. (1), Idea shows some potential for growth or adaptation. (2), Idea shows considerable potential for growth or adaptation. (3), Idea shows extensive potential for growth or adaptation. (4)
    """

sample_ps_pair = """
Problem: Single-use plastic packaging has become an all-too-common sight in our environment, resulting in detrimental environmental impacts. Studies show that approximately 8.3 billion tonnes of plastic have been produced since 1950, and 60% of that plastic ends up in either our landfills or the natural environment. This contributes greatly to pollution, harms wildlife, affects human health, and exacerbates climate change.   
Solution: To alleviate this problem, we propose developing a consumer-friendly, easy-to-use app that manages and optimises the reverse logistics of packaging. Imagine this: when purchasing a product, consumers will pay a one-time fee for reusable packaging. After use, they can return the empty packaging via designated collection points or direct pickup services. The app will facilitate this process by tracking, scheduling pickups or locating nearby collection points. The packaging is then cleaned and reused, thereby reducing the need for new plastic production and ensuring the packaging circulates within the economy, instead of ending up as waste. This app will not only help consumers make more sustainable choices but also incentivise producers to shift towards a circular economy model.
"""
sample_ps_pair2 = """ 
Problem: The solution is meant to solve the issue of electronic waste and reduce the heap of idle electronic products in our homes
Solution: E waste has always been a growing problem in the world. The inclusion of circular economy techniques in our day to day life can bring about a huge change in this context. The consumer electronic goods that remains idle in our homes or is inoperative can be thought of as a means to implement the idea. If there exists a system which can collect the inoperative home consumer goods, extract the different parts like transistors, diodes, etc and make it to use in future products, I think it may reduce the problem of e waste marginally. Even if the parts are damaged, in some cases, trying to repair them can be much more cheap way than building a new component altogether. Thus even the manufacturing cost can be reduced. Also, there can be a quick supply of electronic components in the market. 
There can also be a responsible framework of second hand consumer electronic goods. Thus even the poor people can afford the best of consumer electronics without spending much from their pocket. This will include more people in the consumer electronics market which can in turn improve the market forces.
"""


def evaluate_and_output_score(ps_pair, rubric, api_key):
    
    all_evals = []
    domains = identify_domain(ps_pair, api_key)
    domain_expert_eval = prompt_for_domain_expert_idea_evaluation(domains, rubric, ps_pair, api_key)
    all_evals.append(domain_expert_eval)

    # team_roles = ['Product Designer', 'Business Analyst', 'Marketing Specialist', 'Supply Chain Manager']
    # for role in team_roles:
    #     all_evals.append(prompt_for_business_team_evaluation(role, sample_rubric, sample_ps_pair2, api_key))
        
    total_score = 0
    for eval in all_evals:
        unit_score = extract_total_score(eval, api_key)
        print(unit_score)
        total_score += unit_score
        
    overall_reasoning = summarize_reasoning("\n".join(all_evals), api_key)
    
    return total_score, overall_reasoning
    

def process_dataframe_with_evaluation(df, rubric, api_key):
    # Add a new column to the dataframe to store the evaluation results
    df['final_eval'] = None
    df['overall_reasoning'] = None
    
    for index, row in df.iterrows():
        # Join the 'Problem' and 'Solution' text
        ps_pair = f"Problem: {row['problem']}\nSolution: {row['solution']}"
        print(ps_pair)
        # Call the function 'evaluate_pairs' on the ps_pair and store the result in the new column
        df.at[index, 'final_eval'], df.at[index, 'overall_reasoning'] = evaluate_and_output_score(ps_pair, rubric, api_key)
        print("Finished")
    return df