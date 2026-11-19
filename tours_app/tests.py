from datetime import date, timedelta
from unittest.mock import patch

from django.core import cache, mail
from django.test import TestCase
from django.urls import reverse

from .models import Departure, Location, Order, Tour


class GuestBookingTests(TestCase):
    def setUp(self):
        cache.cache.clear()
        tour = Tour.objects.create(title="Coast", days=1, location=Location.objects.create(name="Coast"))
        day = date.today() + timedelta(days=1)
        self.departure = Departure.objects.create(tour=tour, start_date=day, end_date=day,
                                                  price=200, total_seats=2, available_seats=2)
        self.fields = {"pax": 1, "contact_email": "guest@example.org",
                       "contact_phone": "0000000000", "contact_name": "Guest"}
        self.search = reverse("booking_search")
        self.checkout = reverse("checkout", args=[self.departure.pk])

    def test_unlisted_tour_cannot_be_booked(self):
        Tour.objects.update(is_active=False)
        self.assertEqual(self.client.post(self.checkout, self.fields).status_code, 404)
        self.assertFalse(Order.objects.exists())
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.available_seats, 2)

    def test_guest_receipt_and_email_lookup(self):
        result = self.client.post(self.checkout, self.fields)
        order = Order.objects.get()
        self.assertEqual(self.client.get(result.url).status_code, 200)
        self.client.logout()
        self.assertEqual(self.client.get(result.url).status_code, 404)
        request = {"order_number": order.order_number}
        self.assertIsNone(self.client.post(self.search, request).context.get("order"))
        self.assertEqual(len(mail.outbox), 0)
        request["contact_email"] = order.contact_email
        self.assertIsNone(self.client.post(self.search, request).context.get("order"))
        code = mail.outbox[0].body.splitlines()[-1]
        self.assertEqual(self.client.post(self.search, {"lookup_code": code}).context["order"], order)
        with patch("django.core.signing.time.time", return_value=4102444800):
            self.assertIsNone(self.client.post(self.search, {"lookup_code": code}).context.get("order"))
