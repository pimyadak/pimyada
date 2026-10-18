from rest_framework import serializers
from .models import person  # <--- เปลี่ยนเป็นชื่อ Model จริงของคุณ

class personSerializer(serializers.ModelSerializer):
    class Meta:
        model = person      # <--- เปลี่ยนเป็นชื่อ Model จริงของคุณ
        fields = '__all__'