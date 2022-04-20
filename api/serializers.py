from rest_framework import serializers
from . import models
from django.utils import timezone


class WhiteIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WhiteIP
        fields = '__all__'
        read_only_fields = ("create_at", "update_at")

    def validate_ip(self, value):
        if value == "192.168.1.106":
            raise serializers.ValidationError("You are blocked!")
        else:
            return value

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.created_at = timezone.now()
        obj.save()
        return obj

    def update(self, instance, validated_data):
        old_created_at = instance.created_at
        obj = super().update(instance, validated_data)
        obj.created_at = old_created_at
        obj.updated_at = timezone.now()
        obj.save()
        return obj


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = '__all__'
        read_only_fields = ("date", )


