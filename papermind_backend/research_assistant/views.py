from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .langchain_agent import gemini_agent
from .utils import get_embedding_from_text  
from .models import ResearchPaper  
import numpy as np
import faiss
 


class LangChainAgentView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        pdf_file = request.FILES.get("file")
        if not pdf_file:
            return Response({"error": "No file uploaded"}, status=400)

        # Save temp file
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            for chunk in pdf_file.chunks():
                temp.write(chunk)
            temp_path = temp.name

        try:
            # Run LangChain agent
             result = gemini_agent(temp_path)
             print("Gemini Agent Result:", result)
             summary = result.get("summary", "")
             title = summary[:100]  # or generate from metadata

             embedding = get_embedding_from_text(summary)

             paper = ResearchPaper.objects.create(
                title=title,
                embedding=embedding
            )

             result["paper_id"] = paper.id  # include ID for frontend to fetch similar
        finally:
            os.remove(temp_path)

        return Response(result)



class SimilarPapersView(APIView):
    def get(self, request):
        paper_id = request.query_params.get("paper_id")
        if not paper_id:
            return Response({"error": "Missing paper_id"}, status=400)

        try:
            paper = ResearchPaper.objects.get(id=paper_id)
        except ResearchPaper.DoesNotExist:
            return Response({"error": "Paper not found"}, status=404)

        all_papers = ResearchPaper.objects.exclude(id=paper_id)
        if not all_papers:
            return Response([], status=200)

        embeddings = np.array([p.embedding for p in all_papers], dtype="float32")
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        query_vector = np.array(paper.embedding, dtype="float32").reshape(1, -1)
        _, indices = index.search(query_vector, k=min(5, len(all_papers)))

        similar_titles = [all_papers[i].title for i in indices[0]]
        return Response(similar_titles)