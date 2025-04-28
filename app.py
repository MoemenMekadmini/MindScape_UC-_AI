import gradio as gr

# Fonctions simulées pour l'instant (plus tard on fera appel à l'API avec requests.post)
def login(username: str, password: str):
    if not username or not password:
        return gr.Info("Veuillez remplir tous les champs.")
    
    # 👉 Plus tard ici on enverra les données à l'API
    # Ex: response = requests.post(url_login, json={"username": username, "password": password})

    # Simulation d'une réponse
    if username == "patient" and password == "123":
        gr.Info("Connexion réussie en tant que Patient !")
        return "patient"  # 🔥 On retourne un rôle ici pour gérer la redirection
    elif username == "docteur" and password == "123":
        gr.Info("Connexion réussie en tant que Docteur !")
        return "docteur"
    else:
        gr.Error("Identifiants invalides.")
        return ""

def signup(username: str, password: str, role: str):
    if not username or not password:
        return gr.Error("Veuillez remplir tous les champs.")
    
    if len(password) < 6:
        return gr.Error("Le mot de passe doit contenir au moins 6 caractères.")
    
    # 👉 Plus tard ici on fera un appel API
    # response = requests.post(url_signup, json={"username": username, "password": password, "role": role})

    gr.Info(f"Compte {role.lower()} créé avec succès. Vous pouvez maintenant vous connecter !")
    return ""


# Interface principale
with gr.Blocks(theme=gr.themes.Soft()) as login_page:

    gr.Markdown("<h1 style='text-align: center;'>🔐 Bienvenue sur MindScape</h1>")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("")  # Colonne vide pour équilibrer à gauche

        with gr.Column(scale=2, min_width=600):
            with gr.Tab("Connexion"):
                with gr.Column():
                    login_username = gr.Textbox(label="Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
                    login_password = gr.Textbox(label="Mot de passe", type="password", placeholder="Entrez votre mot de passe")
                    login_button = gr.Button("Se connecter", variant="primary")
                    login_status = gr.State("")
            
            with gr.Tab("Inscription"):
                with gr.Column():
                    signup_username = gr.Textbox(label="Créer un nom d'utilisateur", placeholder="Nouveau nom d'utilisateur")
                    signup_password = gr.Textbox(label="Créer un mot de passe", type="password", placeholder="Nouveau mot de passe")
                    role_radio = gr.Radio(
                        choices=["Patient", "Docteur"],
                        label="Sélectionnez votre statut",
                        value="Patient"
                    )
                    signup_button = gr.Button("Créer un compte", variant="secondary")

        with gr.Column(scale=1):
            gr.Markdown("")  # Colonne vide pour équilibrer à droite

    # Actions sur les boutons
    def handle_login(username, password):
        role = login(username, password)
        return role

    def handle_redirect(role):
        if role == "patient":
            gr.Info("Redirection vers l'espace Patient 🧑‍⚕️...")
            return gr.redirect("patient_chat.py")  # 🔥 Redirige vers une page (fictive pour l'instant)
        elif role == "docteur":
            gr.Info("Redirection vers l'espace Docteur 🩺...")
            return gr.redirect("chat_docteur.py")
        else:
            return None  # Reste sur la même page si échec
        
    login_button.click(
        fn=handle_login,
        inputs=[login_username, login_password],
        outputs=login_status
    ).then(
        fn=handle_redirect,
        inputs=login_status,
        outputs=[]
    )

    signup_button.click(
        fn=signup,
        inputs=[signup_username, signup_password, role_radio],
        outputs=[]
    )

if __name__ == "__main__":
    login_page.launch()
