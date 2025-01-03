# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
# from rest_framework import permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth.models import User
# from v1.utils import constant
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes


# class PasswordUpdateView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     @staticmethod
#     def post(request):
#         """
#         Update password for authenticated user
#         """

#         password = request.data.get('password')

#         try:
#             validate_password(password)
#             request.user.set_password(password)
#             request.user.save()
#             return Response({constant.SUCCESS: 'Password has been updated'})
#         except KeyError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except TypeError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except ValidationError as e:
#             return Response({constant.ERROR: e}, status=status.HTTP_400_BAD_REQUEST)

# class PasswordResetView(APIView):
#     """
#     Password Reset Request View
#     """
#     @staticmethod
#     def post(request):
#         """
#         Sends a password reset email to the user
#         """
#         email = request.data.get("email")
#         if not email:
#             return Response({constant.ERROR: "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             reset_link = f"{request.build_absolute_uri('/update-password/')}?uid={uid}&token={token}"
            
#             # Sending email (you should configure EMAIL settings in settings.py)
#             send_mail(
#                 subject="Password Reset Request",
#                 message=f"Click the link below to reset your password:\n\n{reset_link}",
#                 from_email="noreply@yourdomain.com",
#                 recipient_list=[email],
#                 fail_silently=False,
#             )
#             return Response({constant.SUCCESS: "Password reset email sent successfully"}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({constant.ERROR: "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({constant.ERROR: str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
