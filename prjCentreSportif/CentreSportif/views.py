from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout

def accueil(request):
    activite = Activite.objects.all()
    return render(request, 'accueil.html', {'activite': activite})

def apropos(request):
    return render(request, 'apropos.html')

def sign_up(request):
    errors = {}
    suggestions = []
    message = ""
    user = None
    
    if request.method == 'POST':
        nom = request.POST.get('nom_client', None)
        prenom = request.POST.get('prenom_client', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        age = request.POST.get('age', None)
        choix_sport = request.POST.get('choix_sport', None)
        password = request.POST.get('password')

        # Validation du nom
        if not nom or len(nom) < 2:
            errors['nom'] = "Le nom doit contenir au moins 2 caractères"

        # Validation du prénom
        if not prenom or len(prenom) < 2:
            errors['prenom'] = "Le prénom doit contenir au moins 2 caractères"

        # Validation de l'email
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                errors['email'] = "Cet email est déjà utilisé"
        except ValidationError:
            errors['email'] = "L'email n'est pas dans le bon format"

        # Validation de l'âge
        if not age or not age.isdigit() or int(age) < 0:
            errors['age'] = "L'âge doit être un nombre positif"

        # Validation du choix de sport
        if not choix_sport or len(choix_sport) < 2:
            errors['choix_sport'] = "Le choix de sport doit contenir au moins 2 caractères"

        # Validation du mot de passe
        if not password or len(password) < 8:
            errors['password'] = "Le mot de passe doit contenir au moins 8 caractères"

        # Validation du nom d'utilisateur
        if User.objects.filter(username=username).exists():
            errors['username'] = "Ce nom d'utilisateur existe déjà. Voici quelques suggestions :"
            for i in range(10):
                suggestion = f"{username}{i}"
                if not User.objects.filter(username=suggestion).exists():
                    suggestions.append(suggestion)

        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password)
            client = Client(
                nom_client=nom,
                prenom_client=prenom,
                email=email,
                age=int(age),
                choix_sport=choix_sport,
                password=password,
                user=user
            )
            client.save()
            return redirect('accueil')

    data = {
        'errors': errors,
        'suggestions': suggestions,
        'message': message,
        'user': user  
    }
    return render(request, 'register.html', data)
@login_required
def inscription(request, activite_id):
    client = Client.objects.filter(user=request.user).first()
    if not client:
        return redirect('sign_up')  
    return redirect('inscription_activite', activite_id=activite_id)

@login_required
def inscription_activite(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)
    message = None  

    if request.method == 'POST':
        client = request.user.client  
        horaire_id = request.POST.get('horaire_id')

        if not horaire_id:
            return render(request, 'inscription_activite.html', {
                'activite': activite,
                'horaires': Horaire.objects.filter(activite=activite),
                'error': 'Veuillez sélectionner un horaire.'
            })

        horaire = get_object_or_404(Horaire, id=horaire_id)
        statut_inscription = 'en cours'

        inscription = Inscription(
            client=client,
            activite=activite,
            horaire=horaire,
            statut_inscription=statut_inscription
        )
        inscription.save()
        message = "Inscription réussie !"  

    context = {
        'activite': activite,
        'horaires': Horaire.objects.filter(activite=activite),
        'message': message  
    }
    return render(request, 'inscription_activite.html', context)

# @login_required
# def confirmation_activite(request, inscription_id):
#     inscription = get_object_or_404(Inscription, id=inscription_id)
#     return render(request, 'confirmation_activite.html', {'inscription': inscription})

def sign_in(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('accueil')
        else:
            errors['login'] = "Nom d'utilisateur ou mot de passe incorrect"
    
    return render(request, 'login.html', {'errors': errors})

# def sign_in(request):
#     errors = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('accueil')
#         else:
#             errors['login'] = "Nom d'utilisateur ou mot de passe incorrect"
    
#     return render(request, 'login.html', {'errors': errors})


@staff_member_required
def admin_dashboard(request):
    activites = Activite.objects.all()
    clients = Client.objects.all()
    moniteurs = Moniteur.objects.all()
    return render(request, 'admin_dashboard.html', {
        'activites': activites,
        'clients': clients,
        'moniteurs': moniteurs
    })


@login_required
@staff_member_required
def gestion_activites(request):
    activites = Activite.objects.all()
    return render(request, 'gestion_activites.html', {'activites': activites})

def gestion_clients(request):
    clients = Client.objects.all()
    return render(request, 'gestion_clients.html', {'clients': clients})

def admin_moniteurs(request):
    moniteurs = Moniteur.objects.all()
    return render(request, 'admin_moniteurs.html', {'moniteurs': moniteurs})


# def log_out(request):
#     return render(request, 'login.html', {})

def log_out(request):
    logout(request)
    return redirect('sign_in')

def dashboard(request):
    return render(request, 'admin.html', {})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        user = client.user
        client.delete()
        user.delete()  # Suppression du compte utilisateur associé
        messages.success(request, "Le client a été supprimé avec succès.")
        return redirect('admin_clients')
    return render(request, 'admin_clients.html')


@login_required
@staff_member_required
def add_activite(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        Activite.objects.create(nom=nom, description=description)
        messages.success(request, "Activité ajoutée avec succès.")
        return redirect('gestion_activites')
    return render(request, 'gestion_activites.html')

@login_required
@staff_member_required
def edit_activite(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)
    if request.method == 'POST':
        activite.nom = request.POST.get('nom')
        activite.description = request.POST.get('description')
        activite.save()
        messages.success(request, "Activité modifiée avec succès.")
        return redirect('gestion_activites')
    return render(request, 'edit_activite.html', {'activite': activite})

@login_required
@staff_member_required
def delete_activite(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)
    if request.method == "POST":
        activite.delete()
        messages.success(request, "Activité supprimée avec succès.")
        return redirect('gestion_activites')
    return render(request, 'gestion_activites.html')

def gestion_inscription(request):
    inscriptions = Inscription.objects.all()
    return render(request, 'gestion_inscription.html', {'inscriptions': inscriptions})

def gestion_paiements(request):
    paiements = Paiement.objects.all()
    return render(request, 'gestion_paiements.html', {'paiements': paiements})

def gestion_moniteurs(request):
    moniteurs = Moniteur.objects.all()
    return render(request, 'gestion_moniteurs.html', {'moniteurs': moniteurs})

def gestion_horaires(request):
    horaires = Horaire.objects.all()
    return render(request, 'gestion_horaires.html', {'horaires': horaires})
@login_required
@staff_member_required
def delete_inscription(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)
    if request.method == "POST":
        inscription.delete()
        messages.success(request, "Inscription supprimée avec succès.")
        return redirect('admin_inscriptions')
    return render(request, 'admin_inscriptions.html')

@login_required
@staff_member_required
def add_moniteur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        Moniteur.objects.create(nom=nom, prenom=prenom, email=email)
        messages.success(request, "Moniteur ajouté avec succès.")
        return redirect('admin_moniteurs')
    return render(request, 'admin_moniteurs.html')

@login_required
@staff_member_required
def edit_moniteur(request, moniteur_id):
    moniteur = get_object_or_404(Moniteur, id=moniteur_id)
    if request.method == 'POST':
        moniteur.nom = request.POST.get('nom')
        moniteur.prenom = request.POST.get('prenom')
        moniteur.email = request.POST.get('email')
        moniteur.save()
        messages.success(request, "Moniteur modifié avec succès.")
        return redirect('admin_moniteurs')
    return render(request, 'edit_moniteur.html', {'moniteur': moniteur})

@login_required
@staff_member_required
def delete_moniteur(request, moniteur_id):
    moniteur = get_object_or_404(Moniteur, id=moniteur_id)
    if request.method == "POST":
        moniteur.delete()
        messages.success(request, "Moniteur supprimé avec succès.")
        return redirect('admin_moniteurs')
    return render(request, 'admin_moniteurs.html')

@login_required
@staff_member_required
def add_horaire(request):
    if request.method == 'POST':
        activite_id = request.POST.get('activite')
        jour = request.POST.get('jour')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        moniteur_id = request.POST.get('moniteur')
        activite = get_object_or_404(Activite, id=activite_id)
        moniteur = get_object_or_404(Moniteur, id=moniteur_id)
        Horaire.objects.create(activite=activite, jour=jour, heure_debut=heure_debut, heure_fin=heure_fin, moniteur=moniteur)
        messages.success(request, "Horaire ajouté avec succès.")
        return redirect('gestion_horaires')
    return render(request, 'gestion_horaires.html')

@login_required
@staff_member_required
def edit_horaire(request, horaire_id):
    horaire = get_object_or_404(Horaire, id=horaire_id)
    if request.method == 'POST':
        activite_id = request.POST.get('activite')
        jour = request.POST.get('jour')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        moniteur_id = request.POST.get('moniteur')
        horaire.activite = get_object_or_404(Activite, id=activite_id)
        horaire.jour = jour
        horaire.heure_debut = heure_debut
        horaire.heure_fin = heure_fin
        horaire.moniteur = get_object_or_404(Moniteur, id=moniteur_id)
        horaire.save()
        messages.success(request, "Horaire modifié avec succès.")
        return redirect('gestion_horaires')
    activites = Activite.objects.all()
    moniteurs = Moniteur.objects.all()
    return render(request, 'edit_horaire.html', {'horaire': horaire, 'activites': activites, 'moniteurs': moniteurs})

@login_required
@staff_member_required
def delete_horaire(request, horaire_id):
    horaire = get_object_or_404(Horaire, id=horaire_id)
    if request.method == "POST":
        horaire.delete()
        messages.success(request, "Horaire supprimé avec succès.")
        return redirect('gestion_horaires')
    return render(request, 'gestion_horaires.html')

# from django.shortcuts import render, redirect
# # from django.http import HttpResponse
# from .models import Activite, Client
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User

# def accueil(request):
#     activite = Activite.objects.all()
#     return render(request, 'accueil.html', {'activite': activite})

# def sign_up(request):
#     errors = {}
#     message = ""
#     if request.method == 'POST':
#         nom = request.POST.get('nom_client', None)
#         prenom = request.POST.get('prenom_client', None)
#         email = request.POST.get('email', None)
#         age = request.POST.get('age', None)
#         choix_sport = request.POST.get('choix_sport', None)
#         password = request.POST.get('password')

#         # Validation du nom
#         if not nom or len(nom) < 2:
#             errors['nom'] = "Le nom doit contenir au moins 2 caractères"

#         # Validation du prénom
#         if not prenom or len(prenom) < 2:
#             errors['prenom'] = "Le prénom doit contenir au moins 2 caractères"

#         # Validation de l'email
#         try:
#             validate_email(email)
#             if User.objects.filter(email=email).exists():
#                 errors['email'] = "Cet email est déjà utilisé"
#         except ValidationError:
#             errors['email'] = "L'email n'est pas dans le bon format"
#         # Validation de l'âge
#         if not age or not age.isdigit() or int(age) < 0:
#             errors['age'] = "L'âge doit être un nombre positif"

#         # Validation du choix de sport
#         if not choix_sport or len(choix_sport) < 2:
#             errors['choix_sport'] = "Le choix de sport doit contenir au moins 2 caractères"

#         # Validation du mot de passe
#         if not password or len(password) < 8:
#             errors['password'] = "Le mot de passe doit contenir au moins 8 caractères"
#     else:
#         errors = {}
#         message = ""
#     print("=="*5, "NEW POST: ",nom, prenom, email, age, choix_sport, password, "=="*5)
#     data = {
#             'errors':errors,
#             'message':message
#         }    
#     return render(request, 'register.html', data)
    

# def sign_in(request):
#     return render(request, 'login.html', {})

# def log_out(request):
#     return render(request,'login.html', {})

# def dashboard(request):
#     return render(request, 'admin.html', {})



# def sign_up(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Votre compte a été créé avec succès.')
#             return redirect('accueil')  # Redirige vers la page d'accueil après inscription
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})

# def sign_in(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, 'Connexion réussie.')
#             return redirect('accueil')  # Redirige vers la page d'accueil après connexion
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})

# def log_out(request):
#     if request.method == 'POST':
#         logout(request)
#         messages.success(request, 'Déconnexion réussie.')
#         return redirect('accueil')  
#     return render(request, 'login.html')
