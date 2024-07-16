from django.http import HttpResponse
from django.http.response import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import HttpResponse
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from qdrant_client import QdrantClient, models
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

load_dotenv()


def index(request):
    return HttpResponse('ITS Running')


class HybridSearcher:

    def __init__(self, qdrant_url, qdrant_api_key, collection_name):
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        self.collection_name = collection_name
        # Initialize Qdrant client
        self.client = QdrantClient(url=self.qdrant_url,
                                   api_key=self.qdrant_api_key,
                                   prefer_grpc=True)
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2")

    def hybrid_search(self, query, limit=5):
        # Vector search
        vector_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=self.embeddings.embed_query(query),
            limit=limit)

        # Text search
        text_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=self.embeddings.embed_query(query),
            query_filter=models.Filter(must=[
                models.FieldCondition(key="page_content",
                                      match={"text": query})
            ]),
            limit=limit)

        # Combine and sort results
        combined_results = []
        for result in vector_results + text_results:
            if result.payload and "page_content" in result.payload:
                doc = Document(page_content=result.payload["page_content"],
                               metadata=result.payload.get("metadata", {}))
                combined_results.append((doc, result.score))

        sorted_results = sorted(combined_results,
                                key=lambda x: x[1],
                                reverse=True)

        return sorted_results[:limit]

    def format_search_results(self, results):
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "score": score,
                "text": doc.page_content,
                "metadata": doc.metadata
            })
        return formatted_results


@api_view(['POST'])
def ravinew(request):
    if request.method == 'POST':
        try:
            data = request.data
            query = data.get('query')

            if not query:
                return Response({"error": "Query is required"}, status=400)

            QDRANT_URL = os.getenv('QDRANT_URL')
            QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
            COLLECTION_NAME = "Ravi_Work_quick_new"

            searcher = HybridSearcher(QDRANT_URL, QDRANT_API_KEY,
                                      COLLECTION_NAME)
            results = searcher.hybrid_search(query)
            formatted_results = searcher.format_search_results(results)
            return Response({"query": query, "results": formatted_results})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    return Response({"error": "Only POST requests are allowed"}, status=405)

'''
@csrf_exempt
@api_view(['POST'])
def ravinew(request):
    if request.method == 'POST':
        data = request.data
        query = data.get('query')
        QDRANT_URL = os.getenv("QDRANT_URL")
        QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

        collection_name = "Ravi_Work_quick_new"
        embeddings = HuggingFaceEmbeddings()

        query_vector = embeddings.embed_query(query)
        search_result = client.search(collection_name=collection_name,
                                      query_vector=query_vector,
                                      limit=1)

        if search_result:
            top_result = search_result[0]
            print(f"Score: {top_result.score}")
            print(f"Text: {top_result.payload['text']}")
            print(f"Metadata: {top_result.payload['metadata']}")
            return HttpResponse(top_result.payload['text'],
                                content_type='text/plain')
        else:
            return HttpResponse("No matching documents found.",
                                content_type='text/plain')

    return JsonResponse({'error': 'Invalid request method'}, status=400)
'''
'''
@csrf_exempt
@api_view(['POST'])
def ravinew(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            collection_name = data.get('collection_name',
                                       'ravi_work_quick_new_hybrid')
            limit = data.get('limit', 5)

            if not query:
                return JsonResponse({"error": "Query is required"}, status=400)

            qdrant_client = QdrantClient(
                "https://dc5ccf61-035c-401f-a05c-36a2dea45e13.us-east4-0.gcp.cloud.qdrant.io",
                api_key="bclgpbFspJouOCD3If3nqQdl3VyOO_yWfLjsuwvVNYt9o_CV3LbPzg"
            )
            model = SentenceTransformer('all-MiniLM-L6-v2')

            # Encode query
            query_vector = model.encode(query).tolist()

            # Perform search
            search_result = qdrant_client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit)

            # Format results
            formatted_results = []
            for result in search_result:
                formatted_results.append({
                    "score": result.score,
                    "text": result.payload.get('text', '')
                })

            return JsonResponse({"query": query, "results": formatted_results})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"},
                                status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"},
                        status=405)
'''
'''
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from qdrant_client import QdrantClient, models
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document


class HybridSearcher:

    def __init__(self, qdrant_url, qdrant_api_key, collection_name):
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        self.collection_name = collection_name

        # Initialize Qdrant client
        self.client = QdrantClient(url=self.qdrant_url,
                                   api_key=self.qdrant_api_key,
                                   prefer_grpc=True)

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2")

    def hybrid_search(self, query, limit=5):
        search_results = self.client.query(
            collection_name=self.collection_name,
            query_text=query,
            query_vector=self.embeddings.embed_query(query),
            query_filter=None,  # You can add filters if needed
            limit=limit)

        results = []
        for hit in search_results:
            if hit.payload and "page_content" in hit.payload:
                doc = Document(page_content=hit.payload["page_content"],
                               metadata=hit.payload.get("metadata", {}))
                results.append((doc, hit.score))

        return results

    def format_search_results(self, results):
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "score": score,
                "text": doc.page_content,
                "metadata": doc.metadata
            })
        return formatted_results


# Django view
@csrf_exempt
@api_view(['POST'])
def ravinew(request):
    if request.method == 'POST':
        try:
            data = request.data
            query = data.get('query')

            if not query:
                return Response({"error": "Query is required"}, status=400)

            QDRANT_URL = "https://dc5ccf61-035c-401f-a05c-36a2dea45e13.us-east4-0.gcp.cloud.qdrant.io:6333"
            QDRANT_API_KEY = "bclgpbFspJouOCD3If3nqQdl3VyOO_yWfLjsuwvVNYt9o_CV3LbPzg"
            COLLECTION_NAME = "ravi_work_quick_new_hybrid"

            searcher = HybridSearcher(QDRANT_URL, QDRANT_API_KEY,
                                      COLLECTION_NAME)
            results = searcher.hybrid_search(query)
            formatted_results = searcher.format_search_results(results)

            return Response({"query": query, "results": formatted_results})

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response({"error": "Only POST requests are allowed"}, status=405)
'''
