from typing import Any
from django.core.mail import send_mail
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import QuerySet
from django.shortcuts import render , redirect , reverse
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView ,ListView,DetailView,CreateView,DeleteView,UpdateView
from .models import Lead , Agent , Category
from agents.mixins import OrganisorAndLoginRequiredMixin
from .forms import LeadForm , LeadModelform , CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm
# Create your views here



class SignupView(CreateView):
  template_name = "registration/signup.html"
  form_class = CustomUserCreationForm
  
  def get_success_url(self):
      return reverse("login")

class LandingPageView(TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request,"landing.html")

class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads/lead_list.html"
    
    #customise content
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context

    
def lead_list(request):
    leads  = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request,"leads/lead_list.html",context)


class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = "leads/lead_detail.html"  # Changed to a more appropriate template name
    model = Lead  # This automatically sets the queryset to Lead.objects.all()
    context_object_name = "lead"  # This customizes the context variable name
    def get_queryset(self) -> QuerySet[Any]:
        user  = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
                 
        else :
            # filter for partivular organisation 
            queryset =Lead.objects.filter(organisation = user.agent.organisation)
            #filter for particular agent now
            queryset = queryset.filter(agent__user = user)
        return queryset
def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context={
        "lead" : lead
    }
    return render(request,"leads/lead_detail.html",context)

# def lead_create(request):
    # form = LeadForm()
    # print(request.POST)
    # if request.method == "POST":
    #     print("receving a post request")
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         print("form is valid")
    #         print(form.cleaned_data)
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Lead.objects.create(first_name=first_name,last_name=last_name,age=age,agent=agent)
    #         print("lead has been created")
    #         return redirect("/leads")
        
        
#     context={
#         "form" : form
#     }
#     return render(request,"leads/lead_create.html",context)

class LeadCreateView(OrganisorAndLoginRequiredMixin,CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelform
    
    def get_success_url(self) :
        return reverse("leads:lead-list")
    
    #here are just overwritting this method
    # generally in create view we will enter the details to CreateView
    # afetr entering the deatils django will  check wheather the
    # entered are correct or not for that it will use form.is_valid()
    # ,If the form is valid it will return form_valid(form)
    # as here we we want to send email when the form is valid we will
    # over write the form_valid(form) and send email and again return the actual
    # fucntion
    
    def form_valid(self,form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        #To send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list = ["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)
    
def lead_create(request):
    form = LeadModelform()
    print(request.POST)
    if request.method == "POST":
        print("receving a post request")
        form = LeadModelform(request.POST)
        if form.is_valid():
            form.save()
            print("lead has been created")
            return redirect("/leads")
        
        
    context={
        "form" : form
    }
    return render(request,"leads/lead_create.html",context)


# def lead_update(request,pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     print(request.POST)
#     if request.method == "POST":
#         print("receving a post request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             print("lead has been updated")
#             return redirect("/leads")
        
#     context={
#         "lead" : lead,
#         "form"  : form
#      }
#     return render(request,"leads/lead_update.html",context)


class LeadUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelform
    model = Lead
    def get_success_url(self) :
        return reverse("leads:lead-list")
    
    def get_queryset(self) -> QuerySet[Any]:
        user  = self.request.user
        queryset = Lead.objects.filter(organisation = user.userprofile)
   
        return queryset
    
   
   
def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelform(instance = lead)
   
    if request.method == "POST":
        print("receving a post request")
        form = LeadModelform(request.POST,instance = lead)
        if form.is_valid():
            form.save()
            print("lead has been updates")
            return redirect("/leads")
   
        
    context={
        "lead" : lead,
        "form"  : form
     }
    return render(request,"leads/lead_update.html",context)
    

class LeadDeleteView(LoginRequiredMixin,DeleteView):
  template_name = "leads/lead_delete.html"

   
  def get_queryset(self) -> QuerySet[Any]:
        user  = self.request.user
        queryset = Lead.objects.filter(organisation = user.userprofile)
   
        return queryset
  def get_success_url(self) :
        return reverse("leads:lead-list")
def lead_delete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")    

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    



class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = Lead.objects.filter(category=self.get_object())
    #     context.update({
    #         "leads": leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset



class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail",kwargs={"pk":self.get_object().id})