console.log("Hello World") // in-line comment

document.addEventListener("DOMContentLoaded", function () {
    const firstButton=document.getElementById("firstButton");
    const firstForm=document.forms["myForm"]

    firstButton.addEventListener("mouseover", traTraTaOn);
    firstButton.addEventListener("mouseout", traTraTaOff);
    firstButton.addEventListener("click", alertOn);
    firstForm.addEventListener("submit", validateForm);
    firstForm.addEventListener("keydown", keyDownOn);

    function traTraTaOn() {
    const title = document.getElementById('main-heading');
    title.innerHTML="Тра-та-та-та-ТА!";
    title.style.color='red';
    console.log(title);
    }   

    function traTraTaOff() {
    const title = document.getElementById('main-heading');
    title.innerHTML="Contacts list: ";
    title.style.color='white';
    console.log(title);
    }  

    function alertOn() {
    alert("Hello!")
    }  

    function validateForm() {
        let x = document.forms["myForm"]["fname"].value;
        if (x=="") {
            alert("Empty name")
            return false
        }
    }

    function keyDownOn(event) {
    const formDescription=document.getElementById("formDescription");
    formDescription.innerHTML=event.key
    }  
})

// counter
document.addEventListener("DOMContentLoaded", function () {
    const counterInt=document.getElementById("counterInt");
    const counterText=document.getElementById("counterText");
    const plusBtn=document.getElementById("plusBtn");
    const minusBtn=document.getElementById("minusBtn");
    const resetBtn=document.getElementById("resetBtn");
    const saveBtn=document.getElementById("saveBtn");
    const loadBtn=document.getElementById("loadBtn");

    if (localStorage.getItem('counter')){
        loadCounter()
    }else{
        let count=10;
        counterInt.innerHTML=count
    }

    function defaultText(){
        counterInt.innerHTML=count;
        counterText.innerHTML="";
    }
    function loadCounter(){
        count=localStorage.getItem('counter');
        counterInt.innerHTML=count;
        counterText.innerHTML='Counter '+count+' loaded.';
    }
    
    plusBtn.addEventListener('click', function(){
        count++;
        defaultText();
    });
    minusBtn.addEventListener('click', function(){
        if (count>0){
            count--;
            defaultText();
        }else{
            counterText.innerHTML="Counter can't be below zero!" 
        }
    });
    resetBtn.addEventListener('click', function(){
        count=0;
        defaultText();
    });
    saveBtn.addEventListener('click', function(){
        localStorage.setItem('counter', count);
        counterText.innerHTML='Counter '+count+' saved.';
    });
    loadBtn.addEventListener('click', loadCounter);
})
// end of counter

// to-do list
document.addEventListener("DOMContentLoaded", function () {
    let taskInputText=document.getElementById("taskInputText");
    const addTaskBtn=document.getElementById("addTaskBtn");
    const loadTaskBtn=document.getElementById("loadTaskBtn");
    const clearAllBtn=document.getElementById("clearAllBtn");
    const taskDecription=document.getElementById("taskDecription");
    const toDoList=document.getElementById("toDoList");
    displayTask();

    function displayTask(){
        let taskArray = JSON.parse(localStorage.getItem('taskArray'));
        toDoList.innerHTML="";
        
        for (let i = 0; i < taskArray.length; i++){
            const bullet = document.createElement("li");
            bullet.innerText = taskArray[i];
            toDoList.appendChild(bullet);
        }
    }

    function addTask(){
        let taskArray = JSON.parse(localStorage.getItem('taskArray'));
        let inputValue=taskInputText.value;
        if (inputValue !== "") {
            taskArray.push(inputValue);
            localStorage.setItem('taskArray', JSON.stringify(taskArray));
            // taskDecription.innerHTML=taskArray;
            displayTask();
        } else {
            alert("Empty task")
        }
    }

    function loadTask(){
        let taskArray = JSON.parse(localStorage.getItem('taskArray'));
        // taskDecription.innerHTML='Loaded list: '+taskArray;
        displayTask();
    }

    function clearAllTask(){
        let taskArray = [];
        localStorage.setItem('taskArray', JSON.stringify(taskArray));
        // taskDecription.innerHTML='Cleared list: '+taskArray;

        displayTask();
    }

    function inputToDo (event) {
        if (event.key=="Enter") {
            addTask();
        }
    }

    addTaskBtn.addEventListener('click', addTask); 
    loadTaskBtn.addEventListener('click',loadTask);
    clearAllBtn.addEventListener('click', clearAllTask);
    taskInputText.addEventListener('keydown', inputToDo);
})
// end of to-do list