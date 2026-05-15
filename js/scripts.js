async function system_stats(){
    try{
        let task_count = await window.pywebview.api.db.get_total_task_count();
        console.log(task_count);
        const total_task = document.getElementById('total-task-count');
        total_task.textContent = task_count.count;
        const total_completed = document.getElementById('total-completed-tasks');
        total_completed.textContent = task_count.completed;

    } catch (err) {
        console.log(err);
    }
}

async function load_tasks(){
    try {
        tasks = await window.pywebview.api.db.get_all_tasks();
        console.log("load tasks event fired.");
        display_tasks();
    } catch (err) {
        console.log(err);
    }
}

function display_tasks() {
    const tasksList = document.getElementById('all-tasks');
    console.log(tasks.length);
    if(tasks.length === 0){
        tasksList.innerHTML = "No Tasks have been created.";
        return;
    }
    tasksList.innerHTML= "";
    tasksList.innerHTML= `
        <tr>
            <th>Task Title</th>
            <th>Description</th>
            <th></th>
            <th></th>
        </tr>
    `;
    tasks.forEach(task => {

        const detail = document.createElement('button');
        detail.textContent = task.title;
        detail.type = 'button';
        detail.addEventListener('click', () => { window.pywebview.api.load_task_detail(task.id); });

        const delete_button = document.createElement('button');
        delete_button.textContent = 'Delete';
        delete_button.type = 'button';
        delete_button.addEventListener('click', () =>  { window.pywebview.api.db.delete_task(task.id); refresh_window(); });

        const mark_complete = document.createElement('button');
        mark_complete.textContent = 'Complete';
        mark_complete.addEventListener('click', () => { window.pywebview.api.db.mark_complete(task.id); refresh_window(); });

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="action-task-detail"></td>
            <td>${task.description}</td>
            <td class="action-complete"></td>
            <td class="action-delete"></td>
            `;
        tr.querySelector('.action-task-detail').appendChild(detail);
        tr.querySelector('.action-complete').appendChild(mark_complete);
        tr.querySelector('.action-delete').appendChild(delete_button);

        tasksList.appendChild(tr);
    });


}

//function delete_id(id){
//    window.pywebview.api.db.delete_task(id);
//}
function add_task(){

    let description = document.getElementById('task-description').value;
    let followup = new Date();
    followup.setDate(followup.getDate() + 5);
    console.log(followup);
    let newTask = {
        title: document.getElementById('task-title').value,
        description: document.getElementById('task-description').value,
        followup_date: followup.toISOString(),
        last_followup: null,
        is_completed: false
    };

    window.pywebview.api.db.add_task(newTask);
    document.getElementById('task-title').value = '';
    document.getElementById('task-description').value = '';
    refresh_window();
}

function refresh_window() {
    load_tasks();
    system_stats();
}

window.addEventListener('pywebviewready', () => {
    load_tasks();
    system_stats();
});