import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException 
from llm_helper import llm

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path,encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts,outfile, indent=4)

def get_unified_tags(post_with_metadata):
    unique_tags = set()
    for post in post_with_metadata:
        unique_tags.update(post['tags'])
    unique_tags_list = ', '.join(sorted(unique_tags))

    template = '''
    You will be given a list of system design-related tags: {tags}
    Your task is to unify and merge these tags according to the following rules:
	1.	Unification and Merging: Similar or closely related tags should be merged into a single, more general tag.
	•	Example 1: Load Balancing, Traffic Distribution, and Request Routing can be unified as Load Balancing.
	•	Example 2: Microservices Architecture, Microservices, and Distributed Systems can be unified as Distributed Systems.
	•	Example 3: Database Sharding, Horizontal Scaling, and Scaling Databases can be unified as Scalability.
	2.	Title Case Convention: All tags should follow title case (e.g., Distributed Systems, not distributed systems).
	3.	Output Format: Return the result as a JSON object with mappings from the original tag to the unified tag.
    4. Return ONLY the JSON—no other text, no explanations, no markdown.
    5. DO NOT wrap the JSON in any code block (no triple backticks).
	•	Example output:
    {{"Load Balancing": "Load Balancing", "Traffic Distribution": "Load Balancing", "Microservices": "Distributed Systems","Database Sharding": "Scalability"}}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Unable to Parse data.")
    return res
    

def extract_metadata(post):
    template = '''
    You are given a LinkedIn Post, and you need to extract the number of lines, language and relevant tags.
    1. Return a valid JSON. No Preamble.
    2. tags is an arrage of text tags. return a maximum of 2 arrays, make sure there are only characters as tags, feel free to have niche tags
    3. Language should be English or Hinglish (Hinglish is Hindi + English)

    Here is the post you need to perform the above tasks on: {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post':post})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Unable to Parse data.")
    return res
if __name__ == "__main__":
    process_posts("data/raw_post.json","data/processed_posts.json")