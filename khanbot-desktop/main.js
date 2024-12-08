const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let backendProcess;
let dashboardProcess;

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        title: 'KhanBot'
    });

    // Load the loading screen
    mainWindow.loadFile('loading.html');

    // Start the services
    startServices();
}

async function startServices() {
    try {
        // Start backend service
        console.log('Starting backend service...');
        backendProcess = spawn('conda', ['run', '-n', 'backend-api', 'uvicorn', 'main:app', '--reload'], {
            cwd: path.join(__dirname, 'backend-api')
        });

        backendProcess.stdout.on('data', (data) => {
            console.log(`Backend: ${data}`);
        });

        backendProcess.stderr.on('data', (data) => {
            console.error(`Backend Error: ${data}`);
        });

        // Wait for backend to start
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Start dashboard service
        console.log('Starting dashboard service...');
        dashboardProcess = spawn('conda', ['run', '-n', 'dashboard', 'streamlit', 'run', 'main.py'], {
            cwd: path.join(__dirname, 'dashboard')
        });

        dashboardProcess.stdout.on('data', (data) => {
            console.log(`Dashboard: ${data}`);
        });

        dashboardProcess.stderr.on('data', (data) => {
            console.error(`Dashboard Error: ${data}`);
        });

        // Wait for dashboard to start
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Load the dashboard URL
        mainWindow.loadURL('http://localhost:8501');

    } catch (error) {
        console.error('Failed to start services:', error);
    }
}

function cleanup() {
    if (backendProcess) {
        backendProcess.kill();
    }
    if (dashboardProcess) {
        dashboardProcess.kill();
    }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    cleanup();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Handle app quit
app.on('before-quit', () => {
    cleanup();
});