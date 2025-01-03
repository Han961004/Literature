from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models.profile import Profile
from accounts.serializers.profile import *
from accounts.serializers.user import *


class ProfileView(APIView):
    
    @staticmethod
    def get(request):
        '''
        List profile
        '''
        profiles = Profile.objects.all()
        return Response(ProfileSerializer(profiles, many=True).data)
    
class ProfileDetailView(APIView):
    
    @staticmethod
    def get(request, profile_id):
        '''
        retrieve a specific profile by id
        '''
        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(ProfileSerializer(profile).data)
    
    @staticmethod
    def put(request, profile_id):
        '''
        update the entire profile of authenticated user
        '''
        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ProfileUpdateSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response(UserLoginSerializer(profile.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)