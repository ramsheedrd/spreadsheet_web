import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from .models import Sheets

# Create your views here.


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'

    def get_queryset(self, request):
        queryset = Sheets.objects.filter(user = request.user)
        return queryset

    def get(self, request, id=None):
        if id: # modify sheet
            sheet = Sheets.objects.get(id=id)
            if request.user == sheet.user:
                context = {
                    'new_sheet': sheet,
                    'sheets': self.get_queryset(request)
                }
                return render(request, self.template_name, context)
                
        return render(request, self.template_name, {'sheets': self.get_queryset(request)})

    def post(self, request, id=None):
        title = request.POST.get('title')
        rows = request.POST.get('rows')
        cols = request.POST.get('cols')

        if not (title and rows and cols):
            return redirect('/')

        sheet = Sheets.objects.create(user=request.user, title=title)
        print(rows, cols)
        context = {
            'new_sheet': sheet,
            'rows': rows, 'cols': cols,
            'sheets': self.get_queryset(request)
            }
        return render(request, self.template_name, context)


@csrf_exempt
@login_required
def auto_save_sheet(request):
    post_data = json.loads(request.body)    
    id = post_data.get('sheetId')
    data = post_data.get('sheetData')
    if id and data:
        sheet = Sheets.objects.get(id=id)
        sheet.sheet_data = data
        sheet.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})

@login_required
def load_data(request, id):
    sheet = Sheets.objects.get(id=id)
    return JsonResponse({'data': sheet.sheet_data}, safe=False)



        



    


        

