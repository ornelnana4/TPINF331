from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Notes.models import Semestres, Niveau, UE, Etudiant, Enseignant, Evaluation, EC, Choisir

def Acceuil(request):
    return render(request, 'index.html')

def choose_account(request):
    return render(request, 'choose_account.html')

def register_student(request):
    liste_niveau = Niveau.objects.all()
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        genre = request.POST.get('genre')
        date = request.POST.get('date')
        email = request.POST.get('email')
        password = request.POST.get('password')
        niveau = request.POST.get('niveau')
        
        model_niv = Niveau.objects.get(Niv = niveau)
          
        new_student = Etudiant.objects.create(Matricule = matricule, Nom = nom, Genre = genre, DateNaiss = date, Email = email, Password = password, Niveau_etu = model_niv)
        new_student.save()
        
        return redirect('choice_ue', matricule=new_student.Matricule)
    
    return render(request, 'student_register.html', {'liste_niveau': liste_niveau})

def choisir_ue(request, matricule):
    etudiant = get_object_or_404(Etudiant, Matricule=matricule)
    ue = UE.objects.all()
    contexte = {
        'etudiant': etudiant,
        'ue': ue,
    }
    return render(request, 'choice_ue.html', contexte)

def choisir_ue2(request):
    if request.method == 'POST':
        multi = request.POST.getlist('multi')
        matricule = request.POST.get('nom')
        request.session['matricule']=matricule
        
        etudiant = Etudiant.objects.get(Matricule = matricule)
        for elt in multi:
            ue = UE.objects.get(Code_ue = elt)
            choix = Choisir.objects.create(Code_ue = ue, Etudiant = etudiant)
            choix.save()
        return redirect('mainstudent')  
        
    return render(request, 'choice_ue.html')

def register_teacher(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        nom = request.POST.get('nom')
        genre = request.POST.get('genre')
        date = request.POST.get('date')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        new_teacher = Enseignant.objects.create(Nom = nom, DateNaiss = date, Genre = genre, Email = email, Password = password, Numtel = phone)
        new_teacher.save()
    
    return render(request, 'teacher_register.html')

def login_student(request):
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        password = request.POST.get('password')
        
        e = Etudiant.objects.all()
        for el in e :
            if(el.Password==password and el.Matricule==matricule):
                messages.success(request, 'Connected')
                print("Vue")
                return redirect('student')
            else:
                print("Pas vue")
    return render(request, 'pages-login.html')

def login_teacher(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        e = Enseignant.objects.all()
        for el in e :
            if(el.Password==password and el.Email==email):
                messages.success(request, 'Connected')
                print("Vue")
                return redirect('teacher')
            else:
                print("Pas vue")
        pass
    
    return render(request, 'teacher_login.html')

def mainstudent(request):
    matricule=request.session.get('matricule',None)
    etudiant = Etudiant.objects.get(Matricule=matricule)
    choisir = Choisir.objects.filter(Etudiant=etudiant)
    evaluation = Evaluation.objects.filter(Etudiant=etudiant)
    
    listedesnotefinale = {}
    sum = 0
    
    for choix in choisir:
        for eval in evaluation:
            if eval.Code_ue.Code_ue == choix.Code_ue.Code_ue:
                sum += eval.Note
        listedesnotefinale[eval.Code_ue.Code_ue] = sum
        continue
    
    print(listedesnotefinale)
    
    contexte = {
        'etudiant': etudiant,
        'choisir': choisir,
        'evaluation': evaluation,
        'final': listedesnotefinale,
    }
    
    return render(request, 'studentnote.html',contexte)