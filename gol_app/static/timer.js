// ==========================    Game of Life    ===================================
const canvas = document.getElementById('gol');
const ctx = canvas.getContext('2d');
const resol = 10;
let nonstop = true;
canvas.width = window.innerWidth - 20;
canvas.height = 700;

const cols = canvas.width / resol
const rows = canvas.height / resol

function make_grid() {
    return new Array(cols).fill(null)
    .map(() => new Array(rows).fill(null)
        .map(() => Math.floor(Math.random() * 2)));
}

let gol_grid = make_grid();
let anim;
render(gol_grid)
// requestAnimationFrame(update_grid);

function update_grid() {
    if (nonstop) {
        gol_grid = next_gen(gol_grid);
        render(gol_grid);
        requestAnimationFrame(update_grid);
    }
}

function next_gen(grid) {
    const next = grid.map(arr => [...arr]);
    for (let col = 0; col < grid.length; col++) {
        for (let row = 0; row < grid[col].length; row++) {
            const cell = grid[col][row];
            let sum_of_neightboors = 0;
            for (let i = -1; i < 2; i++) {
                for (let j = -1; j < 2; j++) {
                    if (i === 0 && j === 0) {
                        continue;
                    }
                    const x_cell = col + i;
                    const y_cell = row + j;

                    if (x_cell >= 0 && y_cell >= 0 && x_cell < cols && y_cell < rows) {
                        const neighboor = grid[col + i][row + j];
                        sum_of_neightboors += neighboor;
                    }
                }
            }
            if (cell === 1 && sum_of_neightboors < 2) {
                next[col][row] = 0;
            } else if (cell === 1 && sum_of_neightboors > 3) {
                next[col][row] = 0;
            } else if (cell === 0 && sum_of_neightboors === 3) {
                next[col][row] = 1;
            } 
        }
    }
    return next
}


function render(grid) {
    for (let col = 0; col < grid.length; col++) {
        for (let row = 0; row < grid[col].length; row++) {
            const cell = grid[col][row];
            ctx.beginPath();
            ctx.rect(col * resol, row * resol, resol, resol);
            ctx.fillStyle = cell ? 'black' : 'white';
            ctx.fill();
        }
    }
        
}

// ========================== Timer for the game ===================================

const time_element = document.getElementById('timer')
const saver = document.getElementById('saver');
time_element.innerHTML = '00:00:00';
let current_time = new Date(2022, 11, 24, 0, 0, 0);
let interval;

document.getElementById('stop_btn').disabled = true;


function define_time_str(chunck){
    return chunck < 10 ? `0${chunck}` : `${chunck}`; 
}


function get_time_chunks(date){
    return {
        hours: define_time_str(date.getHours()),
        minutes: define_time_str(date.getMinutes()),
        seconds: define_time_str(date.getSeconds()) 
    }    
}

function displayTime(time) {
    time_obj = get_time_chunks(time)
    time_element.innerHTML = `${time_obj.hours}:${time_obj.minutes}:${time_obj.seconds}`;
}

function timer() {
    current_time.setSeconds(current_time.getSeconds() + 1);
    displayTime(current_time);
}


function startTimer() {
    time_element.innerHTML = '00:00:00';
    interval = setInterval(timer, 1000);
    document.getElementById('start_btn').disabled = true;
    document.getElementById('stop_btn').disabled = false;
    anim = requestAnimationFrame(update_grid);
    nonstop = true;
    saver.classList.add('invisible');
}

function stopTimer() {
    clearInterval(interval);
    clearTimeout(interval);
    current_time = new Date(2022, 11, 24, 0, 0, 0);
    nonstop = false;
    gol_grid = make_grid();
    saver.classList.remove('invisible');
    
    document.getElementById('stop_btn').disabled = true;
    document.getElementById('start_btn').disabled = false;
    
    console.log(saver);
}

function save() {
    window.location = `http://127.0.0.1:5000/save_score/${time_element.innerHTML}`
}