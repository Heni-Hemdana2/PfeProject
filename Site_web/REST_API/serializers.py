from rest_framework import serializers
from django.contrib.auth import authenticate
from Superviseur.models import DetectionResult
import os

class LoginSerializer(serializers.Serializer):
    # Définition des champs de saisie pour les informations de connexion
    pseudo = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        # Extraction du nom d'utilisateur et du mot de passe à partir des données validées
        pseudo = attrs.get('pseudo')
        password = attrs.get('password')

        if pseudo and password:
            # Authentification de l'utilisateur avec les informations fournies
            user = authenticate(username=pseudo, password=password)
            if user:
                if not user.is_active:
                    # Si le compte utilisateur est désactivé, lever une erreur de validation
                    raise serializers.ValidationError('User account is disabled.')
                # Si l'authentification réussit et l'utilisateur est actif,
                # ajouter l'utilisateur aux données validées
                attrs['user'] = user
            else:
                # Lever une erreur de validation si l'authentification échoue
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            # Lever une erreur de validation si le nom d'utilisateur ou le mot de passe est manquant
            raise serializers.ValidationError('Must include "username" and "password".')

        # Retourner les données validées
        return attrs
    pass

class DetectionImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    detection_time = serializers.DateTimeField(source='detected_at', read_only=True)
    camera_name = serializers.CharField(source='camera_name.name_cam', read_only=True)
    
    class Meta:
        model = DetectionResult
        fields = ['id', 'camera_name', 'detection_time', 'image_url', 'detection_data']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.path_to_image and os.path.exists(obj.path_to_image):
            # Convertir le chemin absolu en URL relative
            # On suppose que MEDIA_URL est configuré correctement dans settings.py
            media_path = obj.path_to_image.split('media/')[-1] if 'media/' in obj.path_to_image else obj.path_to_image
            return request.build_absolute_uri(f'/media/{media_path}')
        return None
