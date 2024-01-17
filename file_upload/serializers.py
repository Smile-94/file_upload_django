from rest_framework import serializers

from file_upload.models import Product

class InputSerializers(serializers.Serializer):
    data_table = serializers.CharField(max_length=20)
    file = serializers.FileField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'