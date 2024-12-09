const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let backendProcess;
let dashboardProcess;

async function startServices() {
    try {
        // Start backend service
        console.log('Starting backend service...');
        backendProcess = spawn('conda', [
            'run', 
            '-n', 
            'backend-api', 
            'uvicorn', 
            'main:app', 
            '--reload',
            '--host', 
            'localhost',
            '--port', 
            '8000'
        ], {
            cwd: path.join(__dirname, 'backend-api')
        });

        // Wait for backend to start
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Start dashboard with correct Streamlit flags
        console.log('Starting dashboard...');
        const streamlitEnv = {
            ...process.env,
            STREAMLIT_SERVER_PORT: "8501",
            STREAMLIT_SERVER_ADDRESS: "localhost",
            STREAMLIT_SERVER_HEADLESS: "true",
            STREAMLIT_BROWSER_SERVER_ADDRESS: "localhost",
            STREAMLIT_BROWSER_GATHER_USAGE_STATS: "false"
        };

        dashboardProcess = spawn('conda', [
            'run',
            '-n',
            'dashboard',
            'streamlit',
            'run',
            'main.py',
            '--server.port=8501',
            '--server.address=localhost',
            '--server.headless=true'
        ], {
            cwd: path.join(__dirname, 'dashboard'),
            env: streamlitEnv
        });

        // Log outputs for debugging
        backendProcess.stdout.on('data', (data) => {
            console.log(`Backend: ${data}`);
        });

        backendProcess.stderr.on('data', (data) => {
            console.error(`Backend Error: ${data}`);
        });

        dashboardProcess.stdout.on('data', (data) => {
            console.log(`Dashboard: ${data}`);
        });

        dashboardProcess.stderr.on('data', (data) => {
            console.error(`Dashboard Error: ${data}`);
        });

        // Wait for dashboard to start
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Load the dashboard URL in the Electron window
        mainWindow.loadURL('http://localhost:8501');

    } catch (error) {
        console.error('Failed to start services:', error);
    }
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        title: 'KhanBot'
    });

    mainWindow.loadFile('loading.html');
    startServices();
}

function cleanup() {
    if (backendProcess) backendProcess.kill();
    if (dashboardProcess) dashboardProcess.kill();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    cleanup();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', cleanup);