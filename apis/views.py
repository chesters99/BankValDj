from rest_framework import serializers, status
from rest_framework.exceptions import ParseError
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


class APIOptions(APIView):
    """ /apis/validate/?bank_account=SSSSSS-AAAAAAAA validates a UK Bank Account where S is Sort Code and A is account number
        /apis/rules/X/ allows rules with key X to be retrieved, added, updated and deleted
        /apis/rulelist/?start_sort=XXXXXX&end_sort=YYYYYY returns a list of all rules between specified sort codes """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AllowAny,]


class Validate(APIView):
    """ /apis/validate/?bank_account=SSSSSS-AAAAAAAA validates a UK Bank Account where S is Sort Code and A is account number """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AllowAny,]

    def get(self, request):
        try:
            bank_account_split = self.request.query_params.get('bank_account', None).split('-')
        except AttributeError:
            return Response('bank account not specified- use /apis/validate?bank_account=XXXXXX-YYYYYYYY', status=status.HTTP_400_BAD_REQUEST)
        account = {'sort_code': bank_account_split[0], 'account_number': bank_account_split[1]}
        serializer = ValidateSerialiser(data=account)
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
    """/apis/rules/X/ allows rules with key X to be retrieved, added, updated and deleted"""
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly,]


class RuleList(ListAPIView):
    """/apis/rulelist/?start_sort=XXXXXX&end_sort=YYYYYY returns a list of all rules between specified sort codes """
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
                raise ParseError('Call API as /apis/rulelist/?start_sort=XXXXXX&end_sort=YYYYYY')
