export class Header {
    constructor() {
        this.links = document.querySelectorAll('.navbar__list__link')
        this.indicator = document.querySelector('.navbar__indicator')
        this.active = document.querySelector('.active')
        this.verticalIndicator = ''
        this.selectBtn = document.querySelector('.header__content__menu-btn')
        this.textOption = document.querySelector('.text-option')
        this.options = document.querySelectorAll('.option')
        this.navbar = document.querySelector('.navbar')
        this.text = document.querySelector('.header__content__title')
    }

    // Делает ссылку активной
    activeLink(item, vertical = false) {
        this.links.forEach(link => {
            link.classList.remove('active')
        })
        item.classList.add('active')
        const itemIndex = item.dataset.index
        if (vertical) {
            if (this.verticalIndicator) {
                this.indicator.style.transform = `translateY(${itemIndex * 35}px)`
            }
        } else {
            this.indicator.style.transform = `translateX(${itemIndex * 70}px)`
        }
    }

    // Автоматическое переключение активной ссылки панели навигации
    getCurrentSection() {
        // Определение текущего раздела на основе положения прокрутки
        const sections = document.querySelectorAll('.section')
        let currentSection = ''
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 330 // начала секции
            const sectionHeight = section.offsetHeight  // ширина секции
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                currentSection = section.id
            }
        })
        return currentSection
    }

    // Показывает какая сейчас вкладка активна
    updateActiveLink() {
        if (window.scrollY > 500) { // 500px вниз - только потом появится вертикальный navbar
            this.navbar.classList.add('vertical')
            this.verticalIndicator = document.querySelector('.vertical .navbar__indicator')
        } else {
            this.navbar.classList.remove('vertical')
        }
        const currentSection = this.getCurrentSection()
        this.links.forEach(link => {
            const linkHref = link.querySelector('a').getAttribute('href')
            const sectionId = linkHref.substring(1) // удаляем символ # из href
            if (sectionId === currentSection) {
                this.activeLink(link, true)
            } else {
                link.classList.remove('active')
            }
        })
    }

    // Появдляющийся текст заголовка
    popupText() {
        const splitText = function (text) {
            // Разбиение текста на символы
            text.innerHTML = text.textContent.replace(/(\S*)/g, m => {
                return `<div class="word">` +
                    m.replace(/([-#@])?\S(-|#@)?/g, "<div class='letter'>$&</div>") + `</div>`

            });
            return text
        }

        const myFuncRandom = function (min, max) {
            // Для рандомных позиций появления букв
            return Math.random() * (max - min) + min
        }

        const letters = splitText(this.text)
        const allLetters = Array.from(letters.querySelectorAll('.letter'))

        // Анимация букв
        allLetters.forEach((char, index) => {
            TweenMax.from(char, {
                duration: 2,
                opacity: 0,
                scale: .1,
                x: myFuncRandom(-500, 500),
                y: myFuncRandom(-500, 500),
                z: myFuncRandom(-500, 500),
                delay: index * .02,
                repeat: 0,
            })
        })
    }

    // Выбор типа файла для загрузки
    // TODO добавить загрузку файла по клику на ссылке
    typeFile() {
        this.selectBtn.addEventListener('click', () => {
            this.selectBtn.classList.toggle('active')
        })
        this.options.forEach(option => {
            option.addEventListener('click', () => {
                this.textOption.innerHTML = option.textContent
                this.selectBtn.classList.remove('active')
                const changeType = option.textContent.trim().substring(1).toLowerCase()
                const link = document.createElement('a')
                link.href = `/download-file/${changeType}`
                link.click()
            })
        })
    }

    // Собрана gsap анимация
    animationHeader() {
        // Анимация уголков
        gsap.to('.header__top-left-border', {
            left: 5,
            width: 605,
            duration: 1,
            delay: 1,

        })
        gsap.to('.header__top-right-border', {
            right: 5,
            width: 605,
            duration: 1,
            delay: 1
        })
        gsap.to('.header__left-top-border, .header__right-top-border', {
            height: 150,
            duration: 1,
            delay: 1.7
        })
        gsap.to('.header__left-bottom-border, .header__right-bottom-border', {
            height: 150,
            duration: 1,
            delay: .5
        })
        gsap.to('.header__bottom-left-border, .header__bottom-right-border', {
            width: 150,
            duration: 1,
            delay: .5
        })

        // Меню загрузки резюме
        gsap.to('.header__content__menu', {
            duration: 2,
            x: 0,
            ease: 'bounce'
        })
        // Появление nabar
        gsap.from('.navbar', {
            y: '-100',
            duration: 1,
        })
    }

    // Вызов необходимых методов
    callAllFuncions() {
        this.popupText()
        this.typeFile()
        this.animationHeader()
    }
}

