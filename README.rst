django-allauth-keycloak-ext
==============================

django-allauth-keycloak-ext is a Python package that extends Django-allauth to support security groups configured in Keycloak.

Features
--------

- Supports adding/removing users from Django groups mapped to Keycloak groups during login procedure.
- Supports mapping Keycloak groups to is_staff and is_superuser flags of Django users.

Installation
------------

To install django-allauth-keycloak-ext, run the following command:

.. code-block:: bash

    pip install django-allauth-keycloak-ext

Usage
-----

Once you have installed django-allauth-keycloak-ext, you can use it in your Django project by following these steps:

1. Add `'allauth_keycloak_groups'` to your `INSTALLED_APPS` setting:

   .. code-block:: python

       INSTALLED_APPS = [
           # ...
           'allauth_keycloak_ext',
           # ...
       ]

2. Configure Django-allauth to use Keycloak Ext as a provider by adding the following settings to your `settings.py` file:

   .. code-block:: python

        SOCIALACCOUNT_PROVIDERS = {
            "keycloak_ext": {
                "KEYCLOAK_URL": "http://localhost:8080",
                "KEYCLOAK_REALM": "master",
                "GROUPS": {
                    "GROUP_TO_FLAG_MAPPING": {
                        "is_staff": ["Django Staff", "django-admin-role"],
                        "is_superuser": "django-admin-role",
                    },
                }
            }
        }

3. Configure the security groups you want to use in Keycloak and map them to Django groups in your `settings.py` file:

   .. code-block:: python

       ALLAUTH_KEYCLOAK_GROUPS = {
           'group-name-1': 'django-group-name-1',
           'group-name-2': 'django-group-name-2',
           # ...
       }

   Note that the keys of the `ALLAUTH_KEYCLOAK_GROUPS` dictionary should be the names of the security groups you have configured in Keycloak, and the values should be the names of the Django groups you want to map them to.

License
-------

This package is released under the MIT License.

Contributing
------------

Contributions to this project are welcome. Please submit bug reports