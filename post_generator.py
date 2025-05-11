from llm_helper import llm
from few_shot import FewShotPosts

fs = FewShotPosts()

def generate_length_str(length):
    if(length == "Short"):
        return "1 to 6 lines"
    elif (length == "Medium"):
        return "6 to 13 lines"
    else:
        return "13 or more lines"
    
def get_prompt_to_generate_post(topic, length, language):
    prompt = f'''
    Genrate a crisp Linkedin Post using the following information - no preamble at all.Do not give the prompt back - just the post.
    1. Topic: {topic}
    2. Language: {language}
    3. Length: {generate_length_str(length)}
    '''
    examples = fs.get_filtered_posts(length, language, topic)
    if len(examples)>0:
        prompt+="4) Use the writing skill per the following examples: "
        for i, post in enumerate(examples):
            post_text = post['text']
            prompt+=f"\n\n Example {i+1}: \n\n {post_text}" 
            if i==2: 
                break
    return prompt

def generate_post(topic, length, language):
    prompt = get_prompt_to_generate_post(topic, length, language)
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    post = get_prompt_to_generate_post("System Design","Medium","English")
    print(post)