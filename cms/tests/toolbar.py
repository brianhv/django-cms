from __future__ import with_statement
from cms.cms_toolbar import CMSToolbar
from cms.test_utils.testcases import SettingsOverrideTestCase
from cms.test_utils.util.request_factory import RequestFactory
from cms.toolbar.items import (Anchor, TemplateHTML, Switcher, List, ListItem, 
    GetButton)
from django.contrib.auth.models import AnonymousUser, User


class ToolbarTests(SettingsOverrideTestCase):
    settings_overrides = {'CMS_MODERATOR': False}
    
    def setUp(self):
        self.request_factory = RequestFactory()
    
    def get_anon(self):
        return AnonymousUser()
        
    def get_staff(self):
        staff = User(
            username='staff',
            email='staff@staff.org',
            is_active=True,
            is_staff=True,
        )
        staff.set_password('staff')
        staff.save()
        return staff
    
    def get_superuser(self):
        superuser = User(
            username='superuser',
            email='superuser@superuser.org',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        superuser.set_password('superuser')
        superuser.save()
        return superuser
    
    def test_toolbar_no_page_anon(self):
        request = self.request_factory.get('/')
        request.user = self.get_anon()
        request.current_page = None
        toolbar = CMSToolbar()
        items = toolbar.get_items({}, request)
        self.assertEqual(len(items), 2) # Logo + login
        # check the logo is there
        logo = items[0]
        self.assertTrue(isinstance(logo, Anchor))
        # check the login form is there
        login = items[1]
        self.assertTrue(isinstance(login, TemplateHTML))
        self.assertEqual(login.template, 'cms/toolbar/items/login.html')
    
    def test_toolbar_no_page_staff(self):
        request = self.request_factory.get('/')
        request.user = self.get_staff()
        request.current_page = None
        toolbar = CMSToolbar()
        items = toolbar.get_items({}, request)
        self.assertEqual(len(items), 4) # Logo + edit-mode + admin-menu + logout
        # check the logo is there
        logo = items[0]
        self.assertTrue(isinstance(logo, Anchor))
        # check the edit-mode switcher is there and that the switcher is turned off
        edit = items[1]
        self.assertTrue(isinstance(edit, Switcher))
        self.assertFalse(toolbar.edit_mode)
        # check the admin-menu
        admin = items[2]
        self.assertTrue(isinstance(admin, List))
        self.assertEqual(len(admin.raw_items), 1) # only the link to main admin
        self.assertTrue(isinstance(admin.raw_items[0], ListItem))
        # check the logout button
        logout = items[3]
        self.assertTrue(isinstance(logout, GetButton))
        self.assertEqual(logout.url, '?cms-toolbar-logout')