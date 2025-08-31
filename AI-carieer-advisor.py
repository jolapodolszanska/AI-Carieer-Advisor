"""
AI Career Advisor (PL) – wersja Gradio
-------------------------------------------------
Uruchamianie:
1) pip install -U spacy gradio pandas
2) python -m spacy download pl_core_news_md
3) python app_gradio_career_advisor.py

Uwaga: jeśli nie ma modelu 'md', skrypt spróbuje użyć 'pl_core_news_sm'.
"""

from __future__ import annotations
import pandas as pd
import spacy
import gradio as gr
from typing import List, Tuple

# ---------- ładowanie modelu spaCy ----------

def load_pl_model():
    try:
        return spacy.load("pl_core_news_md")
    except Exception:
        try:
            return spacy.load("pl_core_news_sm")
        except Exception as e:
            raise RuntimeError(
                "Brakuje modelu spaCy dla PL. Uruchom: python -m spacy download pl_core_news_md"
            ) from e

nlp = load_pl_model()

# ---------- dane zawodów ----------
CAREERS = [
    {"Zawód": "Data Scientist", "Opis": "Analiza danych, uczenie maszynowe, statystyka, programowanie."},
    {"Zawód": "Lekarz/-ka", "Opis": "Medycyna, anatomia, farmakologia, diagnozowanie, leczenie."},
    {"Zawód": "Inżynier Oprogramowania", "Opis": "Programowanie, algorytmy, bazy danych, aplikacje webowe."},
    {"Zawód": "Grafik/-czka komputerowy", "Opis": "Adobe Photoshop, projektowanie, ilustracja, kreatywność, grafika komputerowa."},
    {"Zawód": "Psycholog", "Opis": "Psychologia, terapia, emocje, badania nad zachowaniem."},
    {"Zawód": "Analityk/-czka finansowy", "Opis": "Ekonomia, analiza finansowa, inwestycje, matematyka."},
    {"Zawód": "Animator/-ka 3D", "Opis": "Animacja 3D, modelowanie, efekty specjalne, rendering."},
    {"Zawód": "Fotograf/-fka", "Opis": "Fotografia, edycja zdjęć, obróbka graficzna, sesje zdjęciowe."},
    {"Zawód": "Architekt/-tka", "Opis": "Projektowanie budynków, rysunek techniczny, urbanistyka."},
    {"Zawód": "Specjalista/-stka bezpieczeństwa psychologicznego dzieci", "Opis": "Psychologia dziecięca, rozwój dziecka, wsparcie psychologiczne."},
    {"Zawód": "Specjalista/-stka ds. konsultingu", "Opis": "Doradztwo biznesowe, zarządzanie projektami, optymalizacja procesów."},
    {"Zawód": "Mechanik/-czka maszyn i urządzeń", "Opis": "Mechanika, konserwacja maszyn, inżynieria techniczna."},
]

DF = pd.DataFrame(CAREERS)

# ---------- logika dopasowania ----------

def compute_matches(user_interests: str, top_k: int = 3) -> Tuple[pd.DataFrame, str]:
    text = (user_interests or "").strip()
    if not text:
        empty = pd.DataFrame({"Zawód": [], "Dopasowanie": []})
        return empty, "<i>Wpisz swoje zainteresowania powyżej.</i>"

    user_doc = nlp(text.lower())
    scores: List[float] = []

    for desc in DF["Opis"].tolist():
        job_doc = nlp(desc.lower())
        sim = user_doc.similarity(job_doc)
        # przeskalowanie do % (0..100)
        scores.append(max(0.0, min(100.0, sim * 100)))

    tmp = DF.copy()
    tmp["Dopasowanie"] = scores
    tmp_sorted = tmp.sort_values("Dopasowanie", ascending=False).head(int(top_k)).reset_index(drop=True)

    # tabelka dla widoku
    show_df = tmp_sorted[["Zawód", "Dopasowanie"]].copy()
    show_df["Dopasowanie"] = show_df["Dopasowanie"].map(lambda x: f"{x:.2f}%")

    # HTML z paskami postępu + opisy
    bars = []
    for _, row in tmp_sorted.iterrows():
        pct = float(row["Dopasowanie"])  # 0..100
        bars.append(
            f"""
            <div class='card'>
                <div class='title'>{row['Zawód']}</div>
                <div class='desc'>{row['Opis']}</div>
                <div class='bar-wrap'>
                    <div class='bar' style='width:{pct:.2f}%;'></div>
                </div>
                <div class='pct'>{pct:.2f}% dopasowania</div>
            </div>
            """
        )
    html = "\n".join(bars)
    return show_df, html

# ---------- interfejs Gradio ----------

THEME = gr.themes.Soft()

CSS = """
body { background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%); }
.gradio-container { max-width: 1000px !important; }
.hero { text-align: center; padding: 1.25rem 0 0.25rem; }
.hero h1 { margin: 0; font-weight: 800; letter-spacing: -0.02em; }
.hero p { color: #475569; margin-top: .5rem; }
.card { background: #ffffffcc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 14px; box-shadow: 0 4px 16px rgba(0,0,0,.06); margin-bottom: 10px; }
.title { font-weight: 700; }
.desc { color:#475569; font-size: .92rem; margin: .25rem 0 .5rem; }
.bar-wrap { height: 10px; background:#e2e8f0; border-radius: 9999px; overflow: hidden; }
.bar { height: 100%; background: linear-gradient(90deg,#60a5fa,#34d399); }
.pct { font-size:.85rem; color:#334155; margin-top:.35rem; }
.footer { text-align:center; color:#6b7280; font-size:.85rem; margin-top:.75rem; }
"""

with gr.Blocks(theme=THEME, css=CSS) as demo:
    gr.HTML("""
    <div class='hero'>
      <h1>AI Career Advisor</h1>
      <p>Wpisz swoje zainteresowania, a podpowiemy zawody najlepiej do nich pasujące.</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            interests = gr.Textbox(
                label="Twoje zainteresowania",
                placeholder="Np. programowanie w Pythonie, analiza danych medycznych, grafika 3D...",
                lines=3,
                autofocus=True,
            )
            topk = gr.Slider(1, 10, value=3, step=1, label="Ile propozycji pokazać?")
            with gr.Row():
                run_btn = gr.Button("Znajdź zawód", variant="primary")
                clear_btn = gr.Button("Wyczyść")

            gr.Examples(
                examples=[
                    ["analiza danych, statystyka, modele uczenia maszynowego"],
                    ["praca z dziećmi, wsparcie psychologiczne, rozwój emocjonalny"],
                    ["rysunek techniczny, architektura, urbanistyka"],
                    ["grafika, photoshop, ilustracje, kreatywność"],
                ],
                inputs=[interests],
                label="Przykłady",
            )
        with gr.Column(scale=1):
            out_df = gr.Dataframe(label="Najlepsze dopasowania", interactive=False)
            out_html = gr.HTML()

    # akcje
    run_btn.click(fn=compute_matches, inputs=[interests, topk], outputs=[out_df, out_html])
    interests.submit(fn=compute_matches, inputs=[interests, topk], outputs=[out_df, out_html])
    clear_btn.click(lambda: (None, ""), outputs=[out_df, out_html])

    gr.HTML("""
    <div class='footer'>
      Wskazówka: dla najlepszych wyników zainstaluj model <code>pl_core_news_md</code> (ma wektory leksykalne).
    </div>
    """)

if __name__ == "__main__":
    demo.launch()
