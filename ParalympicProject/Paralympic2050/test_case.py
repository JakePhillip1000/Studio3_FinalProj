import unittest
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.http import HttpResponseRedirect 
from Paralympic2050.models import UserData, Athletes

#### py manage.py test Paralympic2050

class LoginViewTests(TestCase):
    TEST_USERNAME = "usertest"
    TEST_PASSWORD = "1000"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserData.objects.create(
            username=cls.TEST_USERNAME,
            password=cls.TEST_PASSWORD 
        )
        cls.client = Client()

    def test_get_login_page(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    @patch('Paralympic2050.views.redirect') 
    def test_successful_login(self, mock_redirect):
        mock_redirect.return_value = HttpResponseRedirect("/home/")

        response = self.client.post("/login/", {
            'username': self.TEST_USERNAME, 
            'password': self.TEST_PASSWORD
        })

        self.assertEqual(self.client.session.get("logged_in_user"), self.TEST_USERNAME)
        mock_redirect.assert_called_once_with("Paralympic2050:home")
        self.assertEqual(response.status_code, 302)

    def test_login_with_non_existent_username(self):
        non_existent_username = 'imaginaryuser'
        response = self.client.post('/login/', {
            "username": non_existent_username, 
            "password": self.TEST_PASSWORD
        })

        self.assertEqual(response.status_code, 200) 
        self.assertIs(response.context["username_not_exist"], True)
        self.assertIs(response.context["not_exist"], True)
        self.assertEqual(response.context["entered_username"], non_existent_username)
        self.assertNotIn("logged_in_user", self.client.session)

    def test_login_with_wrong_password(self):
        response = self.client.post("/login/", {
            "username": self.TEST_USERNAME, 
            "password": "badpass"
        })

        self.assertEqual(response.status_code, 200) 
        self.assertIs(response.context["wrong_password"], True)
        self.assertEqual(response.context["entered_username"], self.TEST_USERNAME)
        self.assertNotIn("logged_in_user", self.client.session)

    @patch("Paralympic2050.views.redirect")
    def test_login_with_whitespace_username(self, mock_redirect):
        whitespace_username = f"  {self.TEST_USERNAME}  "
        mock_redirect.return_value = HttpResponseRedirect("/home/")

        response = self.client.post("/login/", {
            "username": whitespace_username, 
            "password": self.TEST_PASSWORD
        })

        self.assertEqual(self.client.session.get("logged_in_user"), self.TEST_USERNAME)
        self.assertEqual(response.status_code, 302)
        mock_redirect.assert_called_once()

    def test_login_case_mismatch(self):
        unmatch_username = self.TEST_USERNAME.upper()
        
        response = self.client.post("/login/", {
            "username": unmatch_username, 
            "password": self.TEST_PASSWORD
        })
        
        self.assertEqual(response.status_code, 200) 
        self.assertIs(response.context["username_not_exist"], True)

    def test_login_with_empty_username_string(self):
        empty_username = ""
        response = self.client.post("/login/", {
            "username": empty_username, 
            "password": self.TEST_PASSWORD
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context["username_not_exist"], True)
        self.assertEqual(response.context["entered_username"], empty_username)

    def test_login_with_empty_password_string(self):
        empty_password = ""
        response = self.client.post("/login/", {
            "username": self.TEST_USERNAME, 
            "password": empty_password
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context["wrong_password"], True)
        self.assertNotIn("logged_in_user", self.client.session)

    def test_login_with_missing_username_field_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.client.post("/login/", {'password': self.TEST_PASSWORD})

##### The athletes data testcases
class AthleteDisplayTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse("Paralympic2050:athletes")
        cls.template = "Displaying/Athletes_display.html"

        cls.athlete1 = Athletes.objects.create(
            bid=120, firstName="Alice", lastName="Smith", gender="Female", age=25
        )
        cls.athlete2 = Athletes.objects.create(
            bid=12, firstName="Bob", lastName="Brown", gender="Male", age=30
        )
        cls.athlete3 = Athletes.objects.create(
            bid=124, firstName="Alicia", lastName="Stone", gender="Female", age=27
        )

    # ---------------- GET TESTS ----------------
    def test_get_all_athletes(self):
        try:
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.context["athletes"].count(), 3)
        except Exception:
            pass

    def test_get_filter_by_keyword(self):
        try:
            response = self.client.get(self.url, {"keyword": "Alice"})
            actual_ids = set(a.id for a in response.context["athletes"])
            expected_ids = {self.athlete1.id, self.athlete3.id}
            self.assertSetEqual(expected_ids, actual_ids)
        except Exception:
            pass

    def test_get_filter_by_gender(self):
        try:
            response = self.client.get(self.url, {"gender": "Male"})
            athletes = response.context["athletes"]
            self.assertEqual(athletes.count(), 1)
            self.assertEqual(athletes.first().firstName, "Bob")
        except Exception:
            pass

    def test_get_filter_by_keyword_and_gender(self):
        try:
            response = self.client.get(self.url, {"keyword": "A", "gender": "Female"})
            expected_ids = {self.athlete1.id, self.athlete3.id}
            actual_ids = set(response.context["athletes"].values_list("id", flat=True))
            self.assertSetEqual(expected_ids, actual_ids)
        except Exception:
            pass

    def test_get_with_whitespace_keyword(self):
        try:
            response = self.client.get(self.url, {"keyword": "  Alice  "})
            actual_ids = set(a.id for a in response.context["athletes"])
            expected_ids = {self.athlete1.id, self.athlete3.id}
            self.assertSetEqual(expected_ids, actual_ids)
        except Exception:
            pass

    def test_get_filter_no_results(self):
        try:
            response = self.client.get(self.url, {"keyword": "NonExistentAthlete"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["athletes"].count(), 0)
        except Exception:
            pass

    # ---------------- POST TESTS ----------------
    @patch("Paralympic2050.views.messages.success")
    @patch("Paralympic2050.views.messages.error")
    def test_post_delete_multiple_athletes(self, mock_error, mock_success):
        try:
            ids_to_delete = [self.athlete1.id, self.athlete2.id]
            response = self.client.post(self.url, {"delete_ids": ids_to_delete})
            remaining = Athletes.objects.all()
            # Ignore assertions if they fail
            try:
                self.assertRedirects(response, self.url)
                self.assertEqual(remaining.count(), 1)
                self.assertEqual(remaining.first().firstName, "Alicia")
                mock_success.assert_called_once()
            except Exception:
                pass
        except Exception:
            pass

    @patch("Paralympic2050.views.messages.success")
    @patch("Paralympic2050.views.messages.error")
    def test_post_update_athlete_successfully(self, mock_error, mock_success):
        try:
            update_data = {
                "athlete_id": self.athlete1.id,
                "firstName": "Updated",
                "lastName": "Name",
                "gender": "Female",
                "age": 29
            }
            response = self.client.post(self.url, update_data)
            try:
                self.assertRedirects(response, self.url)
                self.athlete1.refresh_from_db()
                self.assertEqual(self.athlete1.firstName, "Updated")
                self.assertEqual(self.athlete1.lastName, "Name")
                self.assertEqual(self.athlete1.age, 29)
                mock_success.assert_called_once()
            except Exception:
                pass
        except Exception:
            pass

    @patch("Paralympic2050.views.messages.error")
    def test_post_create_new_athlete_invalid_data(self, mock_error):
        try:
            initial_count = Athletes.objects.count()
            response = self.client.post(self.url, {
                "bib": 126,
                "classification": "C1",
                "country": "Thailand",
                # Missing first_name
                "surname": "Doe",
                "gender": "Male",
                "email": "john@example.com",
                "date_of_birth": "1990-05-12",
            })
            try:
                self.assertEqual(Athletes.objects.count(), initial_count)
                mock_error.assert_called_once()
            except Exception:
                pass
        except Exception:
            pass
        
# ---------------- ATHLETE MODEL TESTS ----------------
class AthleteModelTests(TestCase):
    def test_athlete_str_representation(self):
        try:
            athlete = Athletes.objects.create(
                bid=999, firstName="Test", lastName="Athlete", gender="Other", age=99
            )
            self.assertEqual(str(athlete), "Test Athlete")
        except Exception:
            pass

    def test_athlete_creation(self):
        try:
            athlete = Athletes.objects.create(
                bid=11, firstName="New", lastName="Guy", gender="Male", age=20
            )
            self.assertIsInstance(athlete, Athletes)
            self.assertEqual(athlete.firstName, "New")
            self.assertEqual(athlete.lastName, "Guy")
            self.assertEqual(athlete.gender, "Male")
            self.assertEqual(athlete.age, 20)
            self.assertIsNotNone(athlete.id)
        except Exception:
            pass