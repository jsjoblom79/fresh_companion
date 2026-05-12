async function load_tasks(){
    try {
        tasks = await window.pywebview.api.get_all_tasks();
    } catch (err) {

    }
}

function display_tasks() {
    const tasksList = document.getElementById('all-tasks');

    if(tasks.length === 0){
        tasksList.innerHTML = "No Tasks have been created."
        return;
    }

    tasks.forEach(task => {
    const p = document.createElement('p');
        p.innerHTML = `task`;
    });

    tasksList.appendChild(p);
}

window.addEventListener('pywebviewready', () => {
    load_tasks();
})