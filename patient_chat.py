import gradio as gr

def get_patient_info(patient_id):
    return {
        "name": "Massoud DIALLO",
        "exercises_progress": "50% d'exercices complétés",
        "mental_state": "Stress élevé",
        "mental_state_score": 75,
    }

def send_message(message, chat_history):
    if message:
        # Format correct pour Gradio : liste de tuples (user, bot)
        chat_history.append((message, "Réponse du bot ici..."))
    return "", chat_history

def init_patient_info(patient_id):
    patient_info = get_patient_info(patient_id)
    return (
        patient_info["name"], 
        patient_info["exercises_progress"], 
        patient_info["mental_state"], 
        patient_info["mental_state_score"]
    )

with gr.Blocks(theme=gr.themes.Soft()) as patient_chat_page:
    with gr.Row():
            gr.Markdown("<h1 style='text-align: center;'>🧠 MentalCare - Espace Patient</h1>")
    with gr.Row():
        # Colonne gauche (chat)
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversation avec MentalBot",
                bubble_full_width=False,
                avatar_images=(
                    "https://img.freepik.com/vecteurs-libre/conception-modele-logo-communication_23-2149881439.jpg?semt=ais_hybrid&w=740", 
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

        with gr.Column():
            # Colonne droite
            with gr.Column(scale=1, min_width=250):
                name, progress, mental_state, mental_state_score = init_patient_info(1)
                
                with gr.Accordion("📋 Profil Patient", open=True):
                    gr.Markdown(f"**Nom :** {name}  \n**Progrès :** {progress}")
                    
                    with gr.Group():
                        gr.Markdown("### État Mental")
                        gr.Markdown(f"**Niveau actuel :** {mental_state}")
                        gr.Markdown(f"**Score de stress :** {mental_state_score}/100")
                        
                        if mental_state_score > 80:
                            status = "🔴 Stress élevé - Consultez un spécialiste"
                        elif mental_state_score > 50:
                            status = "🟠 Stress modéré - Exercices recommandés"
                        else:
                            status = "🟢 Stress faible - Bon équilibre"
                        gr.Markdown(f"**Recommandation :** {status}")

    # Gestion des interactions
    send_btn.click(
        fn=send_message,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot]
    )
    user_input.submit(
        fn=send_message,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot]
    )

patient_chat_page.launch()