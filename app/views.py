from django.shortcuts import get_object_or_404, redirect, render, reverse

from app.models import Breed, Client, Medicine, Pet, Product, Provider, Vet


def home(request):
    return render(request, "home.html")


def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request, id=None):
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            saved, errors = client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST},
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})


def clients_delete(request):
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))

##Medicines

def medicines_repository(request):
    medicines = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicines})

def medicines_form(request, id=None):
    if request.method == "POST":
        medicine_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if medicine_id == "":
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            medicine.update_medicine(request.POST)
        if saved:
            return redirect(reverse("medicines_repo"))

        return render(
            request, "medicines/form.html", {"errors": errors, "medicine": request.POST},
        )

    medicine = None
    if id is not None:
        medicine = get_object_or_404(Medicine, pk=id)

    return render(request, "medicines/form.html", {"medicine": medicine})

def medicines_delete(request):
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()

    return redirect(reverse("medicines_repo"))



##Pets
def pets_repository(request):
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pets_history(request, id):
    pet = get_object_or_404(Pet.objects.prefetch_related("medicines", "vets"), id=id)  # Usa "Vets" en mayúscula

    context = {
        "pet": pet,
    }
    return render(request, "pets/history.html", context)

# def pets_form(request, id=None):
    clients = Client.objects.all()
    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
            # Obtener el ID del cliente seleccionado del formulario
            client_id = request.POST.get("client", "")
            # Asociar el cliente seleccionado con el animal creado
            if client_id:
                pet = Pet.objects.latest('id')  # Obtener el último animal creado
                pet.client_id = client_id
                pet.save()

        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            pet.update_pet(request.POST)
            # Obtener el ID del cliente seleccionado del formulario
            client_id = request.POST.get("client", "")
            # Asociar el cliente seleccionado con el animal actualizado
            if client_id:
                pet.client_id = client_id
                pet.save()

        if saved:
            return redirect(reverse("pets_repo"))


        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST, "clients": clients},
        )

    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet, "clients": clients})


# def pets_form(request, id=None):
#     clients = Client.objects.all()
#     if request.method == "POST":
#         pet_id = request.POST.get("id", "")
#         errors = {}
#         saved = True

#         if pet_id == "":
#             saved, errors = Pet.save_pet(request.POST)
#             # Si el objeto Pet se ha creado correctamente
#             if saved:
#                 # Obtener el ID del cliente seleccionado del formulario
#                 client_id = request.POST.get("client", "")
#                 # Asociar el cliente seleccionado con el animal creado
#                 if client_id:
#                     pet = Pet.objects.latest('id')  # Obtener el último animal creado
#                     pet.client_id = client_id
#                     pet.save()
#         else:
#             pet = get_object_or_404(Pet, pk=pet_id)
#             pet.update_pet(request.POST)
#             # Obtener el ID del cliente seleccionado del formulario
#             client_id = request.POST.get("client", "")
#             # Asociar el cliente seleccionado con el animal actualizado
#             if client_id:
#                 pet.client_id = client_id
#                 pet.save()

#         if saved:
#             return redirect(reverse("pets_repo"))

#         return render(
#             request, "pets/form.html", {"errors": errors, "pet": request.POST, "clients": clients},
#         )

#     pet = None
#     if id is not None:
#         pet = get_object_or_404(Pet, pk=id)

#     return render(request, "pets/form.html", {"pet": pet, "clients": clients})


def pets_form(request, id=None):
    clients = Client.objects.all()
    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
            # Si el objeto Pet se ha creado correctamente
            if saved:
                # Obtener el ID del cliente seleccionado del formulario
                client_id = request.POST.get("client", "")
                # Asociar el cliente seleccionado con el animal creado
                if client_id:
                    pet = Pet.objects.latest('id')  # Obtener el último animal creado
                    pet.client_id = client_id
                    pet.save()
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            saved, errors = pet.update_pet(request.POST)
            if saved:
            # Obtener el ID del cliente seleccionado del formulario
                client_id = request.POST.get("client", "")
            # Asociar el cliente seleccionado con el animal actualizado
                if client_id:
                    pet.client_id = client_id
                    pet.save()

        if saved:
            return redirect(reverse("pets_repo"))

        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST, "clients": clients, "Breed": Breed, } ,
        )

    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet, "clients": clients, "Breed": Breed,})


def pets_form_history(request, id):
    vets = Vet.objects.all()
    medicines = Medicine.objects.all()
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True
        
        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
            medicine_id = request.POST.get("medicines", "")
            vet_id = request.POST.get("vet", "")
            
            if medicine_id and vet_id:
                pet.medicines.add(medicine_id)
                pet.vets.add(vet_id)
                pet.save()
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            pet.update_pet(request.POST)
            
            medicine_id = request.POST.get("medicines", "")
            vet_id = request.POST.get("vet", "")
            
            if medicine_id and vet_id:
                pet.medicines.add(medicine_id)
                pet.vets.add(vet_id)
                pet.save()
        
        if saved:
            return redirect(reverse("pets_history", args=(id,)))

        # Si no se guarda correctamente, debe retornar algo
        return render(request, 'pets/history.html', {
            'pet': pet,
            'vets': vets,
            'medicines': medicines,
            'errors': errors,  # Muestra errores si hay
        })
    
    # Manejo para solicitudes GET
    return render(request, 'pets/form_history.html', {
        'pet': pet,
        'vets': vets,
        'medicines': medicines,
    })



def pets_delete(request):
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pets_repo"))

##Products
def products_repository(request):
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})

def products_form(request, id=None):
    providers = Provider.objects.all()
    if request.method == "POST":
        product_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if product_id == "":
            saved, errors = Product.save_product(request.POST)
            # Obtener el ID del proveedor seleccionado del formulario
            provider_id = request.POST.get("provider", "")
            # Asociar el proveedor seleccionado con el producto creado
            if provider_id:
                product = Product.objects.latest('id')  # Obtener el último producto creado
                product.provider_id = provider_id
                product.save()
        else:
            product = get_object_or_404(Product, pk=product_id)
            saved, errors = product.update_product(request.POST)
            if saved:
                # Obtener el ID del proveedor seleccionado del formulario
                provider_id = request.POST.get("provider", "")
            # Asociar el proveedor seleccionado con el producto actualizado
                if provider_id:
                    product.provider_id = provider_id
                    product.save()
        
        if saved:
            return redirect(reverse("products_repo"))
        
        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST, "providers": providers},
        )

    product = None
    if id is not None:
        product = get_object_or_404(Product, pk=id)

    return render(request, "products/form.html", {"product": product, "providers": providers})

def products_delete(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("products_repo"))
    
##Provider
def providers_repository(request):
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def providers_form(request, id=None):
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            saved, errors = provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("providers_repo"))

        # Si no se guardó correctamente, renderiza el formulario con los errores
        return render(request, "providers/form.html", {"errors": errors, "provider": request.POST})

    # Método GET: cargar formulario para crear nuevo proveedor o editar existente
    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})


def providers_delete(request):
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("providers_repo"))


##Vets
def vets_repository(request):
    vets = Vet.objects.all()
    return render(request, "vets/repository.html", {"vets": vets})

def vets_form(request, id=None):
    if request.method == "POST":
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            vet.update_vet(request.POST)
        if saved:
            return redirect(reverse("vets_repo"))
        

        return render(
            request, "vets/form.html", {"errors": errors, "vet": request.POST},
        )

    vet = None
    if id is not None:
        vet = get_object_or_404(Vet, pk=id)

    return render(request, "vets/form.html", {"vet": vet})

def vets_delete(request):
    vet_id = request.POST.get("vet_id")
    vet = get_object_or_404(Vet, pk=int(vet_id))
    vet.delete()

    return redirect(reverse("vets_repo"))