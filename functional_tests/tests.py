from decimal import Decimal
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import Browser, expect, sync_playwright

from app.models import Client, Pet, Provider

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo),
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()
        

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="54221232555",
            email="goleador@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente",
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()

class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastian Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastian Veron")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email válido"),
        ).to_be_visible()

    def test_should_view_errors_if_name_less_than_three_words(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Ja")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El nombre debe tener al menos 3 caracteres")).to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email válido"),
        ).to_be_visible()

    def test_email_must_end_with_vetsoft_com(self):
        
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Nuria Molina")
        # self.page.get_by_label("Teléfono").fill("1545889999")
        self.page.get_by_label("Email").fill("MolinosNuria@invalido.com")
        self.page.get_by_label("Dirección").fill("7 856")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email válido")).not_to_be_visible()
        
        expect(self.page.get_by_text("El email debe terminar con @vetsoft.com")).to_be_visible()
       

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("54221232555")
        self.page.get_by_label("Email").fill("goleador@vetsoft.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("54221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )
        
    def test_should_view_errors_if_phone_does_not_start_with_54(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastian Veron")
        self.page.get_by_label("Teléfono").fill("123456789")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El número de teléfono debe comenzar con el prefijo 54 para Argentina")).to_be_visible()

    def test_should_view_errors_if_phone_has_letters(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastian Veron")
        self.page.get_by_label("Teléfono").fill("54221634soyunerror")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El número de teléfono debe comenzar con el prefijo 54 para Argentina y solo puede contener números")).to_be_visible()


#  TEST DE PETS
class PetCreateWeightgreaterThanZero(PlaywrightTestCase):

     # test para verificar que el formulario sea invalido y advertencia del precio menor a cero   
    def test_should_view_errors_if_form_is_invalid_with_weight_less_than_zero(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

       
        expect(self.page.get_by_role("form")).to_be_visible()

        #formulario vacio
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor seleccione una raza")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un peso")).to_be_visible()
        
        # peso menor a cero
        self.page.get_by_label("Nombre").fill("Roma")
        self.page.select_option("#breed", label="Dogo Argentino")  # Usa select_option para seleccionar la raza
        self.page.get_by_label("Fecha de Cumpleaños").fill("2022-11-30")
        self.page.get_by_label("Peso").fill("-200.000")
        
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("El peso debe ser un número mayor a cero"),
        ).to_be_visible()

class PetCreateValidateTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_pet(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Firulais")
        self.page.select_option("#breed", label="Labrador")  # Usa select_option para seleccionar la raza
        self.page.get_by_label("Fecha de Cumpleaños").fill("2022-01-01")
        self.page.get_by_label("Peso").fill("130.065")
        

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Firulais")).to_be_visible()
        expect(self.page.get_by_text("Labrador")).to_be_visible()
        expect(self.page.get_by_text("Jan. 1, 2022")).to_be_visible()
        expect(self.page.get_by_text("130.065")).to_be_visible()



    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor seleccione una raza")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un peso")).to_be_visible()


        self.page.get_by_label("Nombre").fill("Firulais")
        self.page.select_option("#breed", label="Labrador")  # Usa select_option para seleccionar la raza
        self.page.get_by_label("Fecha de Cumpleaños").fill("2026-01-01")
        self.page.get_by_label("Peso").fill("130.000")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor seleccione una raza")).not_to_be_visible()
        expect(self.page.get_by_text("La fecha de nacimiento no puede ser mayor o igual a la fecha actual")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un peso")).not_to_be_visible()


    def test_should_be_able_to_edit_a_pet(self):
        pet = Pet.objects.create(
            name="Firulais",
            breed="Labrador",
            birthday="2022-01-01",
            weight= Decimal("150.752"),
        )

        path = reverse("pets_edit", kwargs={"id": pet.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Pepito")
        self.page.select_option("#breed", label="Beagle")  # Usa select_option para seleccionar la raza
        self.page.get_by_label("Fecha de Cumpleaños").fill("2002-10-10")
        self.page.get_by_label("Peso").fill("150.752")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Firulais")).not_to_be_visible()
        expect(self.page.get_by_text("Labrador")).not_to_be_visible()
        expect(self.page.get_by_text("Jan. 1, 2022")).not_to_be_visible()

        expect(self.page.get_by_text("Pepito")).to_be_visible()
        expect(self.page.get_by_text("Beagle")).to_be_visible()
        expect(self.page.get_by_text("Oct. 10, 2002")).to_be_visible()
        expect(self.page.get_by_text("150.752")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id}),
        )

# TEST DE PRODUCTS
class ProductCreatePriceGreaterThanZeroTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_product(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Amoxicilina")
        self.page.get_by_label("Tipo").fill("Antibiotico")
        self.page.get_by_label("Precio").fill("100")

        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Amoxicilina")).to_be_visible()
        expect(self.page.get_by_text("Antibiotico")).to_be_visible()
        #expect(self.page.get_by_text("Proveedor 1")).to_be_visible()
        expect(self.page.get_by_text("100")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid_with_price_less_than_zero(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()

        expect(self.page.get_by_text("Por favor ingrese un tipo")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio")).to_be_visible()
        

        self.page.get_by_label("Nombre").fill("Amoxicilina")
        self.page.get_by_label("Tipo").fill("Antibiótico")
        self.page.get_by_label("Precio").fill("-10")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).not_to_be_visible()
        expect(self.page.get_by_text("El precio debe ser mayor que cero")).to_be_visible()

# TEST DE MEDICINES
class MedicineCreateDoseRangeOneToTen(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_medicine(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Diclofenaco")
        self.page.get_by_label("Descripción").fill("Calma el dolor")
        self.page.get_by_label("Dosis").fill("3")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Diclofenaco")).to_be_visible()
        expect(self.page.get_by_text("Calma el dolor")).to_be_visible()
        expect(self.page.get_by_text("3")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid_with_price_greater_than_ten(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripción")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()


        self.page.get_by_label("Nombre").fill("Diclofenaco")
        self.page.get_by_label("Descripción").fill("Calma el dolor")
        self.page.get_by_label("Dosis").fill("13")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripción")).not_to_be_visible()
        expect(self.page.get_by_text("La dosis debe estar en un rango de 1 a 10")).to_be_visible()
    
    def test_should_view_errors_if_form_is_invalid_with_price_less_than_one(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripción")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()


        self.page.get_by_label("Nombre").fill("Diclofenaco")
        self.page.get_by_label("Descripción").fill("Calma el dolor")
        self.page.get_by_label("Dosis").fill("-3")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripción")).not_to_be_visible()
        expect(self.page.get_by_text("La dosis debe estar en un rango de 1 a 10")).to_be_visible()

# TEST DE PROVIDERS
class ProvidersRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).to_be_visible()

    def test_should_show_providers_data_with_address(self):
        Provider.objects.create(
            name="Proveedor 1",
            email="proveedor1@example.com",
            address="Dirección 1",
        )

        Provider.objects.create(
            name="Proveedor 2",
            email="proveedor2@example.com",
            address="Dirección 2",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Proveedor 1")).to_be_visible()
        expect(self.page.get_by_text("proveedor1@example.com")).to_be_visible()
        expect(self.page.get_by_text("Dirección 1")).to_be_visible()

        expect(self.page.get_by_text("Proveedor 2")).to_be_visible()
        expect(self.page.get_by_text("proveedor2@example.com")).to_be_visible()
        expect(self.page.get_by_text("Dirección 2")).to_be_visible()

    def test_should_show_add_provider_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo proveedor", exact=False,
        )
        expect(add_provider_action).to_have_attribute("href", reverse("providers_form"))

    def test_should_show_provider_edit_action(self):
        provider = Provider.objects.create(
            name="Proveedor de Prueba",
            email="proveedor@ejemplo.com",
            address="Calle Falsa 123",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id}),
        )

    def test_should_show_provider_delete_action(self):
        provider = Provider.objects.create(
            name="Proveedor de Prueba",
            email="proveedor@ejemplo.com",
            address="Calle Falsa 123",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de proveedor",
        )
        provider_id_input = edit_form.locator("input[name=provider_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("providers_delete"))
        expect(provider_id_input).not_to_be_visible()
        expect(provider_id_input).to_have_value(str(provider.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_be_able_to_delete_a_provider(self):
        Provider.objects.create(
            name="Proveedor de Prueba",
            email="proveedor@ejemplo.com",
            address="Calle Falsa 123",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("Proveedor de Prueba")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("providers_delete"))

        # Verificar que el envío del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Proveedor de Prueba")).not_to_be_visible()

class ProviderCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_provider_with_address(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Proveedor de Prueba")
        self.page.get_by_label("Email").fill("proveedor@ejemplo.com")
        self.page.get_by_label("Dirección").fill("Calle Falsa 123")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Proveedor de Prueba")).to_be_visible()
        expect(self.page.get_by_text("proveedor@ejemplo.com")).to_be_visible()
        expect(self.page.get_by_text("Calle Falsa 123")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

    def test_should_be_able_to_edit_a_provider_with_address(self):
        provider = Provider.objects.create(
            name="Proveedor Original",
            email="original@ejemplo.com",
            address="Dirección Original",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Proveedor Actualizado")
        self.page.get_by_label("Email").fill("actualizado@ejemplo.com")
        self.page.get_by_label("Dirección").fill("Dirección Actualizada")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Proveedor Original")).not_to_be_visible()
        expect(self.page.get_by_text("Dirección Original")).not_to_be_visible()
        expect(self.page.get_by_text("actualizado@ejemplo.com")).to_be_visible()
        expect(self.page.get_by_text("Dirección Actualizada")).to_be_visible()

