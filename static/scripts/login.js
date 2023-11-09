document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {
      email: "",
      password: "",
      isEmailValid: true,
      isPasswordValid: true,
      isLoading: false,
      errorMessage: "",
    },
    watch: {
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
        // La logique de validation est maintenant gérée par les watchers
        return this.isEmailValid && this.isPasswordValid;
      },
      submitForm() {
        if (this.validateForm()) {
          this.isLoading = true;
          const formData = {
            email: this.email,
            password: this.password,
          };

          // Enregistrez l'instance de Vue dans une variable pour y accéder dans les callbacks
          const vm = this;

          $.ajax({
            url: "/user/login",
            type: "POST",
            data: formData,
            dataType: "json",
            success: (resp) => {
              if (resp.user.role === "admin") {
                window.location.href = "/admin/users/";
              } else {
                window.location.href = "/dashboard/";
              }
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
            },
          });
        }
      },
    },
  });
});
