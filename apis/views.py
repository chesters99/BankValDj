from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from accounts.utils.BankValidator import Validator
from rules.models import Rule


class ValidateSerialiser(serializers.Serializer):
    sort_code = serializers.CharField(max_length=6)
    account_number = serializers.CharField(max_length=11)

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule


class Validate(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = ValidateSerialiser(data=request.data)
        if serializer.is_valid():
            bv = Validator()
            if bv.validate(sort_code=serializer.validated_data['sort_code'],
                           account_number=serializer.validated_data['account_number']):
                serializer.validated_data['message']= 'Valid Account'
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                serializer.validated_data['message']= bv.message
                return Response(serializer.validated_data, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RuleViewSet(ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly,]


class RuleList(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = Rule
    serializer_class = RuleSerializer

    def get_queryset(self):
        pk = self.request.query_params.get('pk', None)
        if pk:
            return Rule.objects.filter(pk=pk)
        else:
            start_sort = self.request.query_params.get('start_sort', None)
            end_sort = self.request.query_params.get('end_sort', None)
            if start_sort is not None and end_sort is not None:
                return Rule.objects.filter(start_sort__gt=start_sort, end_sort__lt=end_sort)
            else:
                return Rule.objects.none()
