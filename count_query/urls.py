from django.urls import path
from .views import CustomLoginView, CustomLogoutView, query_builder, CustomSignupView, UploadDataView, active_users
from rest_framework.routers import DefaultRouter
from .views import RecordCountViewSet

router = DefaultRouter()
router.register(r'record-count', RecordCountViewSet, basename='record-count')

urlpatterns = [
    path('query_builder/', query_builder, name='query_builder'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('upload_data/', UploadDataView.as_view(), name='upload_data'),
    path('active-users/', active_users, name='active_users'),

]

urlpatterns += router.urls