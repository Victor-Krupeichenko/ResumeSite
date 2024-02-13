gsap.registerPlugin(ScrollTrigger)

export class SlideAndCart {
    // Слайдер и карточки
    constructor() {
        this.allSkillItems = Array.from(document.querySelectorAll('.item'))

        this.activeSlideIdx = 0
        this.direction = 1 // 1 для увеличения, -1 для уменьшения
        this.skillsItems = Array.from(document.querySelectorAll('.skills__icon__item'))
        this.skillsWrapper = document.querySelector('.skills__icon__wrapper')
    }

    // Устанавливает css-свойства для следующего и предыдущего слайда
    setCurrentProperties(slide, numberSlide, tranX, deg) {
        slide.style.transform = `translateX(${tranX * numberSlide}px) scale(${1 - 0.2 * numberSlide}) perspective(16px) rotateY(${deg}deg)`
        slide.style.zIndex = `${-numberSlide}`
        slide.style.filter = 'blur(5px)'
        slide.style.opacity = `${numberSlide > 2 ? 0 : 0.6}`
        slide.style.transitionDuration = '0.5s'
    }

    // Устанавливает css-свойства для текущего слайда
    currentSlideStyle() {
        const currentSlide = this.allSkillItems[this.activeSlideIdx]
        if (currentSlide) { // Проверяем, существует ли элемент
            // Устанавливаем css-свойства
            currentSlide.style.transform = 'none'
            currentSlide.style.zIndex = '1'
            currentSlide.style.filter = 'none'
            currentSlide.style.opacity = '1'
            currentSlide.style.transitionDuration = '0.5s '
        }
    }

    // Показ слайдера
    showSlide() {
        let numberCurrentSlide = 0
        const deg = 1
        const tranX = 120 // trnaslateX 120px
        this.currentSlideStyle()


        this.allSkillItems.slice(this.activeSlideIdx + 1).forEach(slide => {
            numberCurrentSlide += 1
            this.setCurrentProperties(slide, numberCurrentSlide, tranX, -deg)
        })

        numberCurrentSlide = 0
        for (let i = this.activeSlideIdx - 1; i >= 0; i--) {
            numberCurrentSlide += 1
            this.setCurrentProperties(this.allSkillItems[i], numberCurrentSlide, -tranX, deg)
        }
    }

    // Показ текущего слайда
    showCurrentSlide() {
        this.showSlide()
        this.activeSlideIdx += this.direction
        if (this.activeSlideIdx >= this.allSkillItems.length - 1 || this.activeSlideIdx === 0) {
            this.direction *= -1
        }
    }

    // Создание блоков для карточек и заполняет эти блоки содержимым
    createBlockToCard() {
        this.allSkillItems.forEach(item => {
            const imgSrc = item.querySelector('img').getAttribute('src')
            const itemDescr = item.querySelector('.item-description')
            const newElement = document.createElement('div')
            newElement.classList.add('skills__icon__item')
            newElement.innerHTML = `
            <img src="${imgSrc}" alt="skills-image">
            <div class="skills-description">${itemDescr.innerHTML}</div>
            `
            this.skillsWrapper.appendChild(newElement)
        })
    }

    // Анимация карточек
    activeItemSkill() {
        // делает определенную карточку активной и включает анимацию
        // console.log(this.skillsItems)
        this.skillsItems.forEach(item => {
            item.classList.remove('active')
        })
        const activeItem = this.skillsItems[this.activeSlideIdx]
        if (activeItem) {
            activeItem.classList.add('active')
        }

    }

    // Автоматическое переключение слайдера и карточек
    autoSwitchingSlide() {
        setInterval(() => {
            this.activeItemSkill()
            this.showCurrentSlide()
        }, 2000) // переключаем слайдер
    }

}

const cardSkills = new SlideAndCart()
cardSkills.createBlockToCard() // Создаем блоки с карточками и наполняем их содержимым

export class SkillsAnimation {
    constructor() {
        this.skillsBlockTitle = document.querySelector('.skills__title')
        this.skillsSlide = document.querySelector('.skills__slider')
        this.skillsIconWrapper = document.querySelector('.skills__icon__wrapper')
    }

    // Появление заголовка
    viewTitle() {
        gsap.from(this.skillsBlockTitle, {
            scale: 10, y: '50%', duration: 3, opacity: 0, scrollTrigger: {
                trigger: this.skillsBlockTitle, start: 'top 50%', end: 'top 20%', // markers: true,
                scrub: 2, onEnter: () => {
                    this.skillsBlockTitle.classList.add('active')
                }, onLeaveBack: () => {
                    this.skillsBlockTitle.classList.remove('active')
                }
            }
        })
    }

    // Появление слайдера
    viewSlide() {
        gsap.from(this.skillsSlide, {
            y: '100%', opacity: 0, duration: 2, scrollTrigger: {
                trigger: '.skills__wrapper', start: 'top 65%', end: 'top 50%', // markers: true,
                scrub: 2
            }
        })
    }

    // Появление карточек
    viewCard() {
        gsap.to('.skills__icon__item', {
            y: 0, scale: 1, ease: 'circ.out', stagger: .07, opacity: 1, repeatDelay: 1, scrollTrigger: {
                trigger: this.skillsIconWrapper, // markers: true,
                start: 'top 85%', end: 'top 80%', scrub: 2
            }
        })
    }

    // Вызов всех анимаций
    callAllFuncions() {
        this.viewTitle()
        this.viewSlide()
        this.viewCard()
    }
}













