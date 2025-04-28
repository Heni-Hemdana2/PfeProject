from rest_framework import serializers
from django.contrib.auth import authenticate

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
