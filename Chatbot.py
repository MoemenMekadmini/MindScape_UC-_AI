import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import gradio as gr

model_name = "NousResearch/Hermes-2-Pro-Mistral-7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_4bit=True
)

chatbot_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto"
)


def get_patient_info(patient_id):
    return {
        "name": "Moemen Mekadmini",
        "exercises_progress": "50% d'exercices complétés",
        "mental_state": "Stress élevé",
        "mental_state_score": 75,
    }

def init_patient_info(patient_id):
    patient_info = get_patient_info(patient_id)
    return (
        patient_info["name"],
        patient_info["exercises_progress"],
        patient_info["mental_state"],
        patient_info["mental_state_score"]
    )

def respond(message, history):
    prompt = f"""<|im_start|>system
    You are a Tunisian mental health assistant for the CentralUniverisity in Tunisa. Provide concise, supportive responses (2-3 sentences max).
    Focus on active listening and practical suggestions. Respond in English.<|im_end|>
    <|im_start|>user
    {message}<|im_end|>
    <|im_start|>assistant
    """

    output = chatbot_pipeline(
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

# Create the interface
with gr.Blocks(theme=gr.themes.Soft()) as patient_chat_page:
    with gr.Row():
        gr.Markdown("<h1 style='text-align: center;'>🧠 MindScape UC AI- Espace Patient</h1>")

    with gr.Row():
        # Left column (chat)
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversation avec MindScape",
                bubble_full_width=False,
                avatar_images=(
                    "https://img.freepik.com/vecteurs-libre/conception-modele-logo-communication_23-2149881439.jpg",
                    "https://t3.ftcdn.net/jpg/03/35/16/66/360_F_335166628_b2M3WgWbbZqxNHsRt6ZxHzk1dtCrWhVx.jpg"
                )
            )

            with gr.Row():
                user_input = gr.Textbox(
                    placeholder="Écrivez votre message...",
                    show_label=False,
                    container=False
                )
                send_btn = gr.Button("Envoyer", variant="primary")

        with gr.Column(scale=1, min_width=250):
            name, progress, mental_state, mental_state_score = init_patient_info(1)

            with gr.Accordion("📋 Profil Patient", open=True):
                gr.Markdown(f"Nom : {name}  \n*Progrès :* {progress}")

                with gr.Group():
                    gr.Markdown("### État Mental")
                    gr.Markdown(f"Niveau actuel : {mental_state}")
                    gr.Markdown(f"Score de stress : {mental_state_score}/100")

                    if mental_state_score > 80:
                        status = "🔴 Stress élevé - Consultez un spécialiste"
                    elif mental_state_score > 50:
                        status = "🟠 Stress modéré - Exercices recommandés"
                    else:
                        status = "🟢 Stress faible - Bon équilibre"
                    gr.Markdown(f"Recommandation : {status}")

   
    def chat_fn(message, chat_history):
        if not message:
            return "", chat_history
        bot_response = respond(message, chat_history)
        chat_history.append((message, bot_response))
        return "", chat_history

    send_btn.click(
        chat_fn,
        [user_input, chatbot],
        [user_input, chatbot]
    )

    user_input.submit(
        chat_fn,
        [user_input, chatbot],
        [user_input, chatbot]
    )

patient_chat_page.launch()
