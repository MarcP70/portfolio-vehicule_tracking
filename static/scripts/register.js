document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {
      name: "",
      email: "",
      password: "",
      isNameValid: true,
      isEmailValid: true,
      isPasswordValid: true,
      isLoading: false,
      errorMessage: "",
    },
    watch: {
      name(value) {
        this.isNameValid = value.length > 0;
      },
      email(value) {
        const regex = new RegExp(
          /(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/
        );
        this.isEmailValid = regex.test(value);
      },
      password(value) {
        this.isPasswordValid = value.length >= 8;
      },
    },
    methods: {
      validateForm() {
        // Retourne true si tous les champs sont valides, sinon false
        return this.isNameValid && this.isEmailValid && this.isPasswordValid;
      },
      submitForm() {
        if (this.validateForm()) {
          this.isLoading = true;
          const formData = {
            name: this.name,
            email: this.email,
            password: this.password,
          };

          // Enregistrez l'instance de Vue dans une variable pour y accéder dans les callbacks
          const vm = this;

          $.ajax({
            url: "/user/signup",
            type: "POST",
            data: formData,
            dataType: "json",
            success: function (resp) {
              window.location.href = "/dashboard/";
            },
            error: function (xhr) {
              // Parsez la réponse et mettez à jour errorMessage
              let errorMsg = "Erreur inattendue. Veuillez réessayer.";
              if (xhr.responseText) {
                try {
                  const response = JSON.parse(xhr.responseText);
                  errorMsg = response.error || errorMsg;
                } catch (e) {
                  // Erreur lors du parse du JSON, conservez errorMsg par défaut
                }
              }

              // Utilisez vm qui réfère à l'instance Vue ici
              vm.errorMessage = errorMsg;

              vm.$nextTick(() => {
                const $error = document.querySelector(".error");
                if ($error) {
                  $error.textContent = vm.errorMessage;
                  $error.classList.remove("error--hidden");
                }
              });
            },
            complete: () => {
              vm.isLoading = false;
            }
          });
        }
      }
    },
  });
});
