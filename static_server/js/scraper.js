const scraperForm = document.querySelector('#scrap-paa-form')
const scrapResult = document.querySelector('#scrap-result')
const loader = document.querySelector('#loader-main')

document.addEventListener('DOMContentLoaded', function () {
    loader.style.display = 'none'
})

scraperForm.addEventListener('submit', function (event) {
    event.preventDefault()

    const csrfmiddlewaretoken = event.target.elements['csrfmiddlewaretoken'].value
    const keyWord = event.target.elements['keyWord'].value
    const numOfTimes = event.target.elements['numOfTimes'].value
    const relatedKeyWord = event.target.elements['relatedKeyWord'].checked
    const pixaBayKeyWord = event.target.elements['pixaBayKeyWord'].checked
    const pexelKeyWord = event.target.elements['pexelKeyWord'].checked
    const unSplashKeyWord = event.target.elements['unSplashKeyWord'].checked
    const googleKeyWord = event.target.elements['googleKeyWord'].checked
    const youTubeKeyWord = event.target.elements['youTubeKeyWord'].checked
    const paaKeyWord = event.target.elements['paaKeyWord'].checked
    const serpKeyWord = event.target.elements['serpKeyWord'].checked


    const formData = new FormData()

    formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken)
    formData.append('keyWord', keyWord)
    formData.append('numOfTimes', numOfTimes)
    formData.append('relatedKeyWord', relatedKeyWord)
    formData.append('pixaBayKeyWord', pixaBayKeyWord)
    formData.append('pexelKeyWord', pexelKeyWord)
    formData.append('unSplashKeyWord', unSplashKeyWord)
    formData.append('googleKeyWord', googleKeyWord)
    formData.append('youTubeKeyWord', youTubeKeyWord)
    formData.append('paaKeyWord', paaKeyWord)
    formData.append('serpKeyWord', serpKeyWord)

    scrapResult.innerHTML = ''
    loader.style.display = 'inline-block'

    fetch('/people-also-ask', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(body => {
            let html = ``
            body.data.forEach(data => {
                html += `<h3>${data.keyword}</h3><h5>People Also Ask</h5><ol>`
                data.paa.forEach(paa => {
                    html += `<li>${paa.question}</li>
                            <p class="ms-4">${paa.answer}</p>`
                })
                html += '</ol>'
                if (data.related) {
                    html += '<h5>Related Search</h5><ol>'
                    data.related.forEach(related => {
                        html += `<li>${related}</li>`
                    })
                    html += '</ol>'
                }
                if (data.pixabaycom || data.pexelscom || data.unsplashcom || data.googleImages) {
                    html += '<h5>Images</h5><div class="row align-items-center">'
                    if (data.pixabaycom) {
                        data.pixabaycom.forEach(images => {
                            html += `<div class="col"><img class="img-thumbnail image-thumbmail" src="${images}" alt="${images}"/><a class="api-url" href="https://pixabay.com/">pixabay.com</a></div>`
                        })
                    }
                    if (data.pexelscom) {
                        data.pexelscom.forEach(images => {
                            html += `<div class="col"><img class="img-thumbnail image-thumbmail" src="${images}" alt="${images}"/><a class="api-url" href="https://www.pexels.com/">pexels.com</a></div>`
                        })
                    }
                    if (data.unsplashcom) {
                        data.unsplashcom.forEach(images => {
                            html += `<div class="col"><img class="img-thumbnail image-thumbmail" src="${images}" alt="${images}"/><a class="api-url" href="https://unsplash.com/">unsplash.com</a></div>`
                        })
                    }
                    if (data.googleImages) {
                        data.googleImages.forEach(images => {
                            html += `<div class="col"><img class="img-thumbnail image-thumbmail" src="${images}" alt="${images}"/><a class="api-url" href="https://www.google.com/">Google</a></div>`
                        })
                    }
                    html += '</div>'
                }
                if (data.video) {
                    html += '<h5 class="mt-4">Videos</h5><div class="row align-items-center">'
                    data.video.forEach(videos => {
                        html += `<div class="col"><a class="api-url" href="${videos}">${videos}</a></div>`
                    })
                    html += '</div>'
                }
            });
            loader.style.display = 'none'
            scrapResult.innerHTML = html
        }).catch(err => {
        loader.style.display = 'none'
        let html = ``
        html += '<p>Some Exception Accrued!</p>'
        scrapResult.innerHTML = html
        console.error(err)
    })
})
