from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class NewsAnalysisRequest(BaseModel):
    title: Optional[str] = Field(default="", description="The headline or title of the news article")
    text: str = Field(..., min_length=10, description="The main text body of the news article")

class FeatureContribution(BaseModel):
    word: str = Field(..., description="The word token analyzed")
    weight: float = Field(..., description="The contribution weight towards/against the predicted class")
    tfidf: float = Field(..., description="The TF-IDF value of the word in this document")
    model_coef: float = Field(..., description="The model's coefficient/log-odds weight for this word")

class NewsAnalysisResponse(BaseModel):
    prediction: str = Field(..., description="Classification outcome: LIKELY_FAKE or LIKELY_GENUINE")
    confidence: float = Field(..., description="Confidence percentage [0-1] for the prediction")
    model_name: str = Field(..., description="Name of the model used for classification")
    supporting_features: List[FeatureContribution] = Field(..., description="Words supporting the prediction")
    opposing_features: List[FeatureContribution] = Field(..., description="Words opposing the prediction")
    word_count: int = Field(..., description="Total word count of the processed input text")
    character_count: int = Field(..., description="Total character count of the processed input text")
    disclaimer: str = Field(
        default="TruthLens provides a machine-learning-based classification based on patterns learned from labelled training data. It does not independently verify factual claims. Predictions may be incorrect, so important information should always be verified using reliable independent sources.",
        description="Standard academic research disclaimer"
    )

class ModelMetric(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float

class DatasetStatisticsResponse(BaseModel):
    raw_record_count: int
    clean_record_count: int
    columns: List[str]
    missing_values: Dict[str, int]
    duplicate_records: int
    class_distribution: Dict[str, int]
    class_percentages: Dict[str, float]
    text_length: Dict[str, Any]
    splits: Dict[str, int]

class ModelInfoResponse(BaseModel):
    best_model_name: str
    validation_metrics: Dict[str, float]
    test_metrics: Optional[Dict[str, float]] = None
    hyperparameters: Dict[str, Any]
