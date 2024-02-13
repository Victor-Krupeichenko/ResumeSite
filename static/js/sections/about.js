gsap.registerPlugin(ScrollTrigger)

export class About {
    constructor() {
        this.aboutTitle = document.querySelector('.about__title')
    }

    // Анимация
    animationAbout() {
        gsap.to('.about__title', {
            x: 1100,
            duration: 2,
            ease: "sine.out",
            onComplete: () => {
                this.aboutTitle.classList.add('active')
            },
            scrollTrigger: {
                trigger: '.about',
                start: 'top 85%',
                end: 'top 40%',
                // markers: true,
                toggleActions: 'restart none none none',
                scrub: 1,
                onEnterBack: () => {
                    this.aboutTitle.classList.remove('active')
                }

            }
        })
        gsap.to('.about__text__content', {
            y: 0,
            duration: 2,
            ease: "circ.out",
            scrollTrigger: {
                trigger: '.about__text',
                // markers: true,
                start: 'top 68.5%',
                end: 'top 63.2%',
                toggleActions: 'restart none none none',
                scrub: 2,
            }
        })
    }
}


