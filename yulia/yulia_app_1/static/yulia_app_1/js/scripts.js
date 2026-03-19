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
    let toDoListButtons = toDoList.getElementsByTagName("button");
    const updateBtn=document.getElementById("updateBtn");

    if (JSON.parse(localStorage.getItem('taskObj'))===null){
        const taskObj={};
        localStorage.setItem('taskObj', JSON.stringify(taskObj));
    } else {
        const taskObj=JSON.parse(localStorage.getItem('taskObj'));
    }

    displayTask();

    addTaskBtn.addEventListener('click', addTask); 
    loadTaskBtn.addEventListener('click',loadTask);
    clearAllBtn.addEventListener('click', clearAllTask);
    taskInputText.addEventListener('keydown', inputToDo);
    // updateBtn.addEventListener('click', toDoCheckBox);
    for (let i = 0; i < toDoListButtons.length; i++){
        toDoListButtons[i].addEventListener('click', toDoButtons);
    }

    function displayTask_old(){
        let taskArray = JSON.parse(localStorage.getItem('taskArray'));
        toDoList.innerHTML="";
        
        for (let i = 0; i < taskArray.length; i++){
            const bullet = document.createElement("li");
            bullet.innerText = taskArray[i];
            toDoList.appendChild(bullet);
        }
    }

    function displayTask(){
        const taskObj=JSON.parse(localStorage.getItem('taskObj'));
        let objArray = Object.keys(taskObj);
        toDoList.innerHTML="";

        for (let i = 0; i < objArray.length; i++){
            const bullet = document.createElement("li");
            bullet.innerText = taskObj[objArray[i]];
            toDoList.appendChild(bullet);

            const btnDone = document.createElement("button");
            let textDone = document.createTextNode("Done");
            btnDone.id = 'btnDone-'+i;
            btnDone.appendChild(textDone);
            toDoList.appendChild(btnDone);

            const btnNotDone = document.createElement("button");
            let textNotDone = document.createTextNode("Not done");
            btnNotDone.id = 'btnNotDone-'+i;
            btnNotDone.appendChild(textNotDone);
            toDoList.appendChild(btnNotDone);

            const btnEdit = document.createElement("button");
            let textEdit = document.createTextNode("Edit");
            btnEdit.id = 'btnEdit-'+i;
            btnEdit.appendChild(textEdit);
            toDoList.appendChild(btnEdit);

            // const checkbox = document.createElement("input");
            // checkbox.type='checkbox';
            // checkbox.id = 'cb'+i;
            // toDoList.appendChild(checkbox);

            // const label = document.createElement('label');
            // label.htmlFor = 'toDoCheckbox';
            // label.appendChild(document.createTextNode('Done?'));
            
            // checkBox.label = taskObj[objArray[i]];
            
        }
    }

    function toDoCheckBox(){
        const taskObj=JSON.parse(localStorage.getItem('taskObj'));
        let objArray = Object.keys(taskObj);
        for (let i = 0; i < objArray.length; i++){
            let checkBoxIndex='cb'+i;
            const checkBoxElement=document.getElementById(checkBoxIndex);
            if (checkBoxElement.checked) {
                // console.log("Checkbox " +checkBoxIndex+ " is checked.");
                // console.log(taskObj[objArray[i]]);
                taskObj[objArray[i]]="Done";
                }
            }
        localStorage.setItem('taskObj', JSON.stringify(taskObj));
        displayTask();
        }

    function toDoButtons (event) {
        const taskObj=JSON.parse(localStorage.getItem('taskObj'));
        console.log(event.target.id);
        let btnId=event.target.id;
        let btnIdArray = btnId.split("-");
        let btnTask = btnIdArray[0];
        let toDoId = btnIdArray[1];
        let toDoArray = taskObj[toDoId];
        console.log(btnIdArray);

        if (btnTask==="btnDone"){
            toDoArray[1] = "Done";
        } else if (btnTask==="btnNotDone"){
            toDoArray[1] = "Not done";
        } else if (btnTask==="btnEdit"){
            console.log('Edit button pressed');
        } else {
            console.log('Other button pressed');
        }
        localStorage.setItem('taskObj', JSON.stringify(taskObj));
        displayTask();
        return console.log('End');
    }

    function addTask_old(){
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

    function addTask(){
        const taskObj = JSON.parse(localStorage.getItem('taskObj'));
        let objKeyArray = Object.keys(taskObj);
        let inputValue=taskInputText.value;
        if (inputValue !== "") {
            // taskObj[inputValue]="Not done";
            let objValueArray=[inputValue,"Not done"];
            taskObj[objKeyArray.length]=objValueArray;
            localStorage.setItem('taskObj', JSON.stringify(taskObj));
            displayTask();
        } else {
            alert("Empty task")
        }
    }

    function loadTask_old(){
        let taskArray = JSON.parse(localStorage.getItem('taskArray'));
        // taskDecription.innerHTML='Loaded list: '+taskArray;
        displayTask();
    }

    function loadTask(){
        const taskObj = JSON.parse(localStorage.getItem('taskObj'));
        displayTask();
    }

    function clearAllTask_old(){
        let taskArray = [];
        localStorage.setItem('taskArray', JSON.stringify(taskArray));
        // taskDecription.innerHTML='Cleared list: '+taskArray;

        displayTask();
    }

    function clearAllTask(){
        const taskObj = {};
        localStorage.setItem('taskObj', JSON.stringify(taskObj));
        displayTask();
    }

    function inputToDo (event) {
        if (event.key=="Enter") {
            addTask();
        }
    }



})
// end of to-do list

// toastify
document.addEventListener("DOMContentLoaded", function () {
    // toastify on add_agreement.html
    const addAgreementSubmitBtn=document.getElementById("addAgreementSubmitBtn");
    addAgreementSubmitBtn.addEventListener('click', addToast);
    
    function addToast () {
        Toastify({
            text: "Ваш договор формируется",
            duration: 3000
            }).showToast();
    }
})
// end of toastify