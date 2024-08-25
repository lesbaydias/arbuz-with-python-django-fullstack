function update_basket(id, action, page) {
    $.ajax({
        url: '/update_basket',
        type: 'GET',
        data: { id,action,page },
        success: (result) => {
            console.log(result);
            var response = result;
            var html = response['html'];
            if (page=='basket'){
                change_basket(response);
            }
        },
        error: () => {
            console.log('error');
        }
    });
}

function change_basket(response){
    document.querySelector('.card-body').innerHTML=response['html'];
    document.querySelector('#sum').innerHTML=response['sum'];
}