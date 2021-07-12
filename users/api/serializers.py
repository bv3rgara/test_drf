# from django.db.models import fields
from decimal import MAX_EMAX
from rest_framework import serializers
from users.models import User


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

    # solo para listar sobreescribimos el metodo
    def to_representation(self, instance):
        # super().to_representation(instance)
        dic = {
            # 'id': instance.id, # si le enviase el all sin el values
            'id': instance['id'], # se envia en la consulta un values
            'nombre_usuario': instance['username'], # se envia en la consulta un values
            'nombre': instance['name'], # se envia en la consulta un values
            'password': instance['password'] # se envia en la consulta un values
        }
        return dic


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # llamo al contructor para asegurarme de act todos los atributos
        user_up = super().update(instance, validated_data)
        user_up.set_password(validated_data["password"])
        user_up.save()
        return user_up


class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=80)
    email = serializers.EmailField()

    def validate_name(self, value):
        # puedo acceder en cada validate_fiel a algun elemento del dic enviado en context
        #print(self.context["email"])
        if value == "":
            raise serializers.ValidationError("Error, tiene que tener algun nombre")
        return value

    def validate_email(self, value):
        return value
    
    def validate(self, data):
        if data["name"] in data["email"]:
            raise serializers.ValidationError("Error, el email no puede contener el nombre")
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

    # para realizar validaciones sobre los datos pero no se quiere guardar info en la BD
    # def save(self):
    #    print(self)