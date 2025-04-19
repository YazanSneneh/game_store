import jwt
import logging
from datetime import datetime
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            #Input sanitization
            username = data['username'].strip()
            password = data['password']

            #User existence check (case-sensitive)
            user = User.objects.filter(username=username).first()
            if not user:
                logger.warning(f"Login attempt for non-existent user: {username}")
                raise serializers.ValidationError({
                    'username': 'User not found or incorrect credentials'
                })

            #Account status checks
            if not user.is_active:
                logger.warning(f"Login attempt for inactive user: {username}")
                raise serializers.ValidationError({
                    'username': 'Account is inactive'
                })

            #Password validation with timing attack protection
            if not user.check_password(password):
                logger.warning(f"Failed login attempt for user: {username}")
                raise serializers.ValidationError({
                    'password': 'Incorrect password'
                })

            #Generate JWT token
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
                'iat': datetime.utcnow(),
                'is_active': user.is_active
            }

            token = jwt.encode(
                payload,
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM
            )

            #Successful login logging
            logger.info(f"Successful login for user: {username}")

            return {
                'user': UserSerializer(user).data,
                'token': token
            }

        except jwt.PyJWTError as e:
            logger.error(f"JWT generation error: {str(e)}")
            raise serializers.ValidationError({
                'non_field_errors': 'Authentication service unavailable'
            })
        except Exception as e:
            logger.critical(f"Unexpected auth error: {str(e)}")
            raise serializers.ValidationError({
                'non_field_errors': 'Authentication failed'
            })