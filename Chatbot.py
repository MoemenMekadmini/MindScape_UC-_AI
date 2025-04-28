import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


model_name = "NousResearch/Hermes-2-Pro-Mistral-7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_4bit=True 
)


chatbot = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto"
)

def respond(message, history):
    prompt = f"""<|im_start|>system
    You are a mental health assistant. Provide concise, supportive responses (2-3 sentences max).
    Focus on active listening and practical suggestions.<|im_end|>
    <|im_start|>user
    {message}<|im_end|>
    <|im_start|>assistant
    """

    output = chatbot(
        prompt,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )


    response = output[0]['generated_text'].split("<|im_start|>assistant")[-1]
    response = response.split("<|im_end|>")[0].strip()
    return response


import gradio as gr 


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Stable Mental Health Assistant")
    gr.ChatInterface(
        respond,
        examples=[
            "I've been feeling really anxious lately",
            "How can I deal with work stress?",
            "I'm struggling with negative thoughts"
        ]
    )

demo.launch()
