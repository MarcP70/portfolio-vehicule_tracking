document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {
      editMode: false,
      date: trackingData.date,
      trackingId: trackingData._id,
      mileage: trackingData.mileage,

      tireFrontLeft: trackingData.tire_front_left === "true",
      tireFrontRight: trackingData.tire_front_right === "true",
      refTiresFront: trackingData.ref_tires_front,
      tireRearLeft: trackingData.tire_rear_left === "true",
      tireRearRight: trackingData.tire_rear_right === "true",
      refTiresRear: trackingData.ref_tires_rear,

      brakePadsFront: trackingData.brake_pads_front === "true",
      refBrakePadsFront: trackingData.ref_brake_pads_front,
      brakePadsRear: trackingData.brake_pads_rear === "true",
      refBrakePadsRear: trackingData.ref_brake_pads_rear,

      brakeDisksFront: trackingData.brake_disks_front === "true",
      refBrakeDisksFront: trackingData.ref_brake_disks_front,
      brakeDisksRear: trackingData.brake_disks_rear === "true",
      refBrakeDisksRear: trackingData.ref_brake_disks_rear,

      oilChange: trackingData.oil_change === "true",
      refOilChange: trackingData.ref_oil_change,

      oilFilter: trackingData.oil_filter === "true",
      refOilFilter: trackingData.ref_oil_filter,

      airFilter: trackingData.air_filter === "true",
      refAirFilter: trackingData.ref_air_filter,

      fuelFilter: trackingData.fuel_filter === "true",
      refFuelFilter: trackingData.ref_fuel_filter,

      cabinFilter: trackingData.cabin_filter === "true",
      refCabinFilter: trackingData.ref_cabin_filter,

      isDateValid: true,
      isMileageValid: true,

      errorMessage: "",
      successMessage: "",
      showSuccessMessage: false,
    },
    methods: {
      enterEditMode() {
        const mileageErrorMessage = document.getElementById(
          "mileageErrorMessage"
        );
        const dateErrorMessage = document.getElementById("dateErrorMessage");

        mileageErrorMessage.innerText = "";
        dateErrorMessage.innerText = "";

        this.editMode = true; // Activez le mode d'édition
      },
      validateMileage: function () {
        // Remplacez tous les caractères non numériques par une chaîne vide
        this.mileage = this.mileage.replace(/[^0-9]/g, "");
        // Formate le nombre avec des espaces tous les 3 chiffres
        this.mileage = Number(this.mileage).toLocaleString("fr-FR");
      },
      validateForm() {
        this.isDateValid = this.date.length !== 0;
        if (!this.isDateValid) {
          dateErrorMessage.innerText = "Date non conforme";
        }
        this.isMileageValid = parseFloat(this.mileage) > 0;
        if (!this.isMileageValid) {
          mileageErrorMessage.innerText = "Kilométrage non conforme";
        }

        return this.isDateValid && this.isMileageValid;
      },

      toggleTireFrontLeft: function () {
        this.TireFrontLeft = !this.TireFrontLeft;
      },
      toggleTireFrontRight: function () {
        this.TireFrontRight = !this.TireFrontRight;
      },
      toggleTireRearLeft() {
        this.TireRearLeft = !this.TireRearLeft;
      },
      toggleTireRearRight() {
        this.TireRearRight = !this.TireRearRight;
      },
      toggleBrakePadsFront() {
        this.brakePadsFront = !this.brakePadsFront;
      },
      toggleBrakePadsRear() {
        this.brakePadsRear = !this.brakePadsRear;
      },
      toggleBrakeDisksFront() {
        this.brakeDisksFront = !this.brakeDisksFront;
      },
      toggleBrakeDisksRear() {
        this.brakeDisksRear = !this.brakeDisksRear;
      },
      toggleOilChange() {
        this.oilChange = !this.oilChange;
      },
      toggleOilFilter() {
        this.oilFilter = !this.oilFilter;
      },
      toggleAirFilter() {
        this.airFilter = !this.airFilter;
      },
      toggleFuelFilter() {
        this.fuelFilter = !this.fuelFilter;
      },
      toggleCabinFilter() {
        this.cabinFilter = !this.cabinFilter;
      },

      updateTracking() {
        if (this.validateForm()) {
          const formData = {
            trackingId: this.trackingId,
            date: this.date,
            mileage: this.mileage,

            tireFrontLeft: this.tireFrontLeft,
            tireFrontRight: this.tireFrontRight,
            refTiresFront: this.refTiresFront,
            tireRearLeft: this.tireRearLeft,
            tireRearRight: this.tireRearRight,
            refTiresRear: this.refBrakePadsRear,

            brakePadsFront: this.brakePadsFront,
            refBrakePadsFront: this.refBrakePadsFront,
            brakePadsRear: this.brakePadsRear,
            refBrakePadsRear: this.refBrakePadsRear,

            brakeDisksFront: this.brakeDisksFront,
            refBrakeDisksFront: this.refBrakeDisksFront,
            brakeDisksRear: this.brakeDisksRear,
            refBrakeDisksRear: this.refBrakeDisksRear,

            oilChange: this.oilChange,
            refOilChange: this.refOilChange,

            oilFilter: this.oilFilter,
            refOilFilter: this.refOilFilter,

            airFilter: this.airFilter,
            refAirFilter: this.refAirFilter,

            fuelFilter: this.fuelFilter,
            refFuelFilter: this.refFuelFilter,

            cabinFilter: this.cabinFilter,
            refCabinFilter: this.refCabinFilter,
          };
          const trackingId = window.location.pathname.split("/")[2];
          const errorMessage = document.getElementById("errorMessage");
          const successMessage = document.getElementById("successMessage");
          // Envoyer les données au serveur Flask
          $.ajax({
            url: `/tracking/${trackingId}/update_tracking`,
            type: "POST",
            data: formData,
            dataType: "json",
            success: function (resp) {
              successMessage.innerText = resp.message;
            },
            error: function (xhr) {
              if (xhr.status === 500) {
                errorMessage.innerText = xhr.message;
              }
            },
          });
        } else {
          console.log("Formulaire non valide, veuillez corriger les champs.");
        }
        this.editMode = false;
      },
    },
  });
  const formattedDateElements = document.querySelectorAll(".formatted-date");
  formattedDateElements.forEach((element) => {
    const isoDate = element.textContent;
    const dateToFormat = new Date(isoDate);
    element.textContent = dateToFormat.toLocaleDateString("fr-FR");
  });
});
