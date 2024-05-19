from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    pattern_phone = r'^\+?[\d\s\-\(\)]+$'

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not re.match(pattern_phone, phone):
        raise ValidationError("El formato del teléfono es inválido.")

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()

 ##---------medicine----------   
def validate_medicine(data):
    errors = {}

    name = data.get("name", "")
    description = data.get("description", "")
    dose = data.get("dose", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if description == "":
        errors["description"] = "Por favor ingrese una descripción"
    if dose == "":
        errors["dose"] = "Por favor ingrese una dosis"
    else:
        try:
            int_dose = int(dose)
            if int_dose < 1 or int_dose > 10:
                errors["dose"] = "La dosis debe estar en un rango de 1 a 10"
        except ValueError:
            errors["dose"] = "La dosis debe ser un número entero válido"
    return errors

class Medicine(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    dose = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )

        return True, None
    def update_medicine(self, medicine_data):
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save()
    

 ##---------pets----------   
def validate_pet(data):
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"

    if birthday == "":
        errors["birthday"] = "Por favor ingrese una fecha de nacimiento"
    return errors
    
    
class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50)
    birthday = models.DateField()
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True, blank=True)
    medicines = models.ManyToManyField(Medicine)
    vets = models.ManyToManyField("Vet", blank=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
        )

        return True, None
    
    def update_pet(self, pet_data):
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()

##---------products----------   
def validate_product(data):
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "") 
    price = data.get("price", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    
    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

    if price == "": 
        errors["price"] = "Por favor ingrese un precio"
    else:
        try:
            float_price = float(price)
            if float_price <= 0:
                errors["price"] = "El precio debe ser mayor que cero"
        except ValueError:
            errors["price"] = "El precio debe ser un número válido"
    return errors


class Product(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    price = models.FloatField()
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name
    
    @classmethod
    def save_product(cls, product_data):
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
        )

        return True, None
    
    def update_product(self, product_data):
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        self.save()
        
##---------providers----------   

def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
        )

        return True, None

    def update_provider(self, provider_data):
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email

        self.save()

 ##---------vets----------   
def validate_vet(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    specialty = data.get("specialty", "")

    pattern_phone = r'^\+?[\d\s\-\(\)]+$'

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not re.match(pattern_phone, phone):
        errors["phone"] = "El formato del teléfono es inválido."

    if specialty == "":
        errors["specialty"] = "Por favor seleccione una especialidad"

    return errors

class Vet(models.Model):
    class Specialties(models.TextChoices):
        MEDICINA_INTERNA = 'Medicina interna', 'Medicina interna'
        CIRUGIA = 'Cirugía', 'Cirugía'
        DERMATOLOGIA = 'Dermatología', 'Dermatología'
        OFTALMOLOGIA = 'Oftalmología', 'Oftalmología'
        ODONTOLOGIA = 'Odontología', 'Odontología'
        ONCOLOGIA = 'Oncología', 'Oncología'
        ORTOPEDIA = 'Ortopedia', 'Ortopedia'
        CARDIOLOGIA = 'Cardiología', 'Cardiología'
        NEUROLOGIA = 'Neurología', 'Neurología'
        REPRODUCCION = 'Reproducción', 'Reproducción'

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    specialty = models.CharField(
        max_length=16,
        choices=Specialties.choices,
    )

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
        errors = validate_vet(vet_data)

        if errors:
            return False, errors

        cls.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
            specialty=vet_data.get("specialty", cls.Specialties.MEDICINA_INTERNA)
        )

        return True, None

    def update_vet(self, vet_data):
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
        self.specialty = vet_data.get("specialty", self.specialty)
        self.save()