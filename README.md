WP to Django Users
==================

Migrating User Authentication from WordPress to Django

John-Michael Oswalt will be covering how he migrated from using WordPress's built-in login system to the user registration and authentication system in Django. This includes User data and hashed passwords, so users did not need to re-register or reset their passwords. Building a user API and updating the PHP app to read from this API using cookies will also be covered.

## The Problem

WordPress Users -> Django Users

You had a small WordPress site with a few users, but now you've grown your user base and the WP authentication system no longer meets your needs.

You've decided to move to Django (or another python framework) and you want to keep all of your users without them being disrupted.

## The Steps to Convert

1. Export the data from WordPress

2. Import the data into Django

3. Update staff and superusers

4. Install python requirements, settings
    
5. Update passwords with Management Command

## 1. Export the data from WordPress

	SELECT id, user_login as username, user_pass as password, display_name as first_name, user_registered as date_joined, "1" as is_active, user_registered as last_login, user_email as email, "0" as is_staff, "0" as is_superuser FROM wp_users
	
This will give you the default columns you need to the User object in auth. Note that the full name is being added to first_name. You may need to clean that up later.

## 2. Import the data into Django

	mysql -u username -p  dbname < path/to/export.sql

Above is a brief example of importing in MySQL. You may have a different data backend or preferred GUI tool to do the import. Either way, you need to get the data from step 1 into the new Django database.

## 3. Update staff and superusers

	UPDATE auth_user SET is_staff = True, is_superuser = True WHERE id in (1, 2, 3, 26, 553)
	
If you know the IDs of your superusers (Admins in WordPress), then you can simply add them here and run this single query.

An alternative option is to JOIN the wp_usermeta table with wp_users and use wp_user_level to establish staff and superusers.

## 4. Install python requirements, settings

	pip install django-hashers-passlib==0.1

And remember to update your `requirements.txt` or similar.

Within your `settings.py` file for your django project, add the following:

	PASSWORD_HASHERS = (
    	'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    	'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    	'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    	'django.contrib.auth.hashers.BCryptPasswordHasher',
    	'django.contrib.auth.hashers.SHA1PasswordHasher',
    	'django.contrib.auth.hashers.MD5PasswordHasher',
    	'django.contrib.auth.hashers.CryptPasswordHasher',
    	'hashers_passlib.phpass',
	)

The last line will add the `phppass` as a valid password hashing option.

## 5. Update passwords with Management Command

    from django.contrib.auth.hashers import get_hasher
    hasher = get_hasher('phpass')
    user.password = hasher.from_orig(user.password)

Then run the command: `python manage.py convert_wp_passwords`

Old: `$P$B8Wa4IPrveTlsVAIPhT5WIot8qfc67/`

New: `phpass$$P$B8Wa4IPrveTlsVAIPhT5WIot8qfc67/`

Django will reformat the password so that it can parse the correct hasher when it attempts to validate a user.

## Stop Here

Some people will be able to stop here. Their users are now migrated and can log in and out of the new site just like the old one. However, if you were using the WP backend to support anything else, you will need to create a replacement in Django.


## Replacing a custom WP user API

We previously had an XML API to read user data out of WordPress from other apps that we have. We now needed to recreate that in Django.

## Replacement Steps

1. Set an apex domain cookie

2. Create a View to display user info

3. Return XML

4. Read XML from other apps


## 1. Set an apex domain cookie

	SESSION_COOKIE_DOMAIN = ".example.com"

Note the leading '.' on the domain name.

You may also want a custom cookie name, which can be set with:

	SESSION_COOKIE_NAME = "mysite_sessionid"

## 2. Add a URL and View for user info

We will need to accept the cookie value as an input in order to send back the correct user info.

See views.py and urls.py

## 3. Return XML

    <?xml version="1.0" encoding="UTF-8"?>
    <user status="{{ requested_user.status }}" username="{{ requested_user.username }}" email="{{ requested_user.email }}" />
    
## 4. Read XML from other apps

The methods to do this will vary from language to language, and if we need any additional info about the user, we can add it to our XML.