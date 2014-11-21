from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.routers import DefaultRouter
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
    serializer = ValidateSerialiser(data=request.DATA)
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
    created_by = serializers.IntegerField(required=False)
    updated_by = serializers.IntegerField(required=False)
    site = serializers.IntegerField(required=False)

    class Meta:
        model = Rule

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(RuleSerializer, self).get_validation_exclusions()
        return exclusions + ['created_by', 'updated_by', 'site']

    def restore_object(self, attrs, instance=None):
        instance = super().restore_object(attrs, instance)
        request = self.context.get('request', None)
        setattr(instance, 'updated_by', request.user)
        if request.method == 'POST':
            setattr(instance, 'created_by', request.user)
        return instance


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

rules_router = DefaultRouter()
rules_router.register(r'rules', RuleViewSet)
