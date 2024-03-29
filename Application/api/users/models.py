from categories.models import Ward, HelpType, Requirement
from actions import models as action_models
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.db import models
from model_utils import FieldTracker

from datetime import date

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserRole:
    """Constants used in the User class."""
    COORDINATOR, RESIDENT, VOLUNTEER = '1', '2', '3'
    ROLES = [
        (COORDINATOR, "Coordinator"),
        (RESIDENT, "Resident"),
        (VOLUNTEER, "Volunteer")
    ]


class Person(models.Model):
    """Base class with shared profile attributes."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(
        max_length=15, null=True, blank=True, help_text="Main phone number for the user.")
    phone_secondary = models.CharField(
        max_length=15, null=True, blank=True, help_text="Secondary phone number for the user.")
    email = models.CharField(max_length=50, null=True,
                             blank=True, help_text="Main email for the user.")
    notes = models.TextField(null=True, blank=True,
                             help_text="Any other notes?")

    # Track changes to the model so we can access the previous status
    # when it changes, and propagate those if needed
    tracker = FieldTracker()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        # A bit dirty, but don't know of a quick way to
        # implement some kind of wrapper that passes
        # all calls through just to present Volunteers
        # differently in the AJAX calls from the AutocompleteWidgets
        return getattr(self, 'label', None) or self.full_name


class UserProfileMixin(models.Model):
    """An abstract mixin to add the link to auth.User.

    This ensures each kind of profile has their own attribute,
    enforcing that a user can have only one profile of each kind.

    Note: The addition of the OneToOne field is left to the
    extending class, so that a custom related_name can be set for the relation.
    """

    class Meta:
        abstract = True

    user_without_account = models.BooleanField(
        null=False, default=False, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (not self.user_without_account and not bool(self.user)):
            self.create_user()
        if (self.user_without_account and bool(self.user)):
            self.user = None
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def create_user(self):
        """
        Creates a new User this profile is associated with

        IMPORTANT: Leave password empty as it's what will let
        the password reset form be customized to show a different
        message for the first reset
        """
        user = User(username=self.email, email=self.email,
                    first_name=self.first_name, last_name=self.last_name)
        setattr(user, self.profile_related_name, self)
        user.save()


class Resident(Person):
    """Concrete class for those who need help."""
    address_line_1 = models.CharField(
        max_length=100, help_text="First line of their address.")
    address_line_2 = models.CharField(
        max_length=100, null=True, blank=True, help_text="Second line of their address.")
    address_line_3 = models.CharField(
        max_length=100, null=True, blank=True, help_text="Third line of their address.")
    postcode = models.CharField(max_length=10, help_text="Address postcode.")
    ward = models.ForeignKey(Ward, null=True, on_delete=models.PROTECT,
                             help_text="The ward containing the above address.")
    internet_access = models.BooleanField(
        default=False, help_text="Does this person have internet access?")
    smart_device = models.BooleanField(
        default=False, help_text="Does this person have a smart device?")
    confident_online_shopping = models.BooleanField(
        default=False, help_text="Is this person confident online shopping?")
    confident_online_comms = models.BooleanField(
        default=False, help_text="Is this person confident communicating online?")
    shielded = models.BooleanField(
        default=False, help_text="Is this person shielded?")

    time_received = models.DurationField(null=True, blank=True)

    data_consent_date = models.DateField(null=False, verbose_name="Data agreement date",
                help_text='''When did this person give their consent to keeping their data in ToFro?
                
                <br><br>Before confirming, you must read the agreement to them and receive their explicit verbal consent. Otherwise, their data cannot be stored on this system.''')

    @property
    def address(self, join_char=', '):
        filled_lines = [line for line in (
            self.address_line_1, self.address_line_2, self.address_line_3, self.postcode) if line]
        return join_char.join(filled_lines)

    @property
    def assigned_volunteers(self):
        qs = self.requested_actions.values_list('assigned_volunteers', flat=True).distinct()
        return [pk for pk in qs if pk]


class Volunteer(UserProfileMixin, Person):
    """Concrete class for those who can offer help."""
    profile_related_name = 'volunteer'
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.SET_NULL, related_name=profile_related_name)
    external_volunteer_id = models.CharField(
        max_length=50, null=True, blank=True, help_text="The ID of the volunteer in an external system")
    dbs_number = models.CharField(max_length=12, null=True, blank=True,
                                  help_text="The user's DBS certificate number, if they have one.")
    access_to_car = models.BooleanField(
        null=True, verbose_name="Has access to car")
    driving_license = models.BooleanField(
        null=True, verbose_name="Has a driving license")
    ts_and_cs_confirmed = models.BooleanField(
        null=True, verbose_name="Has agreed to terms and conditions")
    health_checklist_received = models.BooleanField(
        null=True, verbose_name="Has received their health checklist")
    key_worker = models.BooleanField(
        null=True, verbose_name="Has received key worker letter from council")
    id_received = models.BooleanField(
        null=True, verbose_name="Has sent a copy of their ID")
    wards = models.ManyToManyField(Ward, blank=True, related_name="volunteers")
    help_types = models.ManyToManyField(
        HelpType, blank=True, related_name="volunteers")
    requirements = models.ManyToManyField(
        Requirement, blank=True, related_name="volunteers")
    reference_details = models.CharField(max_length=250, null=True, blank=True)

    time_given = models.DurationField(null=True, blank=True)

    available_mon_morning = models.BooleanField(
        default=False, verbose_name="Monday morning")
    available_mon_afternoon = models.BooleanField(
        default=False, verbose_name="Monday afternoon")
    available_mon_evening = models.BooleanField(
        default=False, verbose_name="Monday evening")
    available_tues_morning = models.BooleanField(
        default=False, verbose_name="Tuesday morning")
    available_tues_afternoon = models.BooleanField(
        default=False, verbose_name="Tuesday afternoon")
    available_tues_evening = models.BooleanField(
        default=False, verbose_name="Tuesday evening")
    available_wed_morning = models.BooleanField(
        default=False, verbose_name="Wednesday morning")
    available_wed_afternoon = models.BooleanField(
        default=False, verbose_name="Wednesday afternoon")
    available_wed_evening = models.BooleanField(
        default=False, verbose_name="Wednesday evening")
    available_thur_morning = models.BooleanField(
        default=False, verbose_name="Thursday morning")
    available_thur_afternoon = models.BooleanField(
        default=False, verbose_name="Thursday afternoon")
    available_thur_evening = models.BooleanField(
        default=False, verbose_name="Thursday evening")
    available_fri_morning = models.BooleanField(
        default=False, verbose_name="Friday morning")
    available_fri_afternoon = models.BooleanField(
        default=False, verbose_name="Friday afternoon")
    available_fri_evening = models.BooleanField(
        default=False, verbose_name="Friday evening")
    available_sat_morning = models.BooleanField(
        default=False, verbose_name="Saturday morning")
    available_sat_afternoon = models.BooleanField(
        default=False, verbose_name="Saturday afternoon")
    available_sat_evening = models.BooleanField(
        default=False, verbose_name="Saturday evening")
    available_sun_morning = models.BooleanField(
        default=False, verbose_name="Sunday morning")
    available_sun_afternoon = models.BooleanField(
        default=False, verbose_name="Sunday afternoon")
    available_sun_evening = models.BooleanField(
        default=False, verbose_name="Sunday evening")

    daily_digest_optin = models.BooleanField(default=False, verbose_name="Daily digest opt-in")
    weekly_digest_optin = models.BooleanField(default=False, verbose_name="Weekly digest opt-in")

    @property
    def available_actions(self):
        """The QuerySet for actions available to this volunteer."""

        # Filter for pending actions that can be completed by this volunteer.
        # This is done by counting unfilfilled requirements and removing them from the set.

        # Filter for pending actions.
        # Remove those with unfulfilled user requirements.
        # Filter for actions inside the Volunteer's wards and help_types.
        return action_models.Action.objects \
            .filter(
                Q(action_status=action_models.ActionStatus.PENDING) |
                Q(action_status=action_models.ActionStatus.INTEREST)) \
            .annotate(missed_requirements=Count('requirements',
                                                filter=~Q(requirements__in=self.requirements.all()))) \
            .filter(missed_requirements=0) \
            .annotate(has_volunteered=Count('interested_volunteers',
                                            filter=Q(interested_volunteers__id=self.id))) \
            .filter(has_volunteered=0) \
            .filter(resident__ward__in=self.wards.all()) \
            .filter(help_type__in=self.help_types.all())

    @property
    def upcoming_actions(self):
        # select_related needs to happen here rather
        # than outside of the query due to the `union`
        return self.actions_interested_in.\
            filter(Q(action_status=action_models.ActionStatus.INTEREST) |
                   Q(action_status=action_models.ActionStatus.ASSIGNED, assigned_volunteers=self))

    @property
    def completed_actions(self):
        return self.actions_assigned_to.filter(
            Q(action_status=action_models.ActionStatus.COMPLETED) |
            Q(action_status=action_models.ActionStatus.COULDNT_COMPLETE))
    # FIXED assigned_volunteer

    @property
    def ongoing_actions(self):
        #return self.action_set.filter(action_status=action_models.ActionStatus.ONGOING)
        return self.actions_assigned_to.filter(action_status=action_models.ActionStatus.ONGOING)
    # FIXED assigned_volunteer


class Coordinator(UserProfileMixin, Person):
    profile_related_name = 'coordinator'
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.SET_NULL, related_name=profile_related_name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_creation = not bool(self.pk)

        result = super().save(force_insert=force_insert, force_update=force_update,
                              using=using, update_fields=update_fields)
        if is_creation:
            logger.debug('Adding priviledges to user')
            # Add staff and superuser to
            self.user.is_staff = True
            self.user.is_superuser = True
            self.user.save()

        return result


# Add computed helper properties to the User class.
# Directly accessing `volunteer` or `coordinator` risks raising
# a DoesNotExist error, when we just want a boolean.

@property
def is_volunteer(self):
    return hasattr(self, "volunteer") and self.volunteer


@property
def is_coordinator(self):
    return hasattr(self, "coordinator") and self.coordinator


User.is_volunteer = is_volunteer
User.is_coordinator = is_coordinator


def volunteer_check(user):
    return user.is_volunteer


def coordinator_check(user):
    return user.is_coordinator


class Settings(models.Model):
    """
    A profile to store extra info that's not related to
    the coordination of help
    """
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.CASCADE, related_name='settings')
    terms_accepted_at = models.DateTimeField(null=True, blank=True)

# class Relationship(models.Model):
#     user_1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_1")
#     user_2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_2")
#     created_datetime = models.DateTimeField(default=timezone.now, help_text="When did they first make contact?")

#     def __str__(self):
#         return f"{self.id}: {self.user_1} and {self.user_2}"
