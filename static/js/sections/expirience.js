gsap.registerPlugin(ScrollTrigger)

export class Experience {
    constructor() {
        this.experienceTitle = document.querySelector('.expirience__title')
        this.expirienceLline = Array.from(document.querySelectorAll('.expirience-line'))
        this.expirienceInscription = Array.from(document.querySelectorAll('.expirience-inscription'))
        this.listItems = Array.from(document.querySelectorAll('.list__item'))

    }

    // Скрытие блоков
    hiddenBlockItem() {
        this.listItems.forEach((item, index) => {
            if (index % 2 === 0) {
                item.style.transform = `translateX(150%)`
            } else {
                item.style.transform = `translateX(-150%)`
            }
        })
    }

    // Анимация появление заголовка
    viewTitle() {
        gsap.to('.expirience__title', {
            top: 0,
            scale: 1,
            duration: 2,
            onComplete: () => {
                this.experienceTitle.classList.add('active')
            },
            scrollTrigger: {
                trigger: '.expirience',
                // markers: true,
                start: 'top 90%',
                end: 'top 80%',
                scrub: 1,
                toggleActions: 'restart none none none',
                onEnterBack: () => {
                    this.experienceTitle.classList.remove('active')
                }
            }
        })
    }

    // Анимация перед описанием
    animationDescription() {
        // анимация динии
        const tl = gsap.timeline()
        this.expirienceLline.forEach((elem, index) => {
            let even = 0
            if (index % 2 !== 0) {
                even = 1
            }
            tl.to(elem, {
                duration: 4,
                height: '70%',
                repeat: -1,
                yoyo: true,
            }, even)
        })

        // анимация паука
        this.expirienceInscription.forEach((elem, index) => {
            let even = 0
            if (index % 2 !== 0) {
                even = 1
            }
            tl.to(elem, {
                duration: 4,
                top: '85%',
                repeat: -1,
                yoyo: true
            }, even)
        })
    }

    // Анимация появления блоков при скроле
    animationToScroll() {
        gsap.to('.list__item', {
            x: 0,
            opacity: 1,
            duration: 5,
            scrollTrigger: {
                trigger: '.list__item',
                // markers: true,
                start: 'top 70%',
                end: 'top 50%',
                toggleActions: 'restart none none none',
                scrub: 3,

                onEnter: () =>{
                    this.animationDescription()
                },
                onUpdate: function () {
                    gsap.set('.expirience-line, .expirience-inscription', {clearProps: 'all'})
                },
            }
        })
    }

    // Вызов необходимых методов
    callAllFuncions() {
        this.hiddenBlockItem()
        this.viewTitle()
        this.animationToScroll()
    }
}



























