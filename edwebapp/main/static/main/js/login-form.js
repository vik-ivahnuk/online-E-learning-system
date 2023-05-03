const signUp = document.getElementById('sign-up'),
signIn = document.getElementById('sign-in'),
loginIn = document.getElementById('s-in'),
loginUp = document.getElementById('s-up')

signUp.addEventListener('click', ()=>{
  loginIn.classList.remove('block')
  loginUp.classList.remove('hidden-element')

  loginIn.classList.add('hidden-element')
  loginUp.classList.add('block')
})

signIn.addEventListener('click', ()=>{
  loginIn.classList.remove('hidden-element')
  loginUp.classList.remove('block')

  loginIn.classList.add('block')
  loginUp.classList.add('hidden-element')
})