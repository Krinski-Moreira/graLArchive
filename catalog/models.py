from django.db import models

# Create your models here.

from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

class Lens(models.Model):
    class Boolean_class(models.TextChoices):
        TRUE = "TRUE"
        FALSE = "FALSE"

    Name = models.CharField(max_length=30, unique=True)
    RA_mean = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    DEC_mean = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    Type = models.CharField(max_length=10)
    Author = models.CharField(max_length=20, blank=True)
    BibCode = models.CharField(max_length=20, blank=True)
    GraL = models.CharField(max_length=5, choices=Boolean_class.choices, blank=True)
    Max_separation = models.FloatField()
    Diameter = models.FloatField(null=True, blank=True)
    Nb_of_galaxies = models.IntegerField(null=True, blank=True)
    Confirmed = models.IntegerField(null=True, blank=True)
    CS43 = models.CharField(max_length=5, choices=Boolean_class.choices, blank=False)
    DR3 = models.CharField(max_length=5, choices=Boolean_class.choices, blank=False)
    FPR = models.CharField(max_length=5, choices=Boolean_class.choices, blank=False)
    compId = models.IntegerField(null=True, blank=True)
    Nb_of_published_components = models.IntegerField(null=True, blank=True)
    z_source = models.FloatField(null=True, blank=True)
    z_lens = models.FloatField(null=True, blank=True)
    z_bibcode = models.CharField(max_length=20, null=True, blank=True)
    astrometric_excess_noise = models.FloatField(null=True, blank=True)
    astrometric_excess_noise_sig = models.FloatField(null=True, blank=True)
    pseudocolour = models.FloatField(null=True, blank=True)
    pseudocolour_error = models.FloatField(null=True, blank=True)
    duplicated_source = models.CharField(max_length=5, choices=Boolean_class.choices, blank=False)
    Comments = models.TextField(null=True, blank=True)
    nbNeighors = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('lens-name', args=[str(self.Name)])

class LensComponent(models.Model):
    Name = models.ForeignKey(Lens, on_delete=models.CASCADE)
    Component = models.CharField(max_length=5)
    RA_best = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    DEC_best = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    DEC_sexa = models.CharField(max_length=20, null=True, blank=True)
    source_id_CS43 = models.BigIntegerField(null=True, blank=True)
    source_id_DR3 = models.BigIntegerField(null=True, blank=True)
    gravLensName = models.CharField(max_length=30, null=True, blank=True)
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
    astrometric_n_good_obs_al = models.IntegerField(null=True, blank=True)
    astrometric_gof_al = models.FloatField(null=True, blank=True)
    astrometric_chi2_al = models.FloatField(null=True, blank=True)
    astrometric_params_solved = models.IntegerField(null=True, blank=True)
    visibility_periods_used = models.IntegerField(null=True, blank=True)
    ruwe = models.FloatField(null=True, blank=True)
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
    phot_g_mean_mag_corrected = models.FloatField(null=True, blank=True)
    phot_g_mean_mag_error_corrected = models.FloatField(null=True, blank=True)
    phot_g_mean_flux_corrected = models.FloatField(null=True, blank=True)
    nObsComp = models.IntegerField(null=True, blank=True)
    ra_FPR = models.FloatField(null=True, blank=True)
    stdra_FPR = models.FloatField(null=True, blank=True)
    dec_FPR = models.FloatField(null=True, blank=True)
    stddec_FPR = models.FloatField(null=True, blank=True)
    G_FPR = models.FloatField(null=True, blank=True)
    stdG_FPR = models.FloatField(null=True, blank=True)
    ra_CS43 = models.FloatField(null=True, blank=True)
    raError_CS43 = models.FloatField(null=True, blank=True)
    dec_CS43 = models.FloatField(null=True, blank=True)
    decError_CS43 = models.FloatField(null=True, blank=True)
    gFluxMean_CS43 = models.FloatField(null=True, blank=True)
    onBoardGMag_CS43 = models.FloatField(null=True, blank=True)
    muAlpha_CS43 = models.FloatField(null=True, blank=True)
    muAlphaError_CS43 = models.FloatField(null=True, blank=True)
    muDelta_CS43 = models.FloatField(null=True, blank=True)
    muDeltaError_CS43 = models.FloatField(null=True, blank=True)
    parallax_CS43 = models.FloatField(null=True, blank=True)
    parallaxError_CS43 = models.FloatField(null=True, blank=True)
    matchedSemester_CS43 = models.IntegerField(null=True, blank=True)
    whichMatchedSemester = models.BigIntegerField(null=True, blank=True)
    matchedObservations = models.IntegerField(null=True, blank=True)
    matchedObservationsUsedByAgis = models.IntegerField(null=True, blank=True)
    Separation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.Name} {self.Component}'