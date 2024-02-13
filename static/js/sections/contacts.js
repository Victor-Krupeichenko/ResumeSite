gsap.registerPlugin(ScrollTrigger)

export class Contacts {
    constructor() {
        this.skillsItemTitle = document.querySelectorAll('.skills__slider .item .item-title')
        this.itemTitleFirst = document.querySelector('.itemTitleFirst')
        this.itemTitleLast = document.querySelector('.itemTitleLast')
        this.contactTitle = document.querySelector('.contacts__title')
        this.socialLinks = document.querySelectorAll('.social__link .link')
        this.contactFormView = document.querySelector('.form-message')
        this.btnContact = document.querySelector('.btn-contact-from')
    }

    // Добавление элементов в бесконечную ленту
    AddItemToendlessFeed() {
        this.skillsItemTitle.forEach(title => {
            this.itemTitleFirst.innerHTML += `${title.textContent} &#10070; `
            this.itemTitleLast.innerHTML += `${title.textContent} &#10070; `
        })
    }

    // Анимация появления заголовка
    ShowTitle() {
        gsap.from(this.contactTitle, {
            x: '-1100', onComplete: () => {
                this.contactTitle.classList.add('active')
            }, scrollTrigger: {
                trigger: this.contactTitle, start: 'top 86%', end: 'top 78%', // markers: true,
                scrub: 2, onLeaveBack: () => {
                    this.contactTitle.classList.remove('active')
                }

            }
        })
    }

    // Появление значков соц.сецей
    ShowSocialLinks() {
        gsap.from(this.socialLinks, {
            y: '1000', stagger: .5, scrollTrigger: {
                trigger: '.contacts__wrapper', // markers: true,
                start: 'top 75%', end: 'top 70%', scrub: 2
            }

        })
    }

    // Появление формы
    ShowContactForm() {
        gsap.from(this.contactFormView, {
            x: '1100', opacity: 0, scrollTrigger: {
                trigger: '.contact__form', // markers: true,
                start: 'top 75%', end: 'top 70%', scrub: 2
            }
        })
    }

    // Отправка формы
    SendMessageContactForm() {
        this.btnContact.addEventListener('click', async function (evt) {
            evt.preventDefault()
            const form = document.querySelector('.form-message')
            const formData = new FormData(form)
            form.reset()
            await asyncSendMessage(formData)
        })
    }

    // Все анимации
    ShowAllAnimations() {
        this.ShowTitle()
        this.ShowSocialLinks()
        this.ShowContactForm()
        this.SendMessageContactForm()
    }
}

// Запуск отправки формы
const asyncSendMessage = async function (form) {
    const response = await fetch('/send-message', {
        method: 'POST',
        body: form
    })
    const data = await response.json()
    console.log(data)
    if (data.status === 200) {
        // TODO возможность запуска отправки сообщаения
        console.log(data)
    }
}








