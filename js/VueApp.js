var app = new Vue({
  el: "#vuejscrudapp",
  data: {
    records: [],
    oMember: {},
    iAction: 1, // 1 nuevo, 2 editar
  },
  mounted() {
    this.getRecords();
  },
  methods: {
    /**
     * Obtiene los registros de la URL y los setea en la variable global
     */
    getRecords() {
      SGui.showWaiting(2000);
      
      axios({
        url: "http://localhost:5000/",
        method: "get",
      })
        .then((res) => {
          console.log(res);
          this.records = res.data.members;
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(function () {
          // always executed
        });
    },
    /**
     * Reinicia el objeto miembro y prepara el modal para la creación del
     * nuevo regiwtro
     */
    newMember() {
      this.oMember = {};
      this.iAction = 1;
      $("#memberModalId").modal("show");
    },
    /**
     * Recibe el id del miembro a editarse y consulta los datos de la BD
     * 
     * @param int idMember 
     */
    editMember(idMember) {
      SGui.showWaiting(2000);
      this.iAction = 2;
      this.oMember = {};
      axios({
        url: "http://localhost:5000/edit/" + idMember,
        method: "get",
      })
        .then((res) => {
          console.log(res);
          this.oMember = res.data.editmember;
          $("#memberModalId").modal("show");
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(function () {
          // always executed
        });
    },
    /**
     * Dependiendo si es registro nuevo o no, determina si se guarda o solo se actualiza
     */
    saveMember() {
      SGui.showWaiting(2000);
      if (this.iAction == 1) {
        this.storeMember();
      } else {
        this.updateMember();
      }
    },
    /**
     * Guardar registro
     */
    storeMember() {
      let config = {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      };
      axios({
        method: "post",
        url: "http://localhost:5000/insert",
        data: {
          firstname: this.oMember.firstname,
          lastname: this.oMember.lastname,
          address: this.oMember.address,
        },
        config,
      })
        .then((res) => {
          console.log(res);
          SGui.showMessage("Agregado correctamente");
          this.getRecords();
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(function () {
          // always executed
        });
    },
    /**
     * Actualización de registro
     */
    updateMember() {
      let config = {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      };
      axios({
        method: "put",
        url: "http://localhost:5000/update",
        data: {
          firstname: this.oMember.firstname,
          lastname: this.oMember.lastname,
          address: this.oMember.address,
          id: this.oMember.id,
        },
        config,
      })
        .then((res) => {
          console.log(res);
          SGui.showMessage("Modificado correctamente");
          this.getRecords();
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(function () {
          // always executed
        });
    },
    /**
     * Eliminación del registro
     * @param int idMember 
     */
    deleteMember(idMember) {
      if (window.confirm('¿Estás seguro que deseas borrar este registro?')) {
        SGui.showWaiting(2000);
        axios({
          method: "delete",
          url: "http://localhost:5000/delete/" + idMember
        })
          .then((res) => {
            console.log(res);
            SGui.showMessage("Eliminado correctamente");
            this.getRecords();
          })
          .catch((err) => {
            console.log(err);
          })
          .finally(function () {
            // always executed
          });
      }
    }
  },
});
