import gradio as gr

patients = [
    {"prenom": "Massoud", "DIALLO": "Dupont", "mental": "Stresse/Anxiété", "derniere_visite": "2025-03-20"},
    {"prenom": "Alice", "nom": "Martin", "mental": "Tristesse/Depression", "derniere_visite": "2025-04-10"},
    {"prenom": "Marie", "nom": "York", "mental": "Fatique Mentale", "derniere_visite": "2025-01-15"},   {"prenom": "Charlie", "nom": "Lemoine", "mental": "Fatique Mentale", "derniere_visite": "2025-01-15"},
    {"prenom": "John", "nom": "Philip", "mental": "Tristesse", "derniere_visite": "2025-01-15"},
]

def afficher_patient(patient):
    return f"""
# {patient['prenom']} {patient['nom']}
- **Âge**: {patient['mental']}
- **Dernière visite**: {patient['derniere_visite']}
"""

css = """
#patient-info-section { 
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    height: calc(100vh - 250px) !important;
    max-height: 350px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.patient-btn { 
    width: 100% !important;
    text-align: left !important;
    justify-content: start !important;
    padding: 12px 20px !important;
}

#doctor-profile-top { 
    text-align: center;
    padding: 10px;
    border-left: 1px solid #e0e0e0;
}

.gradio-container {
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
}

div[data-testid="row"]:not(:first-child) {
    flex: 1 !important;
    align-items: stretch !important;
}


#initial-state {
    text-align: center;
    height: 100%;
    display: flex !important;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 20px;
}
#patient-details {
    width: 100%;
    height: 100%;
}

#initial-state h2 {
    font-size: 1.8em !important;
    font-weight: 600 !important;
}

#initial-state p {
    font-size: 1.1em !important;
    max-width: 400px;
    margin: 0 auto;
}
"""

with gr.Blocks(css=css) as app:
    # En-tête
    with gr.Row():
        gr.Image("https://cmipq.com/wp-content/uploads/2019/06/AdobeStock_125985403_1200x675-min.jpg", elem_id="logo-healthbot", show_label=False, width=100)
        gr.Markdown("<h1 style='text-align: center; margin-top: 75px; font-size: 30px;'>🧑⚕️ TABLEAU DE BORD MÉDECIN</h1>")
        with gr.Column(elem_id="doctor-profile-top"):
            gr.Markdown("<h1 style='text-align: center; font-size: 20px;'>Dr. Amal</h1>")
            gr.Image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ40hNbhCXk86JOrO8LbDzusmR-kiqwFl_SeQ&s", show_label=False, width=50)

    # Corps principal
    with gr.Row():
        # Liste des patients
        with gr.Column(scale=2, min_width=300):
            gr.Markdown("## Liste des Patients")
            with gr.Accordion("Afficher les patients", open=True):
                patient_buttons = []
                for patient in patients:
                    btn = gr.Button(
                        f"{patient['prenom']} {patient['nom']} | {patient['mental']}",
                        elem_classes="patient-btn"
                    )
                    patient_buttons.append(btn)
        
        # Détails du patient
        with gr.Column(scale=5, elem_id="patient-info-section"):
            with gr.Column(visible=True, elem_id="initial-state") as initial_state:
                

                gr.Markdown(
            """
            <div style='text-align: center;'>
                <h2><div style='font-size: 80px;'> 😷🩺🛌</div></h2>
            </div>
            """
        )
                gr.Markdown("""
                    <div style='text-align: center; margin-top: 20px;'>
                        <h2 style='margin-bottom: 10px; color: #2c3e50;'>👈 Sélectionnez un patient</h2>
                        <p style='color: #7f8c8d; font-size: 16px;'>
                            Cliquez sur un patient dans la liste à gauche pour afficher son dossier complet
                        </p>
                    </div>
                """)
            
            patient_info = gr.Markdown(visible=False, elem_id="patient-details")


    # Gestion des événements
    for btn, patient in zip(patient_buttons, patients):
        btn.click(
            fn=lambda p=patient: afficher_patient(p),
            inputs=[],
            outputs=patient_info
        )

app.launch()