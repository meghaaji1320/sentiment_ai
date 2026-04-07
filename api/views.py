import asyncio
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TextSerializer
from .services import analyze_sentiment


def format_result(result):
    label_map = {
        "LABEL_0": "negative",
        "LABEL_1": "neutral",
        "LABEL_2": "positive"
    }

    scores = result[0]
    top = max(scores, key=lambda x: x["score"])

    return {
        "sentiment": label_map.get(top["label"], "unknown"),
        "confidence": top["score"]
    }

class SentimentView(APIView):

    def post(self, request):   # ✅ FIXED
        serializer = TextSerializer(data=request.data)

        if serializer.is_valid():
            text = serializer.validated_data['text']

            try:
                raw_result = asyncio.run(analyze_sentiment(text))  # ✅ FIXED
                formatted = format_result(raw_result)

                return Response({
                    "success": True,
                    "data": formatted
                })

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)