from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mahasiswa.models import Pkl
from . import models, forms
from catatan.models import Catatan


def index(req):
    return render(req, 'dosen/index.html')

def index_staf(req):
    tasks = models.Dosen.objects.all()
    dosen = models.User.objects.all()
    form_input = forms.DosenForm()
    form_user = forms.CreateUserForm()

    if req.POST:
        form_input = forms.DosenForm(req.POST, req.FILES)
        form_user = forms.CreateUserForm(req.POST)
        if form_input.is_valid() or form_user.is_valid():
            form_input.save()
            form_user.save()
            return redirect('/dosens/')

    return render(req, 'dosens/index.html',{
        'data': tasks,
        'form' : form_input,
        'form_user' : form_user,
        'dosen' : dosen,
    })

def catatan(req, id):
    dosen = models.Dosen.objects.all()

    group = req.user.groups.first(pk=id)
    if group is not None and group.name == 'dosen':
        mahasiswa = models.Pkl.objects.all()
    return render(req, 'dosen/catatan.html',{
        'data': dosen,
        'data': mahasiswa,
    })

def update_staf(req, id):
    if req.POST:
        mitra = models.Dosen.objects.filter(pk=id).update(nip=req.POST['nip'], nama_dosen=req.POST['nama_dosen'], fakultas=req.POST['fakultas'], jurusan=req.POST['jurusan'])
        return redirect('/dosens/')

    dosen = models.Dosen.objects.filter(pk=id).first()
    return render(req, 'dosens/update.html', {
        'data': dosen,
    })

def delete_staf(req, id):
    models.Dosen.objects.filter(pk=id).delete()
    return redirect('/dosens/')

# def index_dosen(req):
#     group = req.user.groups.first() #mengambil group user
#     tasks = models.Pkl.objects.all() # mengambil semua object yang ada di models pkl
#     if group is not None and group.name == 'dosen': # mendefinisikan bahwa ini adalah dosen
#         pkls = models.Pkl.objects.filter(nama_dosen=req.user) # memfilter bahwa satu mahasiswa hanya boleh menginputkan satu dosen
#     return render(req, 'dosenah/index.html',{
#         'data': pkls,
#     })

def detail_dosen(req, id):
    catatans = Catatan.objects.filter(owner=catatan.owner) # mengambil semua object yang ada di models Catatan
    return render(req, 'dosens/detail.html',{
        'data': catatans,
    })
