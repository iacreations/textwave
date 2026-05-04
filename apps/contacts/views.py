import csv
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
