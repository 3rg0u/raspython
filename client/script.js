document.getElementById('door-rpc').addEventListener('submit', function(event){
    event.preventDefault();
    const passcode = document.getElementById('passcode').value;
    fetch('http://127.0.0.1:5000/api/open', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({passcode: passcode}),
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success'){
            Swal.fire({
                title: 'Success!',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'OK'
            });
        }
        else{
            Swal.fire({
                title: 'Error!',
                text: data.message,
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
    })
    .catch(error => {
        Swal.fire({
            title: 'Error!',
            text: 'Something went wrong!',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    });
});