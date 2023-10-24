class SGui {
    static showWaiting(iTime) {
        Swal.fire({
            title: 'Espere...',
            showConfirmButton: false,
            timer: iTime
          });
    }

    static showMessage(sMessage) {
        Swal.fire(sMessage);
    }
}