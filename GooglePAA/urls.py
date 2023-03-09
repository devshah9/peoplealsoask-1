"""GooglePAA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import scraperFront
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('people-also-ask', scraperFront, name='peopleAlsoAsk'),
    path('api/search/', views.searchUsingKeyWord, name='searchUsingKeyWord'),
    path('api/', views.scrappingApi, name='scrappingApi')
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# Create ORM models and functions to manage users and devices in tenants. These models will be used in application where users and devices are grouped by tenants and cannot be accessed between them. Users can have multiple devices and device can be owned by multiple users.
# Requirements


# Define table names:

# Tenant model table should be named tenants.
# User model table should be named users.
# Device model table should be named devices.


# Define a Tenant model with the following properties:

# id (primary key, integer);
# name (string: 30 characters, non-null).


# Define a User model with the following properties:

# id (primary key, integer);
# username (string: 30 characters, non-null);
# password (string: 100 characters, non-null);
# first_name (string: 40 characters, may be null);
# last_name (string: 50 characters, may be null).


# Define a Device model with the following properties:

# id (primary key, integer);
# ip_address (string: 16 characters, non-null);
# description (text, may be null).


# Connect User to Tenant with a Many-to-One relationship (one tenant can have many users):

# Create a tenant field in the User model;
# Create a users array in the Tenant model.


# Connect Device to User with a Many-to-Many relationship (use an association table):

# Create a devices array in the User model;
# Create a users array in the Device model.


# Define constructors:

# for Tenant, which accepts name as a required parameter;
# for User, which accepts username, password as required parameters and first_name, last_name as optional parameters;
# for Device, which accepts ip_address as a required parameter and description as an optional parameter.


# Define proper equality operators to compare the primary keys of given instances (if objects are of the same type and their primary keys are equal then the instances are equal).


# Implement password hashing for the User model. Use bcrypt with salt set to b'$2b$12$CodilityIsSuperFunToDo'.


# Additional class methods:

# Implement a Device method grant_permission(self, session, user) which connects the given user with a device.
# Implement a User method assign_to_tenant(self, session, tenant) which assigns the given tenant to a user.
# Every additional class method should accept session as the second parameter (after self) and use that to save the changes made on the objects. See Example 1.

# Hints

# Use Base as the base class for all the models.
# Use __tablename__ to specify the table name.
# Assumptions

# You don't need to save any objects created with the constructor; assume that the creator will persist those objects.
# Available packages/libraries

# Python 3.8.5
# SQLAlchemy 1.3.23
# bcrypt 3.2.0
# Examples


# Example 1 (every action class method should accept session as the second parameter):
# class Device(Base):

#     def some_action(self, session, some_parameter):
#         # some actions...


# The diagram for this relations look like the following:
