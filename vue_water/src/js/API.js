export default function API_URL(url) {
    let apiUrl = 'https://water-hrcs-django.azurewebsites.net'
        //let apiUrl = ' http://127.0.0.1:8000' // 測試用

    // apiUrl = localStorage.getItem('api')
    url = apiUrl
    return url
}