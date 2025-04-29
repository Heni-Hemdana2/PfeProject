from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, DetectionImageSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from Superviseur.models import DetectionResult, Cam
from rest_framework.pagination import PageNumberPagination
import os
from django.http import FileResponse
from django.conf import settings
import glob


class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    

class DetectionResultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class DetectionListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DetectionResultPagination
    
    def get(self, request):
        # Récupérer les paramètres de filtrage
        camera_name = request.query_params.get('camera', None)
        limit = int(request.query_params.get('limit', 10))
        
        # Construire la requête de base
        queryset = DetectionResult.objects.all().order_by('-detected_at')
        
        # Appliquer le filtre par caméra si nécessaire
        if camera_name:
            queryset = queryset.filter(camera_name__name_cam=camera_name)
        
        # Limiter le nombre de résultats
        queryset = queryset[:limit]
        
        # Sérialiser les résultats
        serializer = DetectionImageSerializer(queryset, many=True, context={'request': request})
        
        return Response(serializer.data)

class LatestDetectionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, camera_name=None):
        try:
            # Filtrer par caméra si spécifié
            if camera_name:
                # Vérifier si la caméra existe
                try:
                    cam = Cam.objects.get(name_cam=camera_name)
                except Cam.DoesNotExist:
                    return Response({"error": "Camera not found"}, status=status.HTTP_404_NOT_FOUND)
                
                # Récupérer la dernière détection pour cette caméra
                detection = DetectionResult.objects.filter(camera_name=cam).order_by('-detected_at').first()
            else:
                # Récupérer la dernière détection toutes caméras confondues
                detection = DetectionResult.objects.all().order_by('-detected_at').first()
            
            if detection:
                serializer = DetectionImageSerializer(detection, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({"error": "No detection found"}, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LatestYoloImageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Trouver le dernier dossier de prédiction YOLO
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            predict_dirs = sorted(glob.glob(os.path.join(base_dir, 'runs', 'detect', 'predict*')))
            
            if not predict_dirs:
                return Response({"error": "No YOLO prediction folders found"}, status=status.HTTP_404_NOT_FOUND)
            
            latest_dir = predict_dirs[-1]
            
            # Trouver la dernière image dans ce dossier
            images = sorted(glob.glob(os.path.join(latest_dir, '*.jpg')) + 
                           glob.glob(os.path.join(latest_dir, '*.png')),
                           key=os.path.getmtime)
            
            if not images:
                return Response({"error": "No images found in latest prediction folder"}, status=status.HTTP_404_NOT_FOUND)
            
            latest_image = images[-1]
            
            # Renvoyer l'image
            return FileResponse(open(latest_image, 'rb'), content_type='image/jpeg')
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)