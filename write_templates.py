import os

BASE = '/home/runner/work/textwave/textwave'

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print(f"Written: {path}")

# base.html
w('templates/base.html', """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TextWave{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>
    <div class="d-flex" id="wrapper">
        <nav id="sidebar" class="sidebar">
            <div class="sidebar-brand">
                <i class="bi bi-chat-dots-fill text-white me-2" style="font-size: 1.5rem;"></i>
                <span class="text-white fw-bold fs-4">TextWave</span>
            </div>
            <ul class="sidebar-nav list-unstyled">
                <li>
                    <a href="{% url 'core:dashboard' %}" class="sidebar-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}">
                        <i class="bi bi-speedometer2"></i> Dashboard
                    </a>
                </li>
                <li>
                    <a href="#contactsSubmenu" data-bs-toggle="collapse" class="sidebar-link">
                        <i class="bi bi-people"></i> Contacts <i class="bi bi-chevron-down ms-auto"></i>
                    </a>
                    <ul class="collapse list-unstyled ps-4 {% if request.resolver_match.namespace == 'contacts' %}show{% endif %}" id="contactsSubmenu">
                        <li><a href="{% url 'contacts:contact_list' %}" class="sidebar-link small">All Contacts</a></li>
                        <li><a href="{% url 'contacts:group_list' %}" class="sidebar-link small">Groups</a></li>
                        <li><a href="{% url 'contacts:import_contacts' %}" class="sidebar-link small">Import CSV</a></li>
                    </ul>
                </li>
                <li>
                    <a href="{% url 'campaigns:campaign_list' %}" class="sidebar-link {% if request.resolver_match.namespace == 'campaigns' %}active{% endif %}">
                        <i class="bi bi-megaphone"></i> Campaigns
                    </a>
                </li>
                <li>
                    <a href="{% url 'reports:report_list' %}" class="sidebar-link {% if request.resolver_match.namespace == 'reports' %}active{% endif %}">
                        <i class="bi bi-bar-chart"></i> Reports
                    </a>
                </li>
                <li>
                    <a href="{% url 'billing:billing' %}" class="sidebar-link {% if request.resolver_match.namespace == 'billing' %}active{% endif %}">
                        <i class="bi bi-credit-card"></i> Billing
                    </a>
                </li>
            </ul>
            <div class="sidebar-footer">
                <a href="{% url 'accounts:profile' %}" class="sidebar-link">
                    <i class="bi bi-person-circle"></i> {{ request.user.get_full_name|default:request.user.username }}
                </a>
                <a href="{% url 'accounts:logout' %}" class="sidebar-link" style="color: #ff6b6b;">
                    <i class="bi bi-box-arrow-right"></i> Logout
                </a>
            </div>
        </nav>
        <div id="page-content-wrapper" class="flex-grow-1">
            <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom px-3">
                <button id="menu-toggle" class="btn btn-sm btn-outline-secondary me-3">
                    <i class="bi bi-list"></i>
                </button>
                <span class="navbar-text fw-semibold">{% block page_title %}{% endblock %}</span>
                <div class="ms-auto d-flex align-items-center gap-3">
                    <span class="badge bg-success">
                        <i class="bi bi-phone"></i> {{ request.user.profile.sms_balance }} credits
                    </span>
                    <a href="{% url 'accounts:profile' %}" class="text-decoration-none text-dark">
                        <i class="bi bi-person-circle fs-5"></i>
                    </a>
                </div>
            </nav>
            <div class="container-fluid px-4 mt-3">
                {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                {% endfor %}
            </div>
            <div class="container-fluid px-4 py-3">
                {% block content %}{% endblock %}
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
""")

# accounts/login.html
w('templates/accounts/login.html', """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - TextWave</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; }
        .card { border: none; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .btn-primary { background-color: #39B54B; border-color: #39B54B; }
        .btn-primary:hover { background-color: #2d9140; border-color: #2d9140; }
        .brand-icon { color: #39B54B; }
        a { color: #39B54B; }
        a:hover { color: #2d9140; }
    </style>
</head>
<body class="d-flex align-items-center justify-content-center" style="min-height: 100vh;">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-5 col-lg-4">
                <div class="card p-4">
                    <div class="text-center mb-4">
                        <i class="bi bi-chat-dots-fill brand-icon" style="font-size: 3rem;"></i>
                        <h2 class="fw-bold mt-2" style="color: #39B54B;">TextWave</h2>
                        <p class="text-muted">Bulk SMS Platform</p>
                    </div>
                    {% if form.errors %}
                    <div class="alert alert-danger">Invalid username or password.</div>
                    {% endif %}
                    <form method="post">
                        {% csrf_token %}
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Username</label>
                            {{ form.username }}
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Password</label>
                            {{ form.password }}
                        </div>
                        <div class="d-grid mt-4">
                            <button type="submit" class="btn btn-primary btn-lg">Sign In</button>
                        </div>
                    </form>
                    <div class="text-center mt-3">
                        <small class="text-muted">Don't have an account? <a href="{% url 'accounts:register' %}">Register</a></small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# accounts/register.html
w('templates/accounts/register.html', """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - TextWave</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; }
        .card { border: none; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .btn-primary { background-color: #39B54B; border-color: #39B54B; }
        .btn-primary:hover { background-color: #2d9140; border-color: #2d9140; }
        .brand-icon { color: #39B54B; }
        a { color: #39B54B; }
        a:hover { color: #2d9140; }
    </style>
</head>
<body class="d-flex align-items-center justify-content-center py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
                <div class="card p-4">
                    <div class="text-center mb-4">
                        <i class="bi bi-chat-dots-fill brand-icon" style="font-size: 3rem;"></i>
                        <h2 class="fw-bold mt-2" style="color: #39B54B;">Create Account</h2>
                        <p class="text-muted">Join TextWave today</p>
                    </div>
                    <form method="post">
                        {% csrf_token %}
                        <div class="row">
                            <div class="col-6 mb-3">
                                <label class="form-label fw-semibold">First Name</label>
                                {{ form.first_name }}
                                {% if form.first_name.errors %}<div class="text-danger small">{{ form.first_name.errors }}</div>{% endif %}
                            </div>
                            <div class="col-6 mb-3">
                                <label class="form-label fw-semibold">Last Name</label>
                                {{ form.last_name }}
                                {% if form.last_name.errors %}<div class="text-danger small">{{ form.last_name.errors }}</div>{% endif %}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Username</label>
                            {{ form.username }}
                            {% if form.username.errors %}<div class="text-danger small">{{ form.username.errors }}</div>{% endif %}
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Email</label>
                            {{ form.email }}
                            {% if form.email.errors %}<div class="text-danger small">{{ form.email.errors }}</div>{% endif %}
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Password</label>
                            {{ form.password1 }}
                            {% if form.password1.errors %}<div class="text-danger small">{{ form.password1.errors }}</div>{% endif %}
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Confirm Password</label>
                            {{ form.password2 }}
                            {% if form.password2.errors %}<div class="text-danger small">{{ form.password2.errors }}</div>{% endif %}
                        </div>
                        <div class="d-grid mt-4">
                            <button type="submit" class="btn btn-primary btn-lg">Create Account</button>
                        </div>
                    </form>
                    <div class="text-center mt-3">
                        <small class="text-muted">Already have an account? <a href="{% url 'accounts:login' %}">Sign In</a></small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# accounts/profile.html
w('templates/accounts/profile.html', """{% extends 'base.html' %}
{% block title %}Profile - TextWave{% endblock %}
{% block page_title %}My Profile{% endblock %}
{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card mb-4">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-person-circle text-success"></i>
                <span>Profile Information</span>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-semibold">First Name</label>
                            {{ form.first_name }}
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-semibold">Last Name</label>
                            {{ form.last_name }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Email</label>
                        {{ form.email }}
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Phone</label>
                        {{ form.phone }}
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Company</label>
                        {{ form.company }}
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Default Sender ID <small class="text-muted">(max 11 chars)</small></label>
                        {{ form.sender_id }}
                    </div>
                    <button type="submit" class="btn btn-primary"><i class="bi bi-check2"></i> Save Changes</button>
                    <a href="{% url 'accounts:password_change' %}" class="btn btn-outline-secondary ms-2">
                        <i class="bi bi-lock"></i> Change Password
                    </a>
                </form>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card mb-4">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-phone text-success"></i>
                <span>SMS Balance</span>
            </div>
            <div class="card-body text-center">
                <div class="display-4 fw-bold text-success">{{ request.user.profile.sms_balance }}</div>
                <p class="text-muted">Available Credits</p>
                <a href="{% url 'billing:billing' %}" class="btn btn-success btn-sm">
                    <i class="bi bi-plus-circle"></i> Buy Credits
                </a>
            </div>
        </div>
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-key text-success"></i>
                <span>API Key</span>
            </div>
            <div class="card-body">
                <div class="input-group mb-2">
                    <input type="text" class="form-control form-control-sm font-monospace" id="api-key-value"
                           value="{{ request.user.profile.api_key }}" readonly>
                    <button class="btn btn-outline-secondary btn-sm" id="copy-api-key" type="button">
                        <i class="bi bi-clipboard"></i> Copy
                    </button>
                </div>
                <form method="post" action="{% url 'accounts:regenerate_api_key' %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-outline-warning btn-sm w-100"
                            onclick="return confirm('Regenerate API key? Old key will stop working.')">
                        <i class="bi bi-arrow-repeat"></i> Regenerate Key
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# accounts/password_change.html
w('templates/accounts/password_change.html', """{% extends 'base.html' %}
{% block title %}Change Password - TextWave{% endblock %}
{% block page_title %}Change Password{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-lock text-success"></i>
                <span>Change Password</span>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {% for field in form %}
                    <div class="mb-3">
                        <label class="form-label fw-semibold">{{ field.label }}</label>
                        {{ field }}
                        {% if field.errors %}
                        <div class="text-danger small mt-1">{{ field.errors }}</div>
                        {% endif %}
                    </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-primary"><i class="bi bi-check2"></i> Update Password</button>
                    <a href="{% url 'accounts:profile' %}" class="btn btn-outline-secondary ms-2">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# core/dashboard.html
w('templates/core/dashboard.html', """{% extends 'base.html' %}
{% block title %}Dashboard - TextWave{% endblock %}
{% block page_title %}Dashboard{% endblock %}
{% block content %}
<div class="row g-4 mb-4">
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card">
            <div class="d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(57,181,75,0.15);">
                    <i class="bi bi-send-check" style="color: #39B54B;"></i>
                </div>
                <div>
                    <div class="fs-2 fw-bold">{{ total_sent }}</div>
                    <div class="text-muted small">Total Sent</div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card">
            <div class="d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(13,110,253,0.15);">
                    <i class="bi bi-check2-all" style="color: #0d6efd;"></i>
                </div>
                <div>
                    <div class="fs-2 fw-bold">{{ delivered }}</div>
                    <div class="text-muted small">Delivered</div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card">
            <div class="d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(220,53,69,0.15);">
                    <i class="bi bi-x-circle" style="color: #dc3545;"></i>
                </div>
                <div>
                    <div class="fs-2 fw-bold">{{ failed }}</div>
                    <div class="text-muted small">Failed</div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card">
            <div class="d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(255,193,7,0.15);">
                    <i class="bi bi-credit-card" style="color: #ffc107;"></i>
                </div>
                <div>
                    <div class="fs-2 fw-bold">{{ balance }}</div>
                    <div class="text-muted small">SMS Credits</div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row g-4">
    <div class="col-lg-4">
        <div class="card h-100">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-lightning-charge text-success"></i>
                <span>Quick Send SMS</span>
            </div>
            <div class="card-body">
                <form method="post" action="{% url 'core:quick_send' %}">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Phone Number</label>
                        <input type="text" name="phone" class="form-control" placeholder="+1234567890" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Message</label>
                        <textarea name="message" class="form-control" rows="4" placeholder="Type your message..." required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="bi bi-send"></i> Send SMS
                    </button>
                </form>
            </div>
        </div>
    </div>
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-megaphone text-success"></i>
                    <span>Recent Campaigns</span>
                </div>
                <a href="{% url 'campaigns:campaign_create' %}" class="btn btn-success btn-sm">
                    <i class="bi bi-plus"></i> New Campaign
                </a>
            </div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Campaign</th>
                                <th>Status</th>
                                <th>Recipients</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for campaign in recent_campaigns %}
                            <tr>
                                <td>
                                    <a href="{% url 'campaigns:campaign_detail' campaign.pk %}" class="text-decoration-none fw-semibold">
                                        {{ campaign.name }}
                                    </a>
                                </td>
                                <td>
                                    <span class="badge badge-{{ campaign.status }}">{{ campaign.get_status_display }}</span>
                                </td>
                                <td>{{ campaign.total_recipients }}</td>
                                <td class="text-muted small">{{ campaign.created_at|date:"M d, Y" }}</td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="4" class="text-center text-muted py-4">
                                    No campaigns yet. <a href="{% url 'campaigns:campaign_create' %}">Create one</a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% if recent_campaigns %}
            <div class="card-footer text-end">
                <a href="{% url 'campaigns:campaign_list' %}" class="btn btn-outline-secondary btn-sm">View All</a>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""")

# core/settings.html
w('templates/core/settings.html', """{% extends 'base.html' %}
{% block title %}Settings - TextWave{% endblock %}
{% block page_title %}Settings{% endblock %}
{% block content %}
<div class="row">
    <div class="col-lg-6">
        <div class="card mb-4">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-gear text-success"></i>
                <span>Account Settings</span>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label fw-semibold">Default Sender ID</label>
                    <p class="form-control-plaintext fw-bold">{{ profile.sender_id }}</p>
                    <small class="text-muted">Change in <a href="{% url 'accounts:profile' %}">Profile</a></small>
                </div>
                <hr>
                <div class="mb-3">
                    <label class="form-label fw-semibold">SMS Balance</label>
                    <p class="display-6 fw-bold text-success mb-1">{{ profile.sms_balance }}</p>
                    <p class="text-muted small">Available credits</p>
                    <a href="{% url 'billing:billing' %}" class="btn btn-success btn-sm">
                        <i class="bi bi-plus-circle"></i> Top Up
                    </a>
                </div>
            </div>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-key text-success"></i>
                <span>API Access</span>
            </div>
            <div class="card-body">
                <p class="text-muted small mb-2">Use this key to access the TextWave API programmatically.</p>
                <div class="input-group mb-3">
                    <input type="text" class="form-control font-monospace" id="api-key-value"
                           value="{{ profile.api_key }}" readonly>
                    <button class="btn btn-outline-secondary" id="copy-api-key" type="button">
                        <i class="bi bi-clipboard"></i> Copy
                    </button>
                </div>
                <form method="post" action="{% url 'accounts:regenerate_api_key' %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-outline-warning btn-sm"
                            onclick="return confirm('Regenerate API key? Your old key will stop working immediately.')">
                        <i class="bi bi-arrow-repeat"></i> Regenerate API Key
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# contacts/contact_list.html
w('templates/contacts/contact_list.html', """{% extends 'base.html' %}
{% block title %}Contacts - TextWave{% endblock %}
{% block page_title %}Contacts{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <span class="text-muted">{{ total_count }} contact{{ total_count|pluralize }}</span>
    <div class="d-flex gap-2">
        <a href="{% url 'contacts:import_contacts' %}" class="btn btn-outline-secondary btn-sm">
            <i class="bi bi-upload"></i> Import CSV
        </a>
        <a href="{% url 'contacts:contact_create' %}" class="btn btn-success btn-sm">
            <i class="bi bi-person-plus"></i> Add Contact
        </a>
    </div>
</div>

<div class="card mb-3">
    <div class="card-body py-2">
        <form method="get" class="row g-2 align-items-center">
            <div class="col-md-5">
                <input type="text" name="search" class="form-control form-control-sm"
                       placeholder="Search name, phone, email..." value="{{ search }}">
            </div>
            <div class="col-md-4">
                <select name="group" class="form-select form-select-sm">
                    <option value="">All Groups</option>
                    {% for group in groups %}
                    <option value="{{ group.pk }}" {% if group_filter == group.pk|stringformat:'s' %}selected{% endif %}>
                        {{ group.name }}
                    </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-auto">
                <button type="submit" class="btn btn-primary btn-sm"><i class="bi bi-search"></i> Search</button>
                <a href="{% url 'contacts:contact_list' %}" class="btn btn-outline-secondary btn-sm">Clear</a>
            </div>
        </form>
    </div>
</div>

<div class="card">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Group</th>
                        <th>Added</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for contact in page_obj %}
                    <tr>
                        <td class="fw-semibold">{{ contact.name }}</td>
                        <td>{{ contact.phone }}</td>
                        <td class="text-muted">{{ contact.email|default:"-" }}</td>
                        <td>
                            {% if contact.group %}
                            <span class="badge bg-secondary">{{ contact.group.name }}</span>
                            {% else %}-{% endif %}
                        </td>
                        <td class="text-muted small">{{ contact.created_at|date:"M d, Y" }}</td>
                        <td>
                            <a href="{% url 'contacts:contact_edit' contact.pk %}" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-pencil"></i>
                            </a>
                            <form method="post" action="{% url 'contacts:contact_delete' contact.pk %}" class="d-inline"
                                  onsubmit="return confirm('Delete {{ contact.name }}?')">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-outline-danger btn-sm">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="6" class="text-center text-muted py-5">
                            <i class="bi bi-people fs-1 d-block mb-2"></i>
                            No contacts found.
                            <a href="{% url 'contacts:contact_create' %}">Add your first contact</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% if page_obj.has_other_pages %}
    <div class="card-footer">
        <nav>
            <ul class="pagination pagination-sm mb-0 justify-content-center">
                {% if page_obj.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}&search={{ search }}&group={{ group_filter }}">
                        <i class="bi bi-chevron-left"></i>
                    </a>
                </li>
                {% endif %}
                <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}&search={{ search }}&group={{ group_filter }}">
                        <i class="bi bi-chevron-right"></i>
                    </a>
                </li>
                {% endif %}
            </ul>
        </nav>
    </div>
    {% endif %}
</div>
{% endblock %}
""")

# contacts/contact_form.html
w('templates/contacts/contact_form.html', """{% extends 'base.html' %}
{% block title %}{{ title }} - TextWave{% endblock %}
{% block page_title %}{{ title }}{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-person text-success"></i>
                <span>{{ title }}</span>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {% for field in form %}
                    <div class="mb-3">
                        <label class="form-label fw-semibold">{{ field.label }}</label>
                        {{ field }}
                        {% if field.errors %}<div class="text-danger small">{{ field.errors }}</div>{% endif %}
                        {% if field.help_text %}<div class="text-muted small">{{ field.help_text }}</div>{% endif %}
                    </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-check2"></i> Save Contact
                    </button>
                    <a href="{% url 'contacts:contact_list' %}" class="btn btn-outline-secondary ms-2">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# contacts/group_list.html
w('templates/contacts/group_list.html', """{% extends 'base.html' %}
{% block title %}Groups - TextWave{% endblock %}
{% block page_title %}Contact Groups{% endblock %}
{% block content %}
<div class="d-flex justify-content-end mb-3">
    <a href="{% url 'contacts:group_create' %}" class="btn btn-success btn-sm">
        <i class="bi bi-folder-plus"></i> Create Group
    </a>
</div>
<div class="card">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Contacts</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for group in page_obj %}
                    <tr>
                        <td class="fw-semibold">{{ group.name }}</td>
                        <td class="text-muted">{{ group.description|default:"-" }}</td>
                        <td><span class="badge bg-success">{{ group.contact_count }}</span></td>
                        <td class="text-muted small">{{ group.created_at|date:"M d, Y" }}</td>
                        <td>
                            <a href="{% url 'contacts:group_edit' group.pk %}" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-pencil"></i>
                            </a>
                            <form method="post" action="{% url 'contacts:group_delete' group.pk %}" class="d-inline"
                                  onsubmit="return confirm('Delete group {{ group.name }}?')">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-outline-danger btn-sm">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center text-muted py-5">
                            <i class="bi bi-folder fs-1 d-block mb-2"></i>
                            No groups yet. <a href="{% url 'contacts:group_create' %}">Create one</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% if page_obj.has_other_pages %}
    <div class="card-footer">
        <nav>
            <ul class="pagination pagination-sm mb-0 justify-content-center">
                {% if page_obj.has_previous %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}"><i class="bi bi-chevron-left"></i></a></li>
                {% endif %}
                <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                {% if page_obj.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}"><i class="bi bi-chevron-right"></i></a></li>
                {% endif %}
            </ul>
        </nav>
    </div>
    {% endif %}
</div>
{% endblock %}
""")

# contacts/group_form.html
w('templates/contacts/group_form.html', """{% extends 'base.html' %}
{% block title %}{{ title }} - TextWave{% endblock %}
{% block page_title %}{{ title }}{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-folder text-success"></i>
                <span>{{ title }}</span>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {% for field in form %}
                    <div class="mb-3">
                        <label class="form-label fw-semibold">{{ field.label }}</label>
                        {{ field }}
                        {% if field.errors %}<div class="text-danger small">{{ field.errors }}</div>{% endif %}
                    </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-primary"><i class="bi bi-check2"></i> Save Group</button>
                    <a href="{% url 'contacts:group_list' %}" class="btn btn-outline-secondary ms-2">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# contacts/import_contacts.html
w('templates/contacts/import_contacts.html', """{% extends 'base.html' %}
{% block title %}Import Contacts - TextWave{% endblock %}
{% block page_title %}Import Contacts{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-7">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-upload text-success"></i>
                <span>Upload CSV File</span>
            </div>
            <div class="card-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label fw-semibold">CSV File</label>
                        {{ form.csv_file }}
                        {% if form.csv_file.errors %}<div class="text-danger small">{{ form.csv_file.errors }}</div>{% endif %}
                        <div class="text-muted small mt-1">{{ form.csv_file.help_text }}</div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Assign to Group (optional)</label>
                        {{ form.group }}
                        {% if form.group.errors %}<div class="text-danger small">{{ form.group.errors }}</div>{% endif %}
                    </div>
                    <button type="submit" class="btn btn-success">
                        <i class="bi bi-upload"></i> Import Contacts
                    </button>
                    <a href="{% url 'contacts:contact_list' %}" class="btn btn-outline-secondary ms-2">Cancel</a>
                </form>
            </div>
        </div>
    </div>
    <div class="col-md-5">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-info-circle text-success"></i>
                <span>CSV Format Guide</span>
            </div>
            <div class="card-body">
                <p class="text-muted small">Your CSV file must have the following columns:</p>
                <table class="table table-sm table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th>Column</th>
                            <th>Required</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><code>name</code></td><td><span class="badge bg-danger">Required</span></td></tr>
                        <tr><td><code>phone</code></td><td><span class="badge bg-danger">Required</span></td></tr>
                        <tr><td><code>email</code></td><td><span class="badge bg-secondary">Optional</span></td></tr>
                        <tr><td><code>group</code></td><td><span class="badge bg-secondary">Optional</span></td></tr>
                    </tbody>
                </table>
                <p class="text-muted small mb-1">Example:</p>
                <pre class="bg-light p-2 rounded small">name,phone,email,group
Alice,+1234567890,alice@example.com,Customers
Bob,+1234567891,,VIP</pre>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# campaigns/campaign_list.html
w('templates/campaigns/campaign_list.html', """{% extends 'base.html' %}
{% block title %}Campaigns - TextWave{% endblock %}
{% block page_title %}Campaigns{% endblock %}
{% block content %}
<div class="d-flex justify-content-end mb-3">
    <a href="{% url 'campaigns:campaign_create' %}" class="btn btn-success">
        <i class="bi bi-plus-lg"></i> New Campaign
    </a>
</div>
<div class="card">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Campaign Name</th>
                        <th>Status</th>
                        <th>Recipients</th>
                        <th>Delivered</th>
                        <th>Failed</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for campaign in page_obj %}
                    <tr>
                        <td>
                            <a href="{% url 'campaigns:campaign_detail' campaign.pk %}" class="text-decoration-none fw-semibold">
                                {{ campaign.name }}
                            </a>
                        </td>
                        <td>
                            <span class="badge badge-{{ campaign.status }}">{{ campaign.get_status_display }}</span>
                        </td>
                        <td>{{ campaign.total_recipients }}</td>
                        <td class="text-success">{{ campaign.delivered_count }}</td>
                        <td class="text-danger">{{ campaign.failed_count }}</td>
                        <td class="text-muted small">{{ campaign.created_at|date:"M d, Y" }}</td>
                        <td>
                            <a href="{% url 'campaigns:campaign_detail' campaign.pk %}" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-eye"></i>
                            </a>
                            <form method="post" action="{% url 'campaigns:campaign_delete' campaign.pk %}" class="d-inline"
                                  onsubmit="return confirm('Delete campaign {{ campaign.name }}?')">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-outline-danger btn-sm">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="7" class="text-center text-muted py-5">
                            <i class="bi bi-megaphone fs-1 d-block mb-2"></i>
                            No campaigns yet. <a href="{% url 'campaigns:campaign_create' %}">Create your first campaign</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% if page_obj.has_other_pages %}
    <div class="card-footer">
        <nav>
            <ul class="pagination pagination-sm mb-0 justify-content-center">
                {% if page_obj.has_previous %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}"><i class="bi bi-chevron-left"></i></a></li>
                {% endif %}
                <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                {% if page_obj.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}"><i class="bi bi-chevron-right"></i></a></li>
                {% endif %}
            </ul>
        </nav>
    </div>
    {% endif %}
</div>
{% endblock %}
""")

# campaigns/campaign_form.html
w('templates/campaigns/campaign_form.html', """{% extends 'base.html' %}
{% block title %}New Campaign - TextWave{% endblock %}
{% block page_title %}Create Campaign{% endblock %}
{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-megaphone text-success"></i>
                <span>Campaign Details</span>
            </div>
            <div class="card-body">
                <form method="post" id="campaign-form">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Campaign Name</label>
                        {{ form.name }}
                        {% if form.name.errors %}<div class="text-danger small">{{ form.name.errors }}</div>{% endif %}
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Sender ID <small class="text-muted">(max 11 chars)</small></label>
                        {{ form.sender_id }}
                        {% if form.sender_id.errors %}<div class="text-danger small">{{ form.sender_id.errors }}</div>{% endif %}
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Message</label>
                        {{ form.message }}
                        <div id="char-counter" class="text-muted small mt-1">0 characters | 1 SMS part(s) | 160 remaining</div>
                        {% if form.message.errors %}<div class="text-danger small">{{ form.message.errors }}</div>{% endif %}
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Recipients</label>
                        <div class="d-flex gap-4 mb-2">
                            {% for choice in form.recipient_type %}
                            <div class="form-check">
                                {{ choice.tag }}
                                <label class="form-check-label" for="{{ choice.id_for_label }}">{{ choice.choice_label }}</label>
                            </div>
                            {% endfor %}
                        </div>

                        <div id="groups-section">
                            <div class="border rounded p-3">
                                <label class="form-label fw-semibold small text-muted">SELECT GROUPS</label>
                                {% for choice in form.groups %}
                                <div class="form-check">
                                    {{ choice.tag }}
                                    <label class="form-check-label" for="{{ choice.id_for_label }}">{{ choice.choice_label }}</label>
                                </div>
                                {% endfor %}
                                {% if form.groups.errors %}<div class="text-danger small">{{ form.groups.errors }}</div>{% endif %}
                            </div>
                        </div>

                        <div id="manual-section">
                            {{ form.manual_numbers }}
                            {% if form.manual_numbers.errors %}<div class="text-danger small">{{ form.manual_numbers.errors }}</div>{% endif %}
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Send Options</label>
                        <div class="d-flex gap-4 mb-2">
                            {% for choice in form.send_option %}
                            <div class="form-check">
                                {{ choice.tag }}
                                <label class="form-check-label" for="{{ choice.id_for_label }}">{{ choice.choice_label }}</label>
                            </div>
                            {% endfor %}
                        </div>
                        <div id="schedule-section" style="display:none;">
                            <label class="form-label fw-semibold">Schedule Date & Time</label>
                            <input type="datetime-local" name="scheduled_at" class="form-control">
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-send"></i> Create Campaign
                    </button>
                    <a href="{% url 'campaigns:campaign_list' %}" class="btn btn-outline-secondary ms-2">Cancel</a>
                </form>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-info-circle text-success"></i>
                <span>Tips</span>
            </div>
            <div class="card-body">
                <ul class="list-unstyled text-muted small">
                    <li class="mb-2"><i class="bi bi-check-circle text-success"></i> Keep messages under 160 chars for 1 SMS credit.</li>
                    <li class="mb-2"><i class="bi bi-check-circle text-success"></i> Sender ID can be up to 11 alphanumeric characters.</li>
                    <li class="mb-2"><i class="bi bi-check-circle text-success"></i> Each recipient uses 1 SMS credit.</li>
                    <li><i class="bi bi-check-circle text-success"></i> Current balance:
                        <strong class="text-success">{{ request.user.profile.sms_balance }} credits</strong>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# campaigns/campaign_detail.html
w('templates/campaigns/campaign_detail.html', """{% extends 'base.html' %}
{% block title %}{{ campaign.name }} - TextWave{% endblock %}
{% block page_title %}Campaign Detail{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-start mb-4">
    <div>
        <h4 class="mb-1">{{ campaign.name }}</h4>
        <span class="badge badge-{{ campaign.status }} me-2">{{ campaign.get_status_display }}</span>
        <span class="text-muted small">Created {{ campaign.created_at|date:"M d, Y H:i" }}</span>
    </div>
    <div class="d-flex gap-2">
        {% if campaign.status == 'draft' or campaign.status == 'scheduled' %}
        <form method="post" action="{% url 'campaigns:campaign_send' campaign.pk %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-success"
                    onclick="return confirm('Send this campaign now?')">
                <i class="bi bi-send"></i> Send Now
            </button>
        </form>
        {% endif %}
        <a href="{% url 'campaigns:campaign_list' %}" class="btn btn-outline-secondary">
            <i class="bi bi-arrow-left"></i> Back
        </a>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card text-center">
            <div class="fs-1 fw-bold">{{ stats.total }}</div>
            <div class="text-muted">Total Recipients</div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card text-center">
            <div class="fs-1 fw-bold text-primary">{{ stats.sent }}</div>
            <div class="text-muted">Sent</div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card text-center">
            <div class="fs-1 fw-bold text-success">{{ stats.delivered }}</div>
            <div class="text-muted">Delivered</div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-3">
        <div class="stat-card text-center">
            <div class="fs-1 fw-bold text-danger">{{ stats.failed }}</div>
            <div class="text-muted">Failed</div>
        </div>
    </div>
</div>

<div class="row g-4">
    <div class="col-lg-4">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-chat-text text-success"></i>
                <span>Message</span>
            </div>
            <div class="card-body">
                <p class="mb-2"><strong>Sender:</strong> {{ campaign.sender_id }}</p>
                <div class="bg-light rounded p-3">{{ campaign.message }}</div>
                <div class="text-muted small mt-2">{{ campaign.message|length }} characters</div>
            </div>
        </div>
    </div>
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-people text-success"></i>
                <span>Recipients</span>
            </div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Phone Number</th>
                                <th>Status</th>
                                <th>Message ID</th>
                                <th>Sent At</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for recipient in page_obj %}
                            <tr>
                                <td>{{ recipient.phone_number }}</td>
                                <td>
                                    <span class="badge badge-{{ recipient.status }}">{{ recipient.get_status_display }}</span>
                                </td>
                                <td class="font-monospace small">{{ recipient.message_id|default:"-" }}</td>
                                <td class="text-muted small">{{ recipient.sent_at|date:"M d H:i"|default:"-" }}</td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="4" class="text-center text-muted py-3">No recipients</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% if page_obj.has_other_pages %}
            <div class="card-footer">
                <nav>
                    <ul class="pagination pagination-sm mb-0 justify-content-center">
                        {% if page_obj.has_previous %}
                        <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}"><i class="bi bi-chevron-left"></i></a></li>
                        {% endif %}
                        <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                        {% if page_obj.has_next %}
                        <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}"><i class="bi bi-chevron-right"></i></a></li>
                        {% endif %}
                    </ul>
                </nav>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""")

# reports/report_list.html
w('templates/reports/report_list.html', """{% extends 'base.html' %}
{% block title %}Reports - TextWave{% endblock %}
{% block page_title %}Delivery Reports{% endblock %}
{% block content %}
<div class="row g-3 mb-4">
    <div class="col-sm-6 col-lg">
        <div class="stat-card text-center">
            <div class="fs-2 fw-bold">{{ stats.total }}</div>
            <div class="text-muted small">Total</div>
        </div>
    </div>
    <div class="col-sm-6 col-lg">
        <div class="stat-card text-center">
            <div class="fs-2 fw-bold text-primary">{{ stats.sent }}</div>
            <div class="text-muted small">Sent</div>
        </div>
    </div>
    <div class="col-sm-6 col-lg">
        <div class="stat-card text-center">
            <div class="fs-2 fw-bold text-success">{{ stats.delivered }}</div>
            <div class="text-muted small">Delivered</div>
        </div>
    </div>
    <div class="col-sm-6 col-lg">
        <div class="stat-card text-center">
            <div class="fs-2 fw-bold text-danger">{{ stats.failed }}</div>
            <div class="text-muted small">Failed</div>
        </div>
    </div>
    <div class="col-sm-6 col-lg">
        <div class="stat-card text-center">
            <div class="fs-2 fw-bold text-warning">{{ stats.pending }}</div>
            <div class="text-muted small">Pending</div>
        </div>
    </div>
</div>

<div class="card mb-3">
    <div class="card-body py-2">
        <form method="get" class="row g-2 align-items-center">
            <div class="col-md-4">
                <select name="status" class="form-select form-select-sm">
                    <option value="">All Statuses</option>
                    <option value="sent" {% if status_filter == 'sent' %}selected{% endif %}>Sent</option>
                    <option value="delivered" {% if status_filter == 'delivered' %}selected{% endif %}>Delivered</option>
                    <option value="failed" {% if status_filter == 'failed' %}selected{% endif %}>Failed</option>
                    <option value="pending" {% if status_filter == 'pending' %}selected{% endif %}>Pending</option>
                </select>
            </div>
            <div class="col-md-4">
                <select name="campaign" class="form-select form-select-sm">
                    <option value="">All Campaigns</option>
                    {% for c in campaigns %}
                    <option value="{{ c.pk }}" {% if campaign_filter == c.pk|stringformat:'s' %}selected{% endif %}>
                        {{ c.name }}
                    </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-auto">
                <button type="submit" class="btn btn-primary btn-sm"><i class="bi bi-funnel"></i> Filter</button>
                <a href="{% url 'reports:report_list' %}" class="btn btn-outline-secondary btn-sm">Clear</a>
                <a href="{% url 'reports:export_csv' %}{% if status_filter %}?status={{ status_filter }}{% endif %}"
                   class="btn btn-outline-success btn-sm">
                    <i class="bi bi-download"></i> Export CSV
                </a>
            </div>
        </form>
    </div>
</div>

<div class="card">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Campaign</th>
                        <th>Phone Number</th>
                        <th>Status</th>
                        <th>Message ID</th>
                        <th>Sent At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for record in page_obj %}
                    <tr>
                        <td>
                            <a href="{% url 'campaigns:campaign_detail' record.campaign.pk %}" class="text-decoration-none">
                                {{ record.campaign.name }}
                            </a>
                        </td>
                        <td>{{ record.phone_number }}</td>
                        <td>
                            <span class="badge badge-{{ record.status }}">{{ record.get_status_display }}</span>
                        </td>
                        <td class="font-monospace small">{{ record.message_id|default:"-" }}</td>
                        <td class="text-muted small">{{ record.sent_at|date:"M d, Y H:i"|default:"-" }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center text-muted py-5">
                            <i class="bi bi-bar-chart fs-1 d-block mb-2"></i>
                            No records found.
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% if page_obj.has_other_pages %}
    <div class="card-footer">
        <nav>
            <ul class="pagination pagination-sm mb-0 justify-content-center">
                {% if page_obj.has_previous %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&status={{ status_filter }}&campaign={{ campaign_filter }}"><i class="bi bi-chevron-left"></i></a></li>
                {% endif %}
                <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                {% if page_obj.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&status={{ status_filter }}&campaign={{ campaign_filter }}"><i class="bi bi-chevron-right"></i></a></li>
                {% endif %}
            </ul>
        </nav>
    </div>
    {% endif %}
</div>
{% endblock %}
""")

# billing/billing.html
w('templates/billing/billing.html', """{% extends 'base.html' %}
{% block title %}Billing - TextWave{% endblock %}
{% block page_title %}Billing & Credits{% endblock %}
{% block content %}
<div class="row g-4">
    <div class="col-lg-7">
        <div class="card mb-4">
            <div class="card-header d-flex align-items-center gap-2">
                <i class="bi bi-cart text-success"></i>
                <span>Purchase SMS Credits</span>
            </div>
            <div class="card-body">
                <div class="text-center mb-4 py-3" style="background: linear-gradient(135deg, #39B54B, #2d9140); border-radius: 12px; color: white;">
                    <div class="display-4 fw-bold">{{ request.user.profile.sms_balance }}</div>
                    <div>Available Credits</div>
                </div>
                <form method="post">
                    {% csrf_token %}
                    <h6 class="fw-semibold mb-3">Select Package</h6>
                    <div class="row g-3 mb-4">
                        {% for value, label in packages %}
                        <div class="col-6">
                            <div class="border rounded p-3 text-center package-option" style="cursor: pointer;">
                                <div class="form-check d-flex justify-content-center">
                                    <input class="form-check-input me-2" type="radio" name="package" value="{{ value }}"
                                           id="pkg_{{ value }}" {% if forloop.first %}checked{% endif %}>
                                    <label class="form-check-label fw-semibold" for="pkg_{{ value }}">{{ label }}</label>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Payment Method</label>
                        {{ form.payment_method }}
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Card Number (demo)</label>
                        {{ form.card_number }}
                    </div>
                    <button type="submit" class="btn btn-success btn-lg w-100">
                        <i class="bi bi-credit-card"></i> Purchase Credits
                    </button>
                    <p class="text-center text-muted small mt-2">
                        <i class="bi bi-shield-check"></i> This is a demo — no real payment is processed.
                    </p>
                </form>
            </div>
        </div>
    </div>
    <div class="col-lg-5">
        <div class="card">
            <div class="card-header d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-clock-history text-success"></i>
                    <span>Recent Transactions</span>
                </div>
                <a href="{% url 'billing:transaction_history' %}" class="btn btn-outline-secondary btn-sm">View All</a>
            </div>
            <div class="card-body p-0">
                <div class="list-group list-group-flush">
                    {% for tx in recent_transactions %}
                    <div class="list-group-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <div class="fw-semibold small">{{ tx.description }}</div>
                                <div class="text-muted" style="font-size: 0.75rem;">{{ tx.created_at|date:"M d, Y H:i" }}</div>
                            </div>
                            <div class="text-end">
                                <span class="fw-bold {% if tx.credits > 0 %}text-success{% else %}text-danger{% endif %}">
                                    {% if tx.credits > 0 %}+{% endif %}{{ tx.credits }}
                                </span>
                                <div class="text-muted" style="font-size: 0.75rem;">credits</div>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <div class="list-group-item text-center text-muted py-4">No transactions yet</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# billing/transaction_history.html
w('templates/billing/transaction_history.html', """{% extends 'base.html' %}
{% block title %}Transaction History - TextWave{% endblock %}
{% block page_title %}Transaction History{% endblock %}
{% block content %}
<div class="card">
    <div class="card-header d-flex align-items-center gap-2">
        <i class="bi bi-receipt text-success"></i>
        <span>All Transactions</span>
    </div>
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Description</th>
                        <th>Type</th>
                        <th>Credits</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for tx in page_obj %}
                    <tr>
                        <td>{{ tx.description }}</td>
                        <td><span class="badge bg-secondary">{{ tx.get_transaction_type_display }}</span></td>
                        <td>
                            <span class="fw-bold {% if tx.credits > 0 %}text-success{% else %}text-danger{% endif %}">
                                {% if tx.credits > 0 %}+{% endif %}{{ tx.credits }}
                            </span>
                        </td>
                        <td>${{ tx.amount }}</td>
                        <td>
                            {% if tx.status == 'completed' %}
                            <span class="badge bg-success">Completed</span>
                            {% elif tx.status == 'pending' %}
                            <span class="badge bg-warning text-dark">Pending</span>
                            {% else %}
                            <span class="badge bg-danger">Failed</span>
                            {% endif %}
                        </td>
                        <td class="text-muted small">{{ tx.created_at|date:"M d, Y H:i" }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="6" class="text-center text-muted py-5">
                            <i class="bi bi-receipt fs-1 d-block mb-2"></i>
                            No transactions yet.
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% if page_obj.has_other_pages %}
    <div class="card-footer">
        <nav>
            <ul class="pagination pagination-sm mb-0 justify-content-center">
                {% if page_obj.has_previous %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}"><i class="bi bi-chevron-left"></i></a></li>
                {% endif %}
                <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                {% if page_obj.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}"><i class="bi bi-chevron-right"></i></a></li>
                {% endif %}
            </ul>
        </nav>
    </div>
    {% endif %}
</div>
{% endblock %}
""")

# CSS
w('static/css/main.css', """:root {
    --primary: #39B54B;
    --primary-dark: #2d9140;
    --sidebar-bg: #1a1a2e;
    --sidebar-width: 250px;
}

body {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

#sidebar {
    min-height: 100vh;
    width: var(--sidebar-width);
    background: var(--sidebar-bg);
    transition: all 0.3s;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}

#sidebar.collapsed {
    width: 0;
    overflow: hidden;
}

.sidebar-brand {
    padding: 1.5rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
}

.sidebar-nav {
    padding: 1rem 0;
    flex: 1;
}

.sidebar-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.25rem;
    color: rgba(255,255,255,0.75);
    text-decoration: none;
    transition: all 0.2s;
}

.sidebar-link:hover, .sidebar-link.active {
    color: #fff;
    background: rgba(57,181,75,0.2);
    border-left: 3px solid var(--primary);
}

.sidebar-link i {
    width: 20px;
    text-align: center;
}

.sidebar-footer {
    padding: 1rem 0;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.stat-card {
    background: #fff;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 15px rgba(0,0,0,0.07);
    transition: transform 0.2s;
    border: none;
}

.stat-card:hover {
    transform: translateY(-3px);
}

.stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.navbar {
    position: sticky;
    top: 0;
    z-index: 100;
}

#page-content-wrapper {
    min-height: 100vh;
    overflow-x: hidden;
}

.btn-primary {
    background-color: var(--primary);
    border-color: var(--primary);
}
.btn-primary:hover, .btn-primary:focus {
    background-color: var(--primary-dark);
    border-color: var(--primary-dark);
}

.btn-success {
    background-color: var(--primary);
    border-color: var(--primary);
}
.btn-success:hover, .btn-success:focus {
    background-color: var(--primary-dark);
    border-color: var(--primary-dark);
}

.badge.bg-success {
    background-color: var(--primary) !important;
}

.text-success {
    color: var(--primary) !important;
}

.table th {
    font-weight: 600;
    color: #495057;
    background-color: #f8f9fa;
}

.card {
    border: none;
    border-radius: 12px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.07);
}

.card-header {
    background: #fff;
    border-bottom: 1px solid #e9ecef;
    font-weight: 600;
    border-radius: 12px 12px 0 0 !important;
}

.badge-draft { background-color: #6c757d; }
.badge-scheduled { background-color: #0d6efd; }
.badge-sending { background-color: #ffc107; color: #000; }
.badge-sent { background-color: #198754; }
.badge-failed { background-color: #dc3545; }
.badge-pending { background-color: #6c757d; }
.badge-delivered { background-color: #198754; }

.alert-error { background-color: #f8d7da; border-color: #f5c2c7; color: #842029; }

@media (max-width: 768px) {
    #sidebar {
        position: fixed;
        z-index: 1000;
        left: -250px;
    }
    #sidebar.show {
        left: 0;
    }
}
""")

# JS
w('static/js/main.js', """document.addEventListener('DOMContentLoaded', function() {
    // SMS character counter
    const textarea = document.getElementById('message-textarea');
    if (textarea) {
        const counter = document.getElementById('char-counter');
        function updateCounter() {
            const len = textarea.value.length;
            const parts = len === 0 ? 1 : Math.ceil(len / 160);
            const remaining = parts * 160 - len;
            if (counter) {
                counter.textContent = len + ' characters | ' + parts + ' SMS part(s) | ' + remaining + ' remaining';
            }
        }
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }

    // Recipient type toggle
    const recipientRadios = document.querySelectorAll('input[name="recipient_type"]');
    const groupsSection = document.getElementById('groups-section');
    const manualSection = document.getElementById('manual-section');
    if (recipientRadios.length) {
        function toggleRecipients() {
            const val = document.querySelector('input[name="recipient_type"]:checked');
            if (val) {
                if (groupsSection) groupsSection.style.display = val.value === 'groups' ? 'block' : 'none';
                if (manualSection) manualSection.style.display = val.value === 'manual' ? 'block' : 'none';
            }
        }
        recipientRadios.forEach(r => r.addEventListener('change', toggleRecipients));
        toggleRecipients();
    }

    // Send option toggle
    const sendRadios = document.querySelectorAll('input[name="send_option"]');
    const scheduleSection = document.getElementById('schedule-section');
    if (sendRadios.length) {
        function toggleSendOption() {
            const val = document.querySelector('input[name="send_option"]:checked');
            if (val && scheduleSection) {
                scheduleSection.style.display = val.value === 'schedule' ? 'block' : 'none';
            }
        }
        sendRadios.forEach(r => r.addEventListener('change', toggleSendOption));
        toggleSendOption();
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        });
    }, 5000);

    // Sidebar toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Copy API key
    const copyBtn = document.getElementById('copy-api-key');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const apiKey = document.getElementById('api-key-value');
            if (apiKey) {
                navigator.clipboard.writeText(apiKey.value || apiKey.textContent.trim()).then(function() {
                    copyBtn.innerHTML = '<i class="bi bi-check"></i> Copied!';
                    setTimeout(function() {
                        copyBtn.innerHTML = '<i class="bi bi-clipboard"></i> Copy';
                    }, 2000);
                });
            }
        });
    }
});
""")

print("All template and static files written successfully!")
