from datetime import date

from django.forms import ValidationError
from django.test import TestCase

from app.models import Client, Provider, Vet, validate_medicine, validate_pet, validate_product, validate_client, validate_vet

class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
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

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({"phone": "54221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555232")
    
    def test_validate_phone_number_in_phone_field(self):
        client_data = {
            "name": "Juan Sebastian Veron",
            "phone": "",
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        }
        
        errors = validate_client(client_data)
        self.assertIn("phone", errors)
        self.assertEqual(errors["phone"], "Por favor ingrese un teléfono")

        

class ProviderModelTest(TestCase):
    
    def test_create_provider_with_address(self):
        # Datos de prueba
        provider_data = {
            "name": "Pedro Perez",
            "email": "PedroP012@hotmail.com",
            "address": "Calle 142 723",
        }

        # Crear proveedor
        success, errors = Provider.save_provider(provider_data)

        # Verificar que no hubo errores y que la creación fue exitosa
        self.assertTrue(success)
        self.assertIsNone(errors)

        # Recuperar el proveedor de la base de datos
        provider = Provider.objects.get(email="PedroP012@hotmail.com")

        # Verificar que los datos se guardaron correctamente
        self.assertEqual(provider.name, "Pedro Perez")
        self.assertEqual(provider.email, "PedroP012@hotmail.com")
        self.assertEqual(provider.address, "Calle 142 723")

    def test_update_provider_with_address(self):
        # Datos de prueba iniciales
        provider = Provider.objects.create(
            name="Proveedor Original",
            email="original@ejemplo.com",
            address="Dirección Original",
        )

        # Datos de prueba para actualización
        update_data = {
            "name": "Proveedor Actualizado",
            "email": "actualizado@ejemplo.com",
            "address": "Dirección Actualizada",
        }

        # Actualizar proveedor
        provider.update_provider(update_data)

        # Verificar que los datos se actualizaron correctamente
        self.assertEqual(provider.name, "Proveedor Actualizado")
        self.assertEqual(provider.email, "actualizado@ejemplo.com")
        self.assertEqual(provider.address, "Dirección Actualizada")

# TEST DE PET
class PetModelTest(TestCase):
    def test_weight_greater_than_zero(self):
          # Crear una instancia de Mascota con un peso mayor a cero
        mascota_data = {
            "name": "Fido",
            "breed": 2,
            "birthday": "2020-01-01",
            "weight": 10,
        }
        errors = validate_pet(mascota_data)
        # verifica que no hay error en el peso
        self.assertNotIn("weight", errors, "No debe haber un error de peso cuando es mayor a cero")



    def weight_test_less_than_zero(self):
        # Crear una instancia de Mascota con un peso menor a cero
        mascota_data: dict ={
            "name": "Roma",
            "breed": 1,
            "birthday": "2021-01-01",
            "weight": -2,
        }
       
        errors= validate_pet(mascota_data)
        #  verifica que la respuesta del error sea correcta
        self.assertEqual(errors["weight"], "El peso debe ser un número mayor a cero")
        
    def test_birthday_today_date(self):

        today = date.today().isoformat()

        # Creo un setup
        pet_data = {
            "name": "Pepe",
            "breed": "Labrador",
            "birthday": today,
            "weight": 10,
            "client": 1,
        }

        errors = validate_pet(pet_data)

        # Compruebo que hay error en el campo de birthday
        self.assertIn("birthday", errors)
        self.assertEqual(errors["birthday"], "La fecha de nacimiento no puede ser mayor o igual a la fecha actual")

    def test_birthday_past_date(self):

        #Creo el setup
        pet_data = {
            "name": "Pepe",
            "breed": "Labrador",
            "birthday": "2020-01-01",
            "weight": 10,
            "client": 1,
        }

        errors = validate_pet(pet_data)

        #Compruebo que no hay error en el campo de birthday
        self.assertNotIn("birthday", errors, "La fecha ingresada es correcta, no debe haber error")

class MedicineModelTest(TestCase):
    def test_medicine_dose_validation_in_range_1_to_10(self):
        # Crear un diccionario con los datos del medicamento
        medicine_data = {
            "name": "Test Medicine",
            "description": "Test Description",
            "dose": -10, 
        }

        # Llamar a la función de validación del medicamento
        errors = validate_medicine(medicine_data)

        # Comprobar que hay un error de validación en el campo 'dose'
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "La dosis debe estar en un rango de 1 a 10")

        # Probar con otra dosis inválida, superando el rango
        medicine_data["dose"] = 15
        errors = validate_medicine(medicine_data)

        # Comprobar que hay un error de validación en el campo 'dose'
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "La dosis debe estar en un rango de 1 a 10")

        # Probar con otra dosis válida, dentro el rango
        medicine_data["dose"] = 10
        errors = validate_medicine(medicine_data)

        # Comprobar que no hay errores de validación
        self.assertNotIn("dose", errors)

        # Probar con otra dosis válida, dentro el rango
        medicine_data["dose"] = 5
        errors = validate_medicine(medicine_data)

        # Comprobar que no hay errores de validación
        self.assertNotIn("dose", errors)

class ProductModelTest(TestCase):
    def test_price_greater_than_zero(self):
        # Crear un diccionario con los datos del producto
        product_data = {
            "name": "Test Product",
            "type": "Test Type",
            "price": -10, 
        }

        # Llamar a la función de validación del producto
        errors = validate_product(product_data)

        # Comprobar que hay un error de validación en el campo 'price'
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "El precio debe ser mayor que cero")

        # Probar con un precio válido
        product_data["price"] = 0
        errors = validate_product(product_data)

        # Comprobar que hay un error de validación en el campo 'price'
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "El precio debe ser mayor que cero")

class VetModelTest(TestCase):
    def test_can_create_and_get_vet(self):
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
            }
        )
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        self.assertEqual(vets[0].name, "Juan Sebastian Veron")
        self.assertEqual(vets[0].phone, 54221555232)
        self.assertEqual(vets[0].email, "brujita75@vetsoft.com")

    def test_can_update_vet(self):
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.phone, 54221555232)

        vet.update_vet({"phone": "54221555233"})

        vet_updated = Vet.objects.get(pk=1)

        self.assertEqual(vet_updated.phone, 54221555233)
    
    def test_update_vet_with_error(self):
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.phone, 54221555232)

        vet.update_vet({"phone": ""})

        vet_updated = Vet.objects.get(pk=1)

        self.assertEqual(vet_updated.phone, 54221555232)
    
    def test_validate_phone_number_in_phone_field(self):
        vet_data = {
            "name": "Juan Sebastian Veron",
            "phone": "Hola, no soy un teléfono válido",
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        }
        
        with self.assertRaises(ValidationError):
            validate_vet(vet_data)
        

