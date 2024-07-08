from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse

from django.core.mail import send_mail
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    
    def get_queryset(self) -> QuerySet[Agent]:
        organisation  = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView): 
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm
    
    def get_success_url(self) -> str:
        return reverse("agents:agent-list")
    
    def form_valid(self, form: AgentModelForm) -> HttpResponse:
        # This saves the Python object but not in the database
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password("123")
        user.save()
        Agent.objects.create(
            user = user,
            organisation  = self.request.user.userprofile
        )
        send_mail(
            subject = "You are invited to be an agent",
            message = "You were added as an agent on DJCRM.Please login to start Working",
            from_email = "admin@test.com",
            recipient_list = [user.email],
        )
       # agent.organisation = self.request.user.userprofile
      #  agent.save()  # Now save in the database
        return super().form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin,generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'
    
    
    def get_queryset(self) -> QuerySet[Agent]:
        organisation  = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm
    model = Agent
    
    def get_success_url(self) -> str:
        return reverse("agents:agent-list")
    #no need of this as we have already mentioned organisation while creating
    # def form_valid(self, form: AgentModelForm) -> HttpResponse:
    #     # This saves the Python object but not in the database
    #     agent = form.save(commit=False)
    #     agent.organisation = self.request.user.userprofile
    #     agent.save()  # Now save in the database
    #     return super().form_valid(form)

class AgentDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'
    
    def get_success_url(self) -> str:
        return reverse("agents:agent-list")
    
    def get_queryset(self) -> QuerySet[Agent]:
        organisation  = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
