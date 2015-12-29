from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from accounts.utils.BankValidator import Validator
from rules.models import Rule

###############################  BUG IN DJANGO REST FRAMEWORK #########################################
# kludge fix needed - change line 841 in rest_framework/serializers.py to kwargs['read_only'] = False #
#######################################################################################################

# The APIs below can be driven by the following curls (also from test scripts)
# 1) to create a rule
# curl -X POST http://localhost:8000/apis/templates/ -d "start_sort=000123&mod_rule=DBLAL&end_sort=012345&
# weight0=2&weight1=2&weight2=2&weight3=1&weight4=1&weight5=1&weight6=1&weight7=1&weight8=1&weight9=1&weight10=1&
# weight11=1&weight12=1&weight13=1&weight14=1" -H 'Authorization: Token 5ca74d0436ca08770415a463f6d428ac307167ed'
# 2) to get all templates
# curl -X GET http://localhost:8000/apis/templates/
# 3) to get a rule
# curl -X GET http://localhost:8000/apis/templates/1000/
# 4) to update a rule
# curl -X PUT http://localhost:8000/apis/templates/1000/ -d "start_sort=000123&mod_rule=DBLAL&end_sort=012345&
# weight0=2&weight1=2&weight2=2&weight3=1&weight4=1&weight5=1&weight6=1&weight7=1&weight8=1&weight9=1&weight10=1&
# weight11=1&weight12=1&weight13=1&weight14=1" -H 'Authorization: Token 5ca74d0436ca08770415a463f6d428ac307167ed'
# 5) to delete a rule (ie change status to active = no)
# curl -X DELETE http://localhost:8000/apis/templates/1000/ -H
# 'Authorization: Token 5ca74d0436ca08770415a463f6d428ac307167ed'
#


class ValidateSerialiser(serializers.Serializer):
    sort_code = serializers.CharField(max_length=6)
    account_number = serializers.CharField(max_length=11)

@api_view(['POST'])
def validate(request):  # pseudo-RESTful API
    serializer = ValidateSerialiser(data=request.data)
    if serializer.is_valid():
        bv = Validator()
        if bv.validate(sort_code=serializer.data['sort_code'],
                       account_number=serializer.data['account_number']):
            serializer.data['message'] = 'Valid Account'
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer.data['message'] = bv.message
            return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule


class RuleView(ListAPIView):
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
                return Rule.objects.filter(start_sort='XXXXXX')


class RuleChange(RetrieveUpdateDestroyAPIView):
    model = Rule
    serializer_class = RuleSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Rule.objects.filter(pk=pk)
