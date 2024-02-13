import {Header} from "./sections/header.js"
import {About} from "./sections/about.js"
import {Experience} from "./sections/expirience.js"
import {SlideAndCart, SkillsAnimation} from "./sections/skills.js"
import {Contacts} from "./sections/contacts.js"


// header
const header = new Header()
header.callAllFuncions()

// About
const about = new About()
about.animationAbout()

// Experience
const experience = new Experience()
experience.callAllFuncions()

// Skills
const skillSlideandCard = new SlideAndCart()
skillSlideandCard.showSlide()
skillSlideandCard.autoSwitchingSlide()
const skillAnimation = new SkillsAnimation()
skillAnimation.callAllFuncions()

// Contacts
const contacts = new Contacts()
contacts.ShowAllAnimations()
contacts.AddItemToendlessFeed()


const upword = document.querySelector('.upward')

window.addEventListener('scroll', function () {
    upword.classList.toggle('active', window.scrollY > 500)
    header.updateActiveLink()
})
header.updateActiveLink()

const scrollTo = function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth',
    })
}

upword.addEventListener('click', scrollTo)


