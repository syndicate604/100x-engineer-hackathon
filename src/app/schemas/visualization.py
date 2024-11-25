from typing import List
from pydantic import BaseModel, Field

class TrendVisualizationResponse(BaseModel):
    """Response model for market trend visualization"""
    
    img: str = Field(..., description="Base64 encoded image of the trend visualization")
    reason: str = Field(..., description="Detailed reasoning behind the trend visualization")
    insights: List[str] = Field(..., description="Key strategic insights derived from the visualization")

class VisualizationMetadata(BaseModel):
    """Metadata for the visualization"""
    
    title: str = Field(..., description="Title of the visualization")
    x_axis_label: str = Field(..., description="Label for the x-axis")
    y_axis_label: str = Field(..., description="Label for the y-axis")
    metrics: List[str] = Field(..., description="List of metrics visualized")
    date_generated: str = Field(..., description="Timestamp of visualization generation")

class DetailedTrendVisualization(TrendVisualizationResponse):
    """Comprehensive trend visualization response"""
    
    metadata: VisualizationMetadata = Field(..., description="Additional metadata about the visualization")
    confidence_score: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Confidence score of the trend analysis (0-1)"
    )
