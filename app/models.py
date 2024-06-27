#Importaciones de Python

import re
from datetime import date
from decimal import Decimal

#Importaciones de Django
from django.db import models


##---------clients----------   
def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    pattern_phone = r'^54[\d\s\-\(\)]+$'
    pattern_email = r'^[a-zA-Z0-9_.+-]+@vetsoft.com$'
    pattern_name = r'^[a-zA-Z\s]+$' #solo letras y espacios

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    elif not re.match(pattern_name, name):
        errors["name"] = "El nombre solo puede contener letras y espacios"
    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not re.match(pattern_phone, phone):
        errors["phone"] = "El número de teléfono debe comenzar con el prefijo 54 para Argentina."
    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email válido"
    elif not re.match(pattern_email, email):
        errors["email"] =("El email debe terminar con @vetsoft.com")
    

    return errors

class Client(models.Model):
    """Esta clase representa un cliente de la veterinaria
    Contiene los siguientes atributos:
    - name: nombre del cliente
    - phone: teléfono del cliente
    - email: email del cliente
    - address: dirección del cliente
    Contiene los siguientes métodos:
    - __str__: retorna el nombre del cliente
    - save_client: guarda un cliente en la base de datos
    - update_client: actualiza los datos de un cliente en la base de datos
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """"save_client: Método para guardar un cliente en la base de datos"""
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
        """"update_client: Método para actualizar un cliente en la base de datos"""
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()

 ##---------medicine----------   


##---------medicines----------   
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
    """ Esta clase representa un medicamento de la veterinaria
    Contiene los siguientes atributos:
    - name: nombre del medicamento
    - description: descripción del medicamento
    - dose: dosis del medicamento
    Contiene los siguientes métodos:
    - __str__: retorna el nombre del medicamento
    - save_medicine: guarda un medicamento en la base de datos
    - update_medicine: actualiza los datos de un medicamento en la base de datos
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    dose = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
        """def save_medicine: Método para guardar un medicamento en la base de datos"""
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
        """def update_medicine: Método para actualizar un medicamento en la base de datos"""
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save()
    

 ##---------pets----------   

##---------pets----------   
def validate_pet(data):
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")
    weight = data.get("weight", None)

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor seleccione una raza"

    if birthday == "":
        errors["birthday"] = "Por favor ingrese una fecha de nacimiento"
    else:
        try:
            birth = date.fromisoformat(birthday)
            if birth >= date.today():
                errors["birthday"] = "La fecha de nacimiento no puede ser mayor o igual a la fecha actual"
        except ValueError:
            errors["birthday"] = "Formato de fecha inválido. Por favor ingrese la fecha en el formato correcto (YYYY-MM-DD)"


    if weight == "": 
        errors["weight"] = "Por favor ingrese un peso"
    else:
        try:
            decimal_weight = Decimal(weight)
            if decimal_weight <= 0:
                errors["weight"] = "El peso debe ser un número mayor a cero"
        except ValueError:
            errors["weight"] = "El peso debe ser un número válido"

    return errors

##---------clase enumerativa de raza----------   
class Breed(models.TextChoices):
    """ Esta clase enumarativa representa las razas de perro
    y gato de una mascota
    """
     # raza de perros
    LABRADOR = 'labrador', 'Labrador'
    BEAGLE = 'beagle', 'Beagle'
    BULLDOG = 'bulldog', 'Bulldog'
    CHIHUAHUA = 'chihuahua', 'Chihuahua'
    DOGO_ARGENTINO = 'dogo_argentino', 'Dogo Argentino'
    PUG = 'pug', 'Pug'
    POODLE = 'poodle', 'Poodle'
    ROTTWEILER = 'rottweiler', 'Rottweiler'
    
    # razas de gatos
    SIAMESE = 'siamese', 'Siamés'
    PERSIAN = 'persian', 'Persa'
    SPHYNX = 'sphynx', 'Sphynx'
    BENGAL = 'bengal', 'Bengalí'

class Pet(models.Model):
    """ Esta clase representa una mascota de la veterinaria
    Contiene los siguientes atributos:
    - name: nombre de la mascota
    - breed: raza de la mascota
    - birthday: fecha de nacimiento de la mascota
    - weight: peso de la mascota
    - client: dueño de la mascota
    - medicines: medicamentos que toma la mascota
    - vets: veterinarios que atienden a la mascota
    Contiene los siguientes métodos:
    - __str__: retorna el nombre de la mascota
    - save_pet: guarda una mascota en la base de datos
    - update_pet: actualiza los datos de una mascota en la base de datos
    """
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50, choices=Breed.choices)
    birthday = models.DateField()
    weight = models.DecimalField(max_digits=8, decimal_places=3)  
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True, blank=True)
    medicines = models.ManyToManyField(Medicine)
    vets = models.ManyToManyField("Vet", blank=True)

    def __str__(self):
        """def __str__: Método para retornar el nombre de la mascota"""
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
        """def save_pet: Método para guardar una mascota en la base de datos"""
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
            weight=pet_data.get("weight"),
        )

        return True, None
    
    def update_pet(self, pet_data):
        """def update_pet: Método para actualizar una mascota en la base de datos"""
        # Validar los datos
        errors = validate_pet(pet_data)
        
        if len(errors.keys()) > 0:
            return False, errors
        
        # Actualizar los datos de la mascota
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday
        self.weight = pet_data.get("weight", "") or self.weight
        self.save()

        return True, None



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
    """ Esta clase representa un producto de la veterinaria
    Contiene los siguientes atributos:
    - name: nombre del producto
    - type: tipo del producto
    - price: precio del producto
    - provider: proveedor del producto
    Contiene los siguientes métodos:
    - __str__: retorna el nombre del producto
    - save_product: guarda un producto en la base de datos
    - update_product: actualiza los datos de un producto en la base de datos
    """
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    price = models.FloatField()
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """def __str__: Método para retornar el nombre del producto"""
        return self.name
    
    @classmethod
    def save_product(cls, product_data):
        """def save_product: Método para guardar un producto en la base de datos"""
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
        """def update_product: Método para actualizar un producto en la base de datos"""
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price
        self.save()

        return True, None
        
##---------providers----------   

def validate_provider(data):
    """validate_provider: Método para validar los datos de un proveedor"""
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    address = data.get("address", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if address == "":
        errors["address"] = "Por favor ingrese una dirección"

    return errors

class Provider(models.Model):
    """ Esta clase representa un proveedor de la veterinaria
    Contiene los siguientes atributos:
    - name: nombre del proveedor
    - email: email del proveedor
    - address: dirección del proveedor
    Contiene los siguientes métodos:
    - __str__: retorna el nombre del proveedor
    - save_provider: guarda un proveedor en la base de datos
    - update_provider: actualiza los datos de un proveedor en la base de datos
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        """save_provider: Método para guardar un proveedor en la base de datos"""
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
            address=provider_data.get("address"),
        )

        return True, None

    def update_provider(self, provider_data):
        """update_provider: Método para actualizar un proveedor en la base de datos"""
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address", "") or self.address

        self.save()
        return True, None


 ##---------vets----------   

##---------vets----------   
def validate_vet(data):
    """validate_vet: Método para validar los datos de un veterinario"""
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    pattern_phone = r'^54[\d\s\-\(\)]+$'

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"
    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"        
    elif not re.match(pattern_phone, phone):
        errors["phone"] = "El número de teléfono debe comenzar con el prefijo 54 para Argentina."


    return errors

class Vet(models.Model):
    """ Esta clase representa un veterinario de la veterinaria
    Contiene los siguientes atributos:
    - name: nombre del veterinario
    - email: email del veterinario
    - phone: teléfono del veterinario
    Contiene los siguientes métodos:
    - __str__: retorna el nombre del veterinario
    - save_vet: guarda un veterinario en la base de datos
    - update_vet: actualiza los datos de un veterinario en la base de datos
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
        """def save_vet: Método para guardar un veterinario en la base"""
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
        )

        return True, None

    def update_vet(self, vet_data):
        """def update_vet: Método para actualizar un veterinario en la base"""
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone

        self.save()



    