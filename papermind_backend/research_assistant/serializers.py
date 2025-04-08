from rest_framework import serializers
from .models import ResearchPaper

# This serializer converts the ResearchPaper model instances into JSON format and vice versa.
class ResearchPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchPaper
        fields = '__all__'