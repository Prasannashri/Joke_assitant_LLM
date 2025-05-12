import requests
import json
import gradio as gr

#Creating Prompts
system_prompt = "You are an assistant that is great at telling jokes"
user_prompt = "Tell a light-hearted joke for an audience of Software Engineers"

prompts = [
    {"role": "system", "content": system_prompt}, 
    {"role": "user" , "content" : user_prompt }
   ];


#params to call LLM
OLLAMA_API      =  "http://localhost:11434/api/chat"
HEADERS         =  {"Content-Type": "application/json"}
MODEL           =  "llama3.2"

#function to call LLM
def callOllama(user_prompt):
    prompts = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user" , "content" : user_prompt }
        ];
    response = requests.post(OLLAMA_API, json={"model": MODEL,
        "messages": prompts,
        "stream": False }, headers=HEADERS)
    return (response.json()['message']['content'])


#function to call LLM with Stream 
def callOllamaWithStream(user_prompt):
    prompts = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user" , "content" : user_prompt }
        ];
    response = requests.post(OLLAMA_API, json={"model": MODEL,
        "messages": prompts,
        "stream": True }, headers=HEADERS)
     # Stream response as it comes in
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            content = data.get("message", {}).get("content", "")
            yield content;



# print(callOllama(prompts));
# callOllamaWithStream(prompts);


view = gr.Interface(
    fn = callOllama,
    inputs=[gr.Textbox(label="Your message:")],
    outputs=[gr.Markdown(label="Response:")],
    flagging_mode="never"
)


view.launch()