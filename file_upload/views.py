from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
import csv
from decimal import Decimal

#Import Models
from file_upload.models import Product
from file_upload.models import Category
from file_upload.serializers import ProductSerializer
from file_upload.serializers import InputSerializers

# Create your views here.

class ProductUploadView(CreateAPIView):
    serializer_class = InputSerializers
   
    def post(self, request, *args, **kwargs):
        serializer = InputSerializers(data=request.data)
        table_key = ('product', 'category')
        reader = None

        if serializer.is_valid():
            # Access the validated data using serializer.validated_data
            data_table = serializer.validated_data.get('data_table')
            uploaded_file = serializer.validated_data.get('file')
            
            # Check if the file has a CSV extension
            if not uploaded_file.name.lower().endswith('.csv'):
                return Response({'errors': 'Invalid file type. Please upload a CSV file.'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                decoded_file = uploaded_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
            
            if data_table not in table_key:
                return Response({'errors': f"data table should be {table_key}, but you have given '{data_table}'"}, status=status.HTTP_400_BAD_REQUEST)
                
        if data_table == 'product':
            product_table_key = ('product_name', 'product_category', 'product_location', 'stock', 'product_price', 'product_vat', 'product_discount', 'product_barcode', )
        
            if reader is not None:
                error_list = []
                seen_barcode = set()
                for row_number, row in enumerate(reader, start=2):
                       
                    for key, value in row.items():
                        
                        if key not in product_table_key:
                            error_list.append(f"Row {row_number}: Invalid: key '{key}' or Value:'{value}'")
                        
                        if key == 'product_name':
                            if value=="" or None:
                                error_list.append(f"Row {row_number}: '{key}' cannot be empty")
                            
                            if value.isdigit():
                                error_list.append(f"Row {row_number}: '{key}' cannot be a number")

                            
                        if key == 'product_category':
                            if not Category.objects.filter(category_name=value).exists():
                                error_list.append(f"Row {row_number}: '{key}' '{value}' does not exist")
                        
                        if key == 'product_location':
                            
                            if value == "" or None:
                                error_list.append(f"Row {row_number}: '{key}' cannot empty")
                            
                            elif value not in ['private_box','medicare','food']:
                                error_list.append(f"Row {row_number}: '{key}' '{value}' not a valid choices")
                        
                        if key == 'stock':
                            try:
                                int(value)
                            except Exception:
                                error_list.append(f"Row {row_number}: '{key}', must be a valid Integer, but you haven given {value}")
                        
                        if key in ['product_price', 'product_vat', 'product_discount']:
                            try:
                                 Decimal(value)
                                
                            except Exception:
                                error_list.append(f"Row {row_number}: {key} must be a valid decimal, but you have given '{value}'.")
                        
                        if key == 'product_barcode':
                            if Product.objects.filter(product_barcode=value).exists():
                                error_list.append(f"Row {row_number}: '{key}' '{value}' already exists")
                                
                            if value in seen_barcode:
                                
                                error_list.append(f"Row {row_number}: '{key}' '{value}' already exists in the CSV file")
                                
                            else:
                                seen_barcode.add(value)
                    
                if error_list:
                    return Response({'errors': error_list}, status=status.HTTP_400_BAD_REQUEST)
                
                
                
                # Reset the file pointer to the beginning
                uploaded_file.seek(0)
                # Read the CSV file again for the second loop
                decoded_file = uploaded_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                database_error = []
                uploaded_product = []
                serializer = None
                for row_number, row in enumerate(reader, start=2):
                    
                    for key, value in row.items():
                        if key == 'product_category':
                            category = Category.objects.get(category_name=value)
                            row['product_category'] = category.id
                    
                    serializer = ProductSerializer(data=row)
                    if serializer.is_valid():
                        serializer.save()
                        uploaded_product.append({'id':serializer.data.get('id'), 'product_name':serializer.data.get('product_name')})
                    else:
                        database_error.append({f"Row {row_number}":serializer.errors})
                    
                    
            
                return Response({'database_errors':database_error,'uploaded_product':uploaded_product,'message': 'Products uploaded successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

