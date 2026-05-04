import os

BASE = '/home/runner/work/textwave/textwave'

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"Written: {path}")

# requirements.txt
w('requirements.txt', """Django>=4.2,<5.0
Pillow>=10.0.0
""")

# manage.py
w('manage.py', """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'textwave.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""")

# textwave/__init__.py
w('textwave/__init__.py', '')

# textwave/settings.py
w('textwave/settings.py', """from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-textwave-secret-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.contacts',
    'apps.campaigns',
    'apps.reports',
    'apps.billing',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'textwave.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'textwave.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
""")

# textwave/urls.py
w('textwave/urls.py', """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('contacts/', include('apps.contacts.urls')),
    path('campaigns/', include('apps.campaigns.urls')),
    path('reports/', include('apps.reports.urls')),
    path('billing/', include('apps.billing.urls')),
    path('', include('apps.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
""")

# textwave/wsgi.py
w('textwave/wsgi.py', """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'textwave.settings')
application = get_wsgi_application()
""")

# textwave/asgi.py
w('textwave/asgi.py', """import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'textwave.settings')
application = get_asgi_application()
""")

# apps/__init__.py
w('apps/__init__.py', '')
w('apps/accounts/__init__.py', '')
w('apps/contacts/__init__.py', '')
w('apps/campaigns/__init__.py', '')
w('apps/reports/__init__.py', '')
w('apps/billing/__init__.py', '')
w('apps/core/__init__.py', '')
w('apps/core/management/__init__.py', '')
w('apps/core/management/commands/__init__.py', '')

# apps/accounts/apps.py
w('apps/accounts/apps.py', """from django.apps import AppConfig
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
""")

# apps/accounts/models.py
w('apps/accounts/models.py', """import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    sms_balance = models.IntegerField(default=0)
    api_key = models.CharField(max_length=64, unique=True, default='')
    sender_id = models.CharField(max_length=11, default='TextWave')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = uuid.uuid4().hex
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
""")

# apps/accounts/forms.py
w('apps/accounts/forms.py', """from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('phone', 'company', 'sender_id')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
""")

# apps/accounts/views.py
w('apps/accounts/views.py', """import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import LoginForm, RegisterForm, ProfileForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect(request.GET.get('next', 'core:dashboard'))
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully! Welcome to TextWave.')
        return redirect('core:dashboard')
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')
            user.save()
            profile_obj.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    return render(request, 'accounts/password_change.html', {'form': form})

@login_required
def regenerate_api_key(request):
    if request.method == 'POST':
        request.user.profile.api_key = uuid.uuid4().hex
        request.user.profile.save()
        messages.success(request, 'API key regenerated successfully.')
    return redirect('core:settings')
""")

# apps/accounts/urls.py
w('apps/accounts/urls.py', """from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', views.password_change_view, name='password_change'),
    path('regenerate-api-key/', views.regenerate_api_key, name='regenerate_api_key'),
]
""")

# apps/accounts/admin.py
w('apps/accounts/admin.py', """from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'company', 'sms_balance', 'sender_id', 'created_at']
    search_fields = ['user__username', 'user__email', 'company', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['api_key', 'created_at', 'updated_at']
""")

# apps/contacts/apps.py
w('apps/contacts/apps.py', """from django.apps import AppConfig
class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacts'
""")

# apps/contacts/models.py
w('apps/contacts/models.py', """from django.db import models
from django.contrib.auth.models import User

class ContactGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def contact_count(self):
        return self.contacts.count()

    class Meta:
        ordering = ['name']

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    group = models.ForeignKey(ContactGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone})"
""")

# apps/contacts/forms.py
w('apps/contacts/forms.py', """from django import forms
from .models import Contact, ContactGroup

class ContactGroupForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'phone', 'email', 'group')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ContactGroup.objects.filter(user=user)
        self.fields['group'].required = False

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}),
        help_text='CSV file with columns: name, phone, email (optional), group (optional)'
    )
    group = forms.ModelChoiceField(
        queryset=ContactGroup.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Assign all imported contacts to this group (optional)'
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ContactGroup.objects.filter(user=user)
""")

# apps/contacts/views.py
w('apps/contacts/views.py', """import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Contact, ContactGroup
from .forms import ContactForm, ContactGroupForm, CSVImportForm

@login_required
def contact_list(request):
    search = request.GET.get('search', '')
    group_filter = request.GET.get('group', '')
    contacts = Contact.objects.filter(user=request.user)
    if search:
        contacts = contacts.filter(Q(name__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search))
    if group_filter:
        contacts = contacts.filter(group_id=group_filter)
    groups = ContactGroup.objects.filter(user=request.user)
    paginator = Paginator(contacts, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'contacts/contact_list.html', {
        'page_obj': page_obj, 'groups': groups, 'search': search,
        'group_filter': group_filter, 'total_count': contacts.count(),
    })

@login_required
def contact_create(request):
    form = ContactForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        messages.success(request, f'Contact {contact.name} added successfully.')
        return redirect('contacts:contact_list')
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Add Contact'})

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    form = ContactForm(request.user, request.POST or None, instance=contact)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Contact {contact.name} updated successfully.')
        return redirect('contacts:contact_list')
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Edit Contact', 'contact': contact})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        name = contact.name
        contact.delete()
        messages.success(request, f'Contact {name} deleted.')
    return redirect('contacts:contact_list')

@login_required
def group_list(request):
    groups = ContactGroup.objects.filter(user=request.user)
    paginator = Paginator(groups, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'contacts/group_list.html', {'page_obj': page_obj})

@login_required
def group_create(request):
    form = ContactGroupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        group = form.save(commit=False)
        group.user = request.user
        group.save()
        messages.success(request, f'Group "{group.name}" created successfully.')
        return redirect('contacts:group_list')
    return render(request, 'contacts/group_form.html', {'form': form, 'title': 'Create Group'})

@login_required
def group_edit(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk, user=request.user)
    form = ContactGroupForm(request.POST or None, instance=group)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Group "{group.name}" updated.')
        return redirect('contacts:group_list')
    return render(request, 'contacts/group_form.html', {'form': form, 'title': 'Edit Group', 'group': group})

@login_required
def group_delete(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk, user=request.user)
    if request.method == 'POST':
        name = group.name
        group.delete()
        messages.success(request, f'Group "{name}" deleted.')
    return redirect('contacts:group_list')

@login_required
def import_contacts(request):
    form = CSVImportForm(request.user, request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        csv_file = request.FILES['csv_file']
        group = form.cleaned_data.get('group')
        decoded = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
        success_count = 0
        error_count = 0
        for row in reader:
            try:
                name = row.get('name', '').strip()
                phone = row.get('phone', '').strip()
                if not name or not phone:
                    error_count += 1
                    continue
                email = row.get('email', '').strip()
                row_group = group
                if not row_group and row.get('group'):
                    row_group, _ = ContactGroup.objects.get_or_create(name=row['group'].strip(), user=request.user)
                Contact.objects.create(name=name, phone=phone, email=email, group=row_group, user=request.user)
                success_count += 1
            except Exception:
                error_count += 1
        messages.success(request, f'Import complete: {success_count} contacts added, {error_count} failed.')
        return redirect('contacts:contact_list')
    return render(request, 'contacts/import_contacts.html', {'form': form})
""")

# apps/contacts/urls.py
w('apps/contacts/urls.py', """from django.urls import path
from . import views
app_name = 'contacts'
urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='contact_create'),
    path('<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('import/', views.import_contacts, name='import_contacts'),
]
""")

# apps/contacts/admin.py
w('apps/contacts/admin.py', """from django.contrib import admin
from .models import Contact, ContactGroup

@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'contact_count', 'created_at']
    search_fields = ['name', 'user__username']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'group', 'user', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['group', 'created_at']
""")

# apps/campaigns/apps.py
w('apps/campaigns/apps.py', """from django.apps import AppConfig
class CampaignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.campaigns'
""")

# apps/campaigns/models.py
w('apps/campaigns/models.py', """from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('scheduled', 'Scheduled'), ('sending', 'Sending'),
        ('sent', 'Sent'), ('failed', 'Failed'),
    ]
    name = models.CharField(max_length=200)
    message = models.TextField()
    sender_id = models.CharField(max_length=11, default='TextWave')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def total_recipients(self):
        return self.recipients.count()

    def sent_count(self):
        return self.recipients.filter(status='sent').count()

    def delivered_count(self):
        return self.recipients.filter(status='delivered').count()

    def failed_count(self):
        return self.recipients.filter(status='failed').count()

    def pending_count(self):
        return self.recipients.filter(status='pending').count()

class CampaignRecipient(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('failed', 'Failed'),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='recipients')
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message_id = models.CharField(max_length=100, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.status}"
""")

# apps/campaigns/forms.py
w('apps/campaigns/forms.py', """from django import forms
from .models import Campaign
from apps.contacts.models import ContactGroup

class CampaignForm(forms.ModelForm):
    recipient_type = forms.ChoiceField(
        choices=[('groups', 'From Groups'), ('manual', 'Manual Numbers')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='manual'
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=ContactGroup.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    manual_numbers = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter phone numbers, one per line or comma-separated'}),
    )
    send_option = forms.ChoiceField(
        choices=[('now', 'Send Now'), ('schedule', 'Schedule'), ('draft', 'Save as Draft')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='now'
    )

    class Meta:
        model = Campaign
        fields = ('name', 'sender_id', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'id': 'message-textarea'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].queryset = ContactGroup.objects.filter(user=user)
        self.fields['sender_id'].initial = user.profile.sender_id if hasattr(user, 'profile') else 'TextWave'

    def clean(self):
        cleaned_data = super().clean()
        recipient_type = cleaned_data.get('recipient_type')
        if recipient_type == 'groups' and not cleaned_data.get('groups'):
            self.add_error('groups', 'Please select at least one group.')
        elif recipient_type == 'manual' and not cleaned_data.get('manual_numbers'):
            self.add_error('manual_numbers', 'Please enter at least one phone number.')
        return cleaned_data
""")

# apps/campaigns/services.py
w('apps/campaigns/services.py', """import uuid
from django.utils import timezone

class SMSGatewayService:
    def send_sms(self, phone, message, sender_id):
        return {"status": "delivered", "message_id": f"mock_{uuid.uuid4().hex[:8]}"}

    def send_bulk(self, recipients, message, sender_id):
        results = []
        for phone in recipients:
            result = self.send_sms(phone, message, sender_id)
            results.append({'phone': phone, 'status': result['status'], 'message_id': result['message_id']})
        return results


def send_campaign(campaign):
    from .models import CampaignRecipient
    service = SMSGatewayService()
    campaign.status = 'sending'
    campaign.save()
    recipients = campaign.recipients.filter(status='pending')
    success = 0
    failed = 0
    for recipient in recipients:
        try:
            result = service.send_sms(recipient.phone_number, campaign.message, campaign.sender_id)
            recipient.status = result['status']
            recipient.message_id = result['message_id']
            recipient.sent_at = timezone.now()
            recipient.save()
            if result['status'] in ('sent', 'delivered'):
                success += 1
            else:
                failed += 1
        except Exception:
            recipient.status = 'failed'
            recipient.save()
            failed += 1
    campaign.status = 'sent'
    campaign.save()
    total_sent = success
    if total_sent > 0 and hasattr(campaign.user, 'profile'):
        profile = campaign.user.profile
        profile.sms_balance = max(0, profile.sms_balance - total_sent)
        profile.save()
        from apps.billing.models import Transaction
        Transaction.objects.create(
            user=campaign.user, amount=0, credits=-total_sent,
            transaction_type='deduction', status='completed',
            description=f'SMS campaign: {campaign.name}'
        )
    return success, failed
""")

# apps/campaigns/views.py
w('apps/campaigns/views.py', """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Campaign, CampaignRecipient
from .forms import CampaignForm
from .services import send_campaign
from apps.contacts.models import Contact, ContactGroup

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.filter(user=request.user)
    paginator = Paginator(campaigns, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'campaigns/campaign_list.html', {'page_obj': page_obj})

@login_required
def campaign_create(request):
    form = CampaignForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        campaign = form.save(commit=False)
        campaign.user = request.user
        send_option = form.cleaned_data['send_option']
        if send_option == 'draft':
            campaign.status = 'draft'
        elif send_option == 'schedule':
            campaign.status = 'scheduled'
            scheduled_at = request.POST.get('scheduled_at')
            if scheduled_at:
                from django.utils.dateparse import parse_datetime
                campaign.scheduled_at = parse_datetime(scheduled_at)
        else:
            campaign.status = 'draft'
        campaign.save()
        recipient_type = form.cleaned_data['recipient_type']
        phones = set()
        if recipient_type == 'groups':
            for group in form.cleaned_data['groups']:
                for contact in Contact.objects.filter(group=group, user=request.user):
                    phones.add(contact.phone)
        else:
            raw = form.cleaned_data['manual_numbers']
            for p in raw.replace(',', '\\n').split('\\n'):
                p = p.strip()
                if p:
                    phones.add(p)
        for phone in phones:
            CampaignRecipient.objects.create(campaign=campaign, phone_number=phone)
        if send_option == 'now':
            if not phones:
                messages.error(request, 'No recipients found.')
                campaign.delete()
                return render(request, 'campaigns/campaign_form.html', {'form': form})
            balance = request.user.profile.sms_balance
            if balance < len(phones):
                messages.error(request, f'Insufficient SMS balance. You need {len(phones)} credits but have {balance}.')
                campaign.delete()
                return render(request, 'campaigns/campaign_form.html', {'form': form})
            success, failed = send_campaign(campaign)
            messages.success(request, f'Campaign sent! {success} delivered, {failed} failed.')
        elif send_option == 'schedule':
            messages.success(request, f'Campaign scheduled for {campaign.scheduled_at}.')
        else:
            messages.success(request, 'Campaign saved as draft.')
        return redirect('campaigns:campaign_list')
    return render(request, 'campaigns/campaign_form.html', {'form': form})

@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    recipients = campaign.recipients.all()
    paginator = Paginator(recipients, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    stats = {
        'total': campaign.total_recipients(),
        'sent': campaign.sent_count(),
        'delivered': campaign.delivered_count(),
        'failed': campaign.failed_count(),
        'pending': campaign.pending_count(),
    }
    return render(request, 'campaigns/campaign_detail.html', {'campaign': campaign, 'page_obj': page_obj, 'stats': stats})

@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if request.method == 'POST':
        name = campaign.name
        campaign.delete()
        messages.success(request, f'Campaign "{name}" deleted.')
    return redirect('campaigns:campaign_list')

@login_required
def campaign_send(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if request.method == 'POST' and campaign.status in ('draft', 'scheduled'):
        total = campaign.total_recipients()
        balance = request.user.profile.sms_balance
        if balance < total:
            messages.error(request, f'Insufficient balance. Need {total} credits, have {balance}.')
        else:
            success, failed = send_campaign(campaign)
            messages.success(request, f'Campaign sent! {success} delivered, {failed} failed.')
    return redirect('campaigns:campaign_detail', pk=pk)
""")

# apps/campaigns/urls.py
w('apps/campaigns/urls.py', """from django.urls import path
from . import views
app_name = 'campaigns'
urlpatterns = [
    path('', views.campaign_list, name='campaign_list'),
    path('create/', views.campaign_create, name='campaign_create'),
    path('<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('<int:pk>/delete/', views.campaign_delete, name='campaign_delete'),
    path('<int:pk>/send/', views.campaign_send, name='campaign_send'),
]
""")

# apps/campaigns/admin.py
w('apps/campaigns/admin.py', """from django.contrib import admin
from .models import Campaign, CampaignRecipient

class CampaignRecipientInline(admin.TabularInline):
    model = CampaignRecipient
    extra = 0
    readonly_fields = ['sent_at', 'created_at']

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status', 'total_recipients', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'user__username']
    inlines = [CampaignRecipientInline]

@admin.register(CampaignRecipient)
class CampaignRecipientAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'campaign', 'status', 'sent_at']
    list_filter = ['status']
    search_fields = ['phone_number', 'campaign__name']
""")

# apps/reports/apps.py
w('apps/reports/apps.py', """from django.apps import AppConfig
class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reports'
""")

# apps/reports/models.py
w('apps/reports/models.py', '# No models needed for reports app\n')

# apps/reports/views.py
w('apps/reports/views.py', """import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from apps.campaigns.models import CampaignRecipient, Campaign

@login_required
def report_list(request):
    status_filter = request.GET.get('status', '')
    campaign_filter = request.GET.get('campaign', '')
    recipients = CampaignRecipient.objects.filter(campaign__user=request.user).select_related('campaign')
    if status_filter:
        recipients = recipients.filter(status=status_filter)
    if campaign_filter:
        recipients = recipients.filter(campaign_id=campaign_filter)
    campaigns = Campaign.objects.filter(user=request.user)
    paginator = Paginator(recipients, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    stats = {
        'total': CampaignRecipient.objects.filter(campaign__user=request.user).count(),
        'sent': CampaignRecipient.objects.filter(campaign__user=request.user, status='sent').count(),
        'delivered': CampaignRecipient.objects.filter(campaign__user=request.user, status='delivered').count(),
        'failed': CampaignRecipient.objects.filter(campaign__user=request.user, status='failed').count(),
        'pending': CampaignRecipient.objects.filter(campaign__user=request.user, status='pending').count(),
    }
    return render(request, 'reports/report_list.html', {
        'page_obj': page_obj, 'stats': stats, 'campaigns': campaigns,
        'status_filter': status_filter, 'campaign_filter': campaign_filter,
    })

@login_required
def export_csv(request):
    recipients = CampaignRecipient.objects.filter(campaign__user=request.user).select_related('campaign')
    status_filter = request.GET.get('status', '')
    if status_filter:
        recipients = recipients.filter(status=status_filter)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="delivery_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Campaign', 'Phone Number', 'Status', 'Message ID', 'Sent At', 'Created At'])
    for r in recipients:
        writer.writerow([r.campaign.name, r.phone_number, r.status, r.message_id, r.sent_at, r.created_at])
    return response
""")

# apps/reports/urls.py
w('apps/reports/urls.py', """from django.urls import path
from . import views
app_name = 'reports'
urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('export/', views.export_csv, name='export_csv'),
]
""")

# apps/reports/admin.py
w('apps/reports/admin.py', 'from django.contrib import admin\n')

# apps/billing/apps.py
w('apps/billing/apps.py', """from django.apps import AppConfig
class BillingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.billing'
""")

# apps/billing/models.py
w('apps/billing/models.py', """from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('purchase', 'Purchase'), ('deduction', 'Deduction'),
        ('bonus', 'Bonus'), ('refund', 'Refund'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credits = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.credits} credits"
""")

# apps/billing/forms.py
w('apps/billing/forms.py', """from django import forms

CREDIT_PACKAGES = [
    ('100', '100 Credits - $1.00'),
    ('500', '500 Credits - $4.50'),
    ('1000', '1000 Credits - $8.00'),
    ('5000', '5000 Credits - $35.00'),
]

class PurchaseForm(forms.Form):
    package = forms.ChoiceField(
        choices=CREDIT_PACKAGES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Select Package'
    )
    payment_method = forms.ChoiceField(
        choices=[('card', 'Credit/Debit Card'), ('mobile', 'Mobile Money')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    card_number = forms.CharField(
        max_length=19, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'}),
    )
""")

# apps/billing/views.py
w('apps/billing/views.py', """from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Transaction
from .forms import PurchaseForm, CREDIT_PACKAGES

PACKAGE_PRICES = {
    '100': Decimal('1.00'), '500': Decimal('4.50'),
    '1000': Decimal('8.00'), '5000': Decimal('35.00'),
}

@login_required
def billing_view(request):
    form = PurchaseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        package = form.cleaned_data['package']
        credits = int(package)
        amount = PACKAGE_PRICES.get(package, Decimal('0'))
        profile = request.user.profile
        profile.sms_balance += credits
        profile.save()
        Transaction.objects.create(
            user=request.user, amount=amount, credits=credits,
            transaction_type='purchase', status='completed',
            description=f'Purchased {credits} SMS credits'
        )
        messages.success(request, f'Successfully purchased {credits} SMS credits!')
        return redirect('billing:billing')
    recent_transactions = Transaction.objects.filter(user=request.user)[:5]
    return render(request, 'billing/billing.html', {'form': form, 'recent_transactions': recent_transactions, 'packages': CREDIT_PACKAGES})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    paginator = Paginator(transactions, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'billing/transaction_history.html', {'page_obj': page_obj})
""")

# apps/billing/urls.py
w('apps/billing/urls.py', """from django.urls import path
from . import views
app_name = 'billing'
urlpatterns = [
    path('', views.billing_view, name='billing'),
    path('history/', views.transaction_history, name='transaction_history'),
]
""")

# apps/billing/admin.py
w('apps/billing/admin.py', """from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'credits', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['user__username', 'description']
""")

# apps/core/apps.py
w('apps/core/apps.py', """from django.apps import AppConfig
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
""")

# apps/core/views.py
w('apps/core/views.py', """from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.contacts.models import Contact, ContactGroup
from apps.billing.models import Transaction

@login_required
def dashboard(request):
    user = request.user
    total_sent = CampaignRecipient.objects.filter(campaign__user=user).exclude(status='pending').count()
    delivered = CampaignRecipient.objects.filter(campaign__user=user, status='delivered').count()
    failed = CampaignRecipient.objects.filter(campaign__user=user, status='failed').count()
    balance = user.profile.sms_balance
    recent_campaigns = Campaign.objects.filter(user=user)[:5]
    contact_count = Contact.objects.filter(user=user).count()
    return render(request, 'core/dashboard.html', {
        'total_sent': total_sent, 'delivered': delivered, 'failed': failed,
        'balance': balance, 'recent_campaigns': recent_campaigns, 'contact_count': contact_count,
    })

@login_required
def settings_view(request):
    profile = request.user.profile
    return render(request, 'core/settings.html', {'profile': profile})

@login_required
def quick_send(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        sender_id = request.user.profile.sender_id or 'TextWave'
        if not phone or not message:
            messages.error(request, 'Phone number and message are required.')
            return redirect('core:dashboard')
        balance = request.user.profile.sms_balance
        if balance < 1:
            messages.error(request, 'Insufficient SMS balance.')
            return redirect('core:dashboard')
        from apps.campaigns.models import Campaign, CampaignRecipient
        from apps.campaigns.services import send_campaign
        campaign = Campaign.objects.create(
            name=f'Quick SMS to {phone}', message=message, sender_id=sender_id,
            user=request.user, status='draft'
        )
        CampaignRecipient.objects.create(campaign=campaign, phone_number=phone)
        success, failed = send_campaign(campaign)
        if success:
            messages.success(request, f'SMS sent successfully to {phone}!')
        else:
            messages.error(request, 'Failed to send SMS.')
    return redirect('core:dashboard')
""")

# apps/core/urls.py
w('apps/core/urls.py', """from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('quick-send/', views.quick_send, name='quick_send'),
]
""")

# apps/core/admin.py
w('apps/core/admin.py', 'from django.contrib import admin\n')

# apps/core/management/commands/seed_data.py
w('apps/core/management/commands/seed_data.py', """from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.contacts.models import Contact, ContactGroup
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.billing.models import Transaction

class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@textwave.com', 'admin123')
            admin.first_name = 'Admin'
            admin.last_name = 'User'
            admin.save()
            admin.profile.sms_balance = 10000
            admin.profile.company = 'TextWave Inc'
            admin.profile.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))

        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user('demo', 'demo@textwave.com', 'demo123')
            demo.first_name = 'Demo'
            demo.last_name = 'User'
            demo.save()
            demo.profile.sms_balance = 500
            demo.profile.company = 'Demo Company'
            demo.profile.save()
            self.stdout.write(self.style.SUCCESS('Created demo user (demo/demo123)'))
        else:
            demo = User.objects.get(username='demo')

        group1, _ = ContactGroup.objects.get_or_create(name='Customers', user=demo, defaults={'description': 'Regular customers'})
        group2, _ = ContactGroup.objects.get_or_create(name='VIP', user=demo, defaults={'description': 'VIP clients'})

        contacts_data = [
            ('Alice Johnson', '+1234567890', 'alice@example.com', group1),
            ('Bob Smith', '+1234567891', 'bob@example.com', group1),
            ('Carol Davis', '+1234567892', 'carol@example.com', group2),
            ('David Wilson', '+1234567893', 'david@example.com', group1),
            ('Eve Brown', '+1234567894', 'eve@example.com', group2),
            ('Frank Miller', '+1234567895', 'frank@example.com', group1),
            ('Grace Lee', '+1234567896', 'grace@example.com', group1),
            ('Henry Taylor', '+1234567897', 'henry@example.com', group2),
            ('Iris Anderson', '+1234567898', 'iris@example.com', group1),
            ('Jack Thomas', '+1234567899', 'jack@example.com', group2),
        ]
        for name, phone, email, group in contacts_data:
            Contact.objects.get_or_create(phone=phone, user=demo, defaults={'name': name, 'email': email, 'group': group})

        if Campaign.objects.filter(user=demo).count() < 2:
            c1 = Campaign.objects.create(
                name='Welcome Campaign',
                message='Welcome to our service! Enjoy 10% off your next purchase with code WELCOME10.',
                sender_id='TextWave', status='sent', user=demo
            )
            for contact in Contact.objects.filter(user=demo, group=group1):
                CampaignRecipient.objects.create(campaign=c1, phone_number=contact.phone, status='delivered', message_id='mock_001')

            c2 = Campaign.objects.create(
                name='VIP Offer',
                message='Exclusive VIP offer! Get 20% off all services this weekend.',
                sender_id='TextWave', status='sent', user=demo
            )
            for contact in Contact.objects.filter(user=demo, group=group2):
                CampaignRecipient.objects.create(campaign=c2, phone_number=contact.phone, status='delivered', message_id='mock_002')

            Campaign.objects.create(
                name='Monthly Newsletter',
                message='Hello! Check out our latest updates and new features this month.',
                sender_id='TextWave', status='draft', user=demo
            )

        if Transaction.objects.filter(user=demo).count() < 2:
            Transaction.objects.create(user=demo, amount='8.00', credits=1000, transaction_type='purchase', status='completed', description='Initial credit purchase')
            Transaction.objects.create(user=demo, amount='0.00', credits=-500, transaction_type='deduction', status='completed', description='SMS campaigns')

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully!'))
""")

print("All Python/config files written successfully!")
