// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Manager, Command};
use std::process::Command as StdCommand;
use std::thread;
use std::time::Duration;

fn main() {
  tauri::Builder::default()
    .setup(|app| {
      let app_handle = app.handle();

      // Spawn backend in a separate thread so as not to block.
      thread::spawn(move || {
        // Start backend API
        let backend_script = format!("{}/scripts/start_backend.sh", app_handle.path_resolver().resolve_resource("../").unwrap().display());
        let _backend_child = StdCommand::new("sh")
          .arg(&backend_script)
          .spawn()
          .expect("Failed to start backend API");

        // Start dashboard
        let dashboard_script = format!("{}/scripts/start_dashboard.sh", app_handle.path_resolver().resolve_resource("../").unwrap().display());
        let _dashboard_child = StdCommand::new("sh")
          .arg(&dashboard_script)
          .spawn()
          .expect("Failed to start Streamlit dashboard");

        // Wait a few seconds for the dashboard to come online
        thread::sleep(Duration::from_secs(10));

        // Now the dashboard should be running at http://127.0.0.1:8501
        // We can instruct the window to navigate there.
        app_handle.get_window("main").unwrap().eval("window.location.replace('http://127.0.0.1:8501');").unwrap();
      });

      Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}