from fastapi import APIRouter
from backend.app.schemas.analysis import NewsAnalysisRequest, NewsAnalysisResponse
from backend.app.services.predictor import PredictorService
from backend.app.services.explainer import ExplainerService

router = APIRouter()

@router.post("/analyze", response_model=NewsAnalysisResponse)
def analyze_news(request: NewsAnalysisRequest):
    # 1. Run prediction
    pred_res = PredictorService.predict(request.title, request.text)
    
    # 2. Run explanation using preprocessed combined text
    explain_res = ExplainerService.explain(pred_res["combined_text"], pred_res["prediction"])
    
    # 3. Compile word counts and response
    words = pred_res["combined_text"].split()
    word_count = len(words)
    char_count = len(pred_res["combined_text"])
    
    return NewsAnalysisResponse(
        prediction=pred_res["prediction"],
        confidence=pred_res["confidence"],
        model_name=pred_res["model_name"],
        supporting_features=explain_res["supporting_features"],
        opposing_features=explain_res["opposing_features"],
        word_count=word_count,
        character_count=char_count
    )

@router.get("/sample-articles")
def get_sample_articles():
    """
    Returns a small set of clearly labelled demo examples for testing the UI.
    """
    return [
        {
            "id": 1,
            "label": "DEMO ARTICLE — LIKELY GENUINE (Reuters)",
            "title": "U.N. seeks humanitarian pause in Sanaa where streets become battlegrounds",
            "text": "The United Nations on Sunday called for a humanitarian pause in Yemen's capital Sanaa to allow civilians to leave their homes, seek medical assistance and obtain food and water, as clashes escalated. The international organization expressed deep concern over the heavy fighting and civilian casualties in the city. Streets have become battlegrounds, blocking access to hospitals and trapping residents. Relief coordinators urged all parties to stop hostilities immediately to protect vulnerable populations and aid workers."
        },
        {
            "id": 2,
            "label": "DEMO ARTICLE — LIKELY FAKE (Sensationalist Blog)",
            "title": "UNBELIEVABLE! CLINTON FOUNDATION RECEIVED MILLIONS IN CASH FROM ALIEN LOBBY GROUP!",
            "text": "In a shocking turn of events, a secret leaked document has revealed that the Clinton Foundation received millions of dollars in cash payments from a mysterious alien lobby group claiming to represent extraterrestrial interests. According to the document, the payments were made during the height of the presidential campaign. This shocking discovery has left the public stunned, and mainstream media is refusing to cover this massive cover-up! Investigators are calling it the biggest scandal in modern history! SHARE this article everywhere before it gets taken down by the elite!"
        },
        {
            "id": 3,
            "label": "DEMO ARTICLE — AMBIGUOUS (Mixed/Opinion Piece)",
            "title": "Is the New Social Media Regulation Really Good for Public Speech?",
            "text": "A new regulation proposed by the government aims to curb online hate speech by imposing fines on social media platforms that fail to remove illegal content. Proponents argue this is a necessary step to protect citizens and maintain civil discourse. However, critics point out that this could lead to widespread censorship, as companies might err on the side of caution and remove legitimate speech. The debate highlights the complex balance between maintaining security and protecting the fundamental right to free expression online."
        }
    ]
