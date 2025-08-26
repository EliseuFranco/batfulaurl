import  mitt from 'mitt'
import { jwtDecode } from 'jwt-decode'

const eventBus = mitt()



const copyToClipBoard = async function(text) {
    try{
        navigator.clipboard.writeText(text)
        return 'Copiado para área de transferência'
    }
    catch(error){
        console.log("Algo correu mal", error)
    }

}

 const getSlug = function(shorten_url){
        if(!shorten_url){
            return ''
        }
        const ArrayURL = shorten_url.split('/')
        const size = ArrayURL.length
        return ArrayURL[size - 1]
    }


const createMask = (url) => {
    try {
        const parsed = new URL(url)
        const domain = parsed.hostname
        return domain.length > 25 ? domain.slice(0, 25) + '...' : domain
    } catch (error) {
        return url.length > 30 ? url.slice(0, 30) + '...' : url
    }
}

const isAuthenticated = function(){
    const token = localStorage.getItem('token')

    if(!token){
        return false
    }
    const {exp} = jwtDecode(token)

    return exp * 1000 > Date.now()
}

const calcConversionRate = (unique_clicks, total_clicks) => {
    if (!total_clicks) return 0;
    return ((unique_clicks / total_clicks) * 100).toFixed(2);
}


export {eventBus, copyToClipBoard, getSlug, createMask, isAuthenticated, calcConversionRate}