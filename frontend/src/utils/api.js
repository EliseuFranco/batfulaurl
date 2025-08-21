

const create_url = async function(data) {
      
    console.log(data)
      try {
        const request = await fetch('http://127.0.0.1:8000/create_shorten_url', {
            method: 'POST',
            headers: {
            'Authorization': `Bearer ${data.token}`,
            'Content-Type': 'application/json' 
            },
            body: JSON.stringify({url: data.url})

        });

        if(!request.ok){
            console.log(request)
            return {error: 'Não foi possível estabelecer ligação com o servidor'}
        }
       
        const responseData  = await request.json();

        if (responseData.shorten_url){
          return {error: responseData.msg}
        }

        return responseData

      } catch (error) {
            console.log('Houve um erro ao criar URL: ', error)
            return 'Houve um erro ao estabelecer ligação'
      }
    }


export {create_url}