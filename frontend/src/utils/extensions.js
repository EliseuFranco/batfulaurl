import  mitt from 'mitt'

const eventBus = mitt()



const copyToClipBoard = async function(text) {
    
    try{
        navigator.clipboard.writeText(text)
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


export {eventBus, copyToClipBoard, getSlug, createMask}