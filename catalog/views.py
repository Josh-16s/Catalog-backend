from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Branch, Product, Category
from .serializers import BranchSerializer, ProductSerializer, CategorySerializer



# Branch ViewSet (NO AUTH REQUIRED)
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
  
    permission_classes = []  

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        branch = self.get_object()
        products = Product.objects.filter(branch=branch)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = []
        for branch in Branch.objects.all():
            product_count = Product.objects.filter(branch=branch).count()
            stats.append({
                'branch': BranchSerializer(branch).data,
                'product_count': product_count
            })
        return Response(stats)

# Category ViewSet (NO AUTH REQUIRED)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    permission_classes = []

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from catalog.models import Product, Category, Branch
from .serializers import ProductSerializer
from django.db.models import Count, Min

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = []

    def get_queryset(self):
        # Start with all products
        queryset = Product.objects.all()

        # Get query parameters
        branch_id = self.request.query_params.get('branch', None)
        category_id = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)

        # Apply filters
        if branch_id is not None:
            queryset = queryset.filter(branch=branch_id)
        if category_id is not None:
            queryset = queryset.filter(category=category_id)
        if search is not None:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )

        # Group by name to get unique products, selecting the first instance (by id)
        queryset = queryset.values('name', 'description', 'category', 'price', 'unit', 'on_sale', 'sale_price', 'image').annotate(
            min_id=Min('id')
        ).order_by('name')

        # Rebuild queryset to include full Product objects, using the minimum id
        queryset = Product.objects.filter(id__in=[item['min_id'] for item in queryset])

        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        print("Request data:", request.data)
        
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        products = Product.objects.filter(on_sale=True)
        # Ensure unique products for on_sale endpoint
        products = products.values('name', 'description', 'category', 'price', 'unit', 'on_sale', 'sale_price', 'image').annotate(
            min_id=Min('id')
        )
        products = Product.objects.filter(id__in=[item['min_id'] for item in products])
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        return Response([])

    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Update stats to reflect unique products
        unique_products = Product.objects.values('name').annotate(count=Count('id')).count()
        on_sale_products = Product.objects.filter(on_sale=True).values('name').annotate(count=Count('id')).count()
        categories_count = Category.objects.count()
        branches_count = Branch.objects.count()

        return Response({
            'total_products': unique_products,
            'on_sale_products': on_sale_products,
            'categories_count': categories_count,
            'branches_count': branches_count
        })
# Admin Dashboard View (NO AUTH REQUIRED)
from rest_framework.views import APIView

class AdminDashboardView(APIView):
    permission_classes = []

    def get(self, request):
        dashboard_data = {
            'total_products': Product.objects.count(),
            'total_branches': Branch.objects.count(),
            'total_categories': Category.objects.count(),
            'products_on_sale': Product.objects.filter(on_sale=True).count(),
            'recent_products': ProductSerializer(
                Product.objects.order_by('-id')[:5],
                many=True
            ).data
        }
        return Response(dashboard_data)
