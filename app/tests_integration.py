from decimal import Decimal
from django.shortcuts import reverse
from django.test import TestCase

from app.models import Client, Pet, Provider


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "54221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email válido")

    def test_validate_email_ends_with_vetsoft_com(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Rosario Central",
                "phone": "544444444",
                "address": "13 y 44",
                "email": "rositac@gmail.com",
            },
        )

        self.assertContains(response, "El email debe terminar con @vetsoft.com")    

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastian Veron",
            phone="54221555232",
            email="brujita75@vetsoft.com",
            address="13 y 44",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
                "phone": client.phone,
                "email": client.email,
                "address": client.address,
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)

        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.email, client.email)
        self.assertEqual(editedClient.address, client.address)
        
    def test_validation_valid_phone(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Perez",
                "phone": "",  # teléfono inválido
                "email": "hola@vetsoft.com",
                "address": "Calle 123",
            },
        )
        self.assertContains(response, "Por favor ingrese un teléfono")
    
    def test_validation_invalid_phone_number(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "111111111",
                "email": "brujita75@vetsoft.com",
                "address": "13 y 44",     
            },
        )
        self.assertContains(response, "El número de teléfono debe comenzar con el prefijo 54 para Argentina")
    
    def test_validation_invalid_format_phone_number(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54aaa1111111",
                "email": "brujita75@vetsoft.com",
                "address": "13 y 44",     
            },
        )
        self.assertContains(response, "El número de teléfono debe comenzar con el prefijo 54 para Argentina y solo puede contener números")
    
    def test_validation_invalid_name(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan123",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
                "address": "13 y 44",
            },
        )
        self.assertContains(response, "El nombre solo puede contener letras y espacios")


class ProvidersTest(TestCase):

    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_repo_display_all_providers(self):
        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("providers_form"))
        self.assertTemplateUsed(response, "providers/form.html")

    def test_can_create_provider(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "Proveedor de Prueba",
                "email": "proveedor@ejemplo.com",
                "address": "Calle Falsa 123",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Proveedor de Prueba")
        self.assertEqual(providers[0].email, "proveedor@ejemplo.com")
        self.assertEqual(providers[0].address, "Calle Falsa 123")

        self.assertRedirects(response, reverse("providers_repo"))

    def test_validation_errors_create_provider(self):
        response = self.client.post(
            reverse("providers_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_provider_doesnt_exists(self):
        response = self.client.get(reverse("providers_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "Juan Perez",
                "email": "invalid-email",  # email inválido
                "address": "Calle 123",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")


    def test_edit_provider_with_valid_data(self):
        provider = Provider.objects.create(
            name="Proveedor Original",
            address="Dirección Original",
            email="original@ejemplo.com",
        )

        response = self.client.post(
            reverse("providers_form"),
            data={
                "id": provider.id,
                "name": "Proveedor Actualizado",
                "address": provider.address,
                "email": provider.email,
            },
        )

        # Redirección después del POST
        self.assertEqual(response.status_code, 302)

        edited_provider = Provider.objects.get(pk=provider.id)
        self.assertEqual(edited_provider.name, "Proveedor Actualizado")
        self.assertEqual(edited_provider.email, provider.email)
        self.assertEqual(edited_provider.address, provider.address)

# TEST DE PET
class PetsTest(TestCase):
    # verifica que se una la template correcta
    def test_form_use_form_template(self):
        response = self.client.get(reverse("pets_form"))
        self.assertTemplateUsed(response, "pets/form.html")
        
    # creacion de mascota
    def test_can_create_pet(self):
            response = self.client.post(
                reverse("pets_form"),
                data={
                    "name": "Roma",
                    "breed": "Labrador",
                    "birthday": "2021-10-10",
                    "weight": Decimal("10.158"),
                },
            )
            pets = Pet.objects.all()

            self.assertEqual(len(pets), 1)
            # verificamos coincidencias
            self.assertEqual(pets[0].name, "Roma")
            self.assertEqual(pets[0].breed, "Labrador")
            self.assertEqual(pets[0].birthday.strftime('%Y-%m-%d'), "2021-10-10") # formateo la fecha de cumple para comparar
            self.assertEqual(pets[0].weight,  Decimal("10.158"))

            # verifico si existe en la base de datos
            self.assertTrue(Pet.objects.filter(name="Roma").exists())
            # verifico si redirige a la url correcta
            self.assertRedirects(response, reverse("pets_repo"))



    # validar de que el peso no puede ser negativo
    def test_validation_errors_weight_less_than_zero(self):
        response = self.client.post(
                reverse("pets_form"),
                data={
                    "name": "Roma",
                    "breed": "Labrador",
                    "birthday": "2021-10-10",
                    "weight": Decimal("-10.000"),
                },
            )
        # Verifico si el peso es negativo y muestra un mensaje de error
        self.assertContains(response, "El peso debe ser un número mayor a cero")
    
    def test_validation_invalid_birthday(self):
        
        response = self.client.post(
            reverse("pets_form"),
            data = {
            "name": "Pepe",
            "breed": "Labrador",
            "birthday": "2026-01-01",
            "weight": Decimal("10.252"),
        },
        )

        self.assertContains(response, "La fecha de nacimiento no puede ser mayor o igual a la fecha actual")
        
     # validar de que la raza no puede ser null
    def test_validation_errors_pet_breedless(self):
        response = self.client.post(
                reverse("pets_form"),
                data={
                    "name": "Posta",
                    "breed": "",
                    "birthday": "2021-10-10",
                    "weight": Decimal("180.050")
                },
            )
        # Verifico si no tiene raza y muestra un mensaje de error
        self.assertContains(response, "Por favor seleccione una raza")

class ProductsTest(TestCase):
    def test_validation_invalid_price(self):
        # client es un objeto que proporciona Django para simular solicitudes HTTP en tus tests.
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Paracetamol",
                "description": "Medicamento para el dolor",
                "price": 0,
            },
        )

        self.assertContains(response, "El precio debe ser mayor que cero")
        
class MedicinesTest(TestCase):
    def test_validation_invalid_dose(self):
        # client es un objeto que proporciona Django para simular solicitudes HTTP en tus tests.
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Diclofenac",
                "description": "Calma el dolor muscular",
                "dose": 0,
            },
        )

        self.assertContains(response, "La dosis debe estar en un rango de 1 a 10")

class VetsTest(TestCase):
    def test_validation_invalid_phone(self):
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Perez",
                "phone": "",  # teléfono inválido
                "email": "hola@vetsoft.com",
            },
        )

        self.assertContains(response, "Por favor ingrese un teléfono")

    def test_validation_invalid_phone_number(self):
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "111111111",
                "email": "brujita75@vetsoft.com",  
            },
        )
        self.assertContains(response, "El número de teléfono debe comenzar con el prefijo 54 para Argentina")

