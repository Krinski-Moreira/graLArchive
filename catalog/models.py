from django.db import models

# Create your models here.

from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.template.defaultfilters import slugify

class Boolean_class(models.TextChoices):
        TRUE = "TRUE"
        FALSE = "FALSE"
class Lens(models.Model):

    Name = models.CharField(max_length=30)
    Type = models.CharField(max_length=10)
    source_id_DR3 = models.BigIntegerField(null=True, blank=True)
    gravLensName = models.CharField(max_length=30, null=True, blank=True)
    compId = models.SmallIntegerField(null=True, blank=True)
    Max_separation = models.FloatField(null=True, blank=True)
    Nb_of_published_components = models.SmallIntegerField(null=True, blank=True)
    BibCode = models.CharField(max_length=30, null=True, blank=True)
    RA_center = models.FloatField(null=True, blank=True, help_text='RA center [°]')
    DEC_center = models.FloatField(null=True, blank=True, help_text='DEC center [°]')
    RA_center_sexa = models.CharField(max_length=30, null=True, blank=True, help_text='RA center [d:mm:ss.ss]')
    DEC_center_sexa = models.CharField(max_length=30, null=True, blank=True, help_text='DEC center [d:mm:ss.ss]')
    z_source = models.FloatField(null=True, blank=True, help_text='z source')
    z_lens = models.FloatField(null=True, blank=True, help_text='z lens')
    z_bibcode = models.CharField(max_length=30, null=True, blank=True, help_text='z bibcode')

    def __str__(self):
        return self.Name
    
    def slug(self):
         return slugify(self.Name)

    def get_absolute_url(self):
        return reverse('lens-name', args=[str(self.Name)])

class LensComponent(models.Model):
    Name = models.ForeignKey(Lens, on_delete=models.CASCADE)
    Component = models.CharField(max_length=30)
    RA_best = models.FloatField(null=True, blank=True, help_text='RA best [°]')
    DEC_best = models.FloatField(null=True, blank=True, help_text='DEC best [°]')
    RA_sexa = models.CharField(max_length=30, null=True, blank=True, help_text='RA best [d:mm:ss.ss]')
    DEC_sexa = models.CharField(max_length=30, null=True, blank=True, help_text='DEC best [d:mm:ss.ss]')
    DR3 = models.CharField(max_length=5, choices=Boolean_class.choices, blank=False)
    FPR = models.CharField(max_length=5, choices=Boolean_class.choices, blank=False)
    RA_pub = models.FloatField(null=True, blank=True)
    DEC_pub = models.FloatField(null=True, blank=True)
    ra_Gaia_DR3 = models.FloatField(null=True, blank=True)
    ra_error = models.FloatField(null=True, blank=True)
    dec_Gaia_DR3 = models.FloatField(null=True, blank=True)
    dec_error = models.FloatField(null=True, blank=True)
    parallax = models.FloatField(null=True, blank=True)
    parallax_error = models.FloatField(null=True, blank=True)
    parallax_over_error = models.FloatField(null=True, blank=True)
    pm = models.FloatField(null=True, blank=True)
    pmra = models.FloatField(null=True, blank=True)
    pmra_error = models.FloatField(null=True, blank=True)
    pmdec = models.FloatField(null=True, blank=True)
    pmdec_error = models.FloatField(null=True, blank=True)
    astrometric_n_good_obs_al = models.SmallIntegerField(null=True, blank=True)
    astrometric_gof_al = models.FloatField(null=True, blank=True)
    astrometric_chi2_al = models.FloatField(null=True, blank=True)
    astrometric_excess_noise = models.FloatField(null=True, blank=True)
    astrometric_excess_noise_sig = models.FloatField(null=True, blank=True)
    astrometric_params_solved = models.SmallIntegerField(null=True, blank=True)
    pseudocolour = models.FloatField(null=True, blank=True)
    pseudocolour_error = models.FloatField(null=True, blank=True)
    visibility_periods_used = models.SmallIntegerField(null=True, blank=True)
    ruwe = models.FloatField(null=True, blank=True)
    duplicated_source = models.CharField(max_length=5, choices=Boolean_class.choices, blank=False)
    phot_g_mean_flux = models.FloatField(null=True, blank=True)
    phot_g_mean_flux_error = models.FloatField(null=True, blank=True)
    phot_g_mean_mag = models.FloatField(null=True, blank=True)
    phot_bp_mean_flux = models.FloatField(null=True, blank=True)
    phot_bp_mean_flux_error = models.FloatField(null=True, blank=True)
    phot_bp_mean_mag = models.FloatField(null=True, blank=True)
    phot_rp_mean_flux = models.FloatField(null=True, blank=True)
    phot_rp_mean_mag = models.FloatField(null=True, blank=True)
    bp_rp = models.FloatField(null=True, blank=True)
    phot_g_mean_mag_error = models.FloatField(null=True, blank=True)
    phot_bp_mean_mag_error = models.FloatField(null=True, blank=True)
    phot_rp_mean_mag_error = models.FloatField(null=True, blank=True)
    #phot_g_mean_mag_corrected = models.FloatField(null=True, blank=True)
    #phot_g_mean_mag_error_corrected = models.FloatField(null=True, blank=True)
    #phot_g_mean_flux_corrected = models.FloatField(null=True, blank=True)
    nObsComp = models.SmallIntegerField(null=True, blank=True)
    ra_FPR = models.FloatField(null=True, blank=True)
    stdra_FPR = models.FloatField(null=True, blank=True)
    dec_FPR = models.FloatField(null=True, blank=True)
    stddec_FPR = models.FloatField(null=True, blank=True)
    G_FPR = models.FloatField(null=True, blank=True)
    stdG_FPR = models.FloatField(null=True, blank=True)
    #nbNeighors = models.SmallIntegerField(null=True, blank=True)
    z_milli = models.FloatField(null=True, blank=True)
    flag_z_milli = models.CharField(max_length=30, null=True, blank=True)
    ref_z_milli = models.CharField(max_length=30, null=True, blank=True)
    #z_SHSRC = models.FloatField(null=True, blank=True)
    #flag_z_SHSRC = models.CharField(max_length=100, null=True, blank=True)
    #class_z_SHSRC = models.CharField(max_length=100, null=True, blank=True)
    #ref_z_SHSRC = models.CharField(max_length=100, null=True, blank=True)
    #z_qsoc_Gaia = models.FloatField(null=True, blank=True)
    #flag_z_qsoc = models.FloatField(null=True, blank=True)
    #W1 = models.FloatField(null=True, blank=True)
    #W2 = models.FloatField(null=True, blank=True)
    #W3 = models.FloatField(null=True, blank=True)
    #W4 = models.FloatField(null=True, blank=True)
    #e_W1 = models.FloatField(null=True, blank=True)
    #e_W2 = models.FloatField(null=True, blank=True)
    #e_W3 = models.FloatField(null=True, blank=True)
    #e_W4 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.Name}_{self.Component}'