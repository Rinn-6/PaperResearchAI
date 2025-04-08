from django.urls import path
from .views import LangChainAgentView, SimilarPapersView

urlpatterns = [
    path('analyze-paper/', LangChainAgentView.as_view(), name='analyze_paper'),
    path('similar-papers/', SimilarPapersView.as_view(), name='similar_papers'),
]

