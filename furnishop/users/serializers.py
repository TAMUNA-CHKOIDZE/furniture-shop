from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    # password-ის ჩაწერა შესაძლებელია, მაგრამ JSON-ის output-ში არ გამოჩნდება. მხოლოდ read არის შესაძლებელი.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'birth_date', 'password']

    def create(self, validated_data):
        # პაროლის ამოღება dict-დან, რათა პირდაპირ არ მოხდეს შენახვა
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        # პაროლი დაიჰეშბა, არ შიინახება plaintext სახით.
        user.set_password(password)
        # ინახავს მონაცემებს DB-ში.
        user.save()
        return user


# authenticate() Django-ს ფუნქცია იკვლევს, არსებობს თუ არა მომხმარებელი მოცემული email და password-ით.
# თუ user არსებობს და აქტიურია (is_active=True), ვაბრუნებთ data-ს, რომელსაც დამატებული აქვს user.
# თუ credentials არასწორია, აგდებს ValidationError-ს.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")


# ProfileSerializer გამოიყენება პროფილის ნახვისთვის, response JSON-ში გვაძლევს მომხმარებლის მონაცემებს.
# გამორიცხავს პაროლს (არა write-only, არა read-write).
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'address', 'birth_date']


# Serializer ორ ველს იღებს: ძველი პაროლი და ახალი პაროლი. ორივე write-onlyა, response-ში ვერ გამოჩნდება.
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    # validate_old_password — ვერიფიკაციას უკეთებს ძველ პაროლს.
    # self.context['request'].user არის მომხამრებელი, რომელიც ამჟამად ავტორიზებულია
    # user.check_password(value) — ამოწმებს, ემთხვევა თუ არა ძველი პაროლი database-ში დაჰეშილს
    # თუ არ ემთხვევა გაისვრის ValidationError-ს
    # წარმატების შემთხვევაში, დაბრუნდება ძველი პაროლი (შემდეგ ეტაპზე ახალი პაროლის შესაცვლელად გამოიყენება).
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
