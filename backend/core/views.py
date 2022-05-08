# from core.filters import UserFilter
# from core.models import User
# from core.serializers import UserSerializer, TokenUserSerializer
# from core.utils import run_async
# from django_filters import rest_framework as filters
# from notifications.services import notification_service
# from rest_framework import viewsets
# from rest_framework.filters import OrderingFilter
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
#     filter_class = UserFilter
#     http_method_names = ['get', 'post', 'patch', 'delete', 'options']
#
#     def get_permissions(self):
#         permission_classes = [IsAuthenticated]
#         if self.action in ['create', 'metadata']:
#             permission_classes = [AllowAny]
#
#         return [permission() for permission in permission_classes]
#
#     def get_queryset(self):
#         queryset = User.objects.filter(is_active=True, id=self.request.user.id)
#         # Filter superusers from listings
#         if not self.request.user.is_superuser:
#             queryset = queryset.exclude(is_superuser=True)
#         return queryset
#
#     def get_serializer_class(self):
#         serializer_class = UserSerializer
#         if self.action not in ['list', 'retrieve']:
#             serializer_class = TokenUserSerializer
#         return serializer_class
#
#     def perform_create(self, serializer):
#         instance = serializer.save()
#         run_async(notification_service.admin_new_user, instance)
#
#     # Custom DELETE call to deactivate instead of delete db object (attribute 'is_active' is required)
#     def perform_destroy(self, instance):
#         instance.is_active = False
#         instance.save()
