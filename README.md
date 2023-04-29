<h2>SunnyBoy </h2>
<p>This project consists of two repositories:</br>
Project "SunnyBoy" a Web Server Application AND Project "MoonY" a ioT Client Application </p>
<p>The idea behind the "SunnyBoy" project is, that the Sunnyboy-Server manages and stores (weather-)information and administers the control of several "MoonY" clients. First, a "MoonY" requests its to-do list from the server. It works through the received process steps in its to-do list and sends back data to the server whenever a process step requires to do so. The collected data is stored in the server's database. Furthermore, all to-do lists are editable through a web interface to maximize the system's flexibility. The server and client communication is established by Rest API endpoints. </p>
<h2>Table of Contents</h2>
<ul>
  <li><a href="#getting-started">Getting Started</a></li>
  <li><a href="#how-it-is-done">Frontend</a></li>
  <li><a href="#how-it-is-done">Backend</a></li>
  <li><a href="#version">Version</a></li>
  <li><a href="#built-with">Built With</a></li>
  <li><a href="#license">License</a></li>
</ul>
<h2>Getting Started</h2>
<p>The "Sunnyboy" Server Application runs on every server instance as long as python3 is installed. Therefore, it can be used on a hosted server in the web or a raspberry pi running in your local network. </p>
<a href="url"><img src="https://user-images.githubusercontent.com/55065075/235248025-86310ed0-0836-4ba3-8bf7-e2d25dbefa02.png" height="auto" width="500" ></a>
<h2>Frontend</h2>
<p>The frontend consists of four routes.<br>
<h3>/home</h3>
<p>Here, the last in the servers database stored weatherinformations are displayed. The user can edit the requested location by editing the entry in the textfield. By pushing the Update-button, the weatherinformation are updated. </p>
<a href="url"><img src="https://user-images.githubusercontent.com/55065075/234973144-7887be5f-5e5a-40b3-bfe8-94379d13c3f3.png" height="auto" width="500" ></a>
<h3>/client process control</h3>
<h3>/api & /about</h3>
<h2>Backend</h2>
<h3>System Architecture</h3>
<p>The server side consits of the three segments as shown in the picture below. </p>
<a href="url"><img src="https://user-images.githubusercontent.com/55065075/235254542-2c8e5483-edde-4a65-a2c4-9c69e754d229.png" height="auto" width="500" ></a>
<h4>app</h4>
<p>insert routes/API endpoints here</p>
<h4>packages</h4>
<p>scrapes data from my own weather info api - for more information, see: Project weather information api </p>
<h4>database</h4>
<p>insert Database ER-Modell here</p>
<h2>Version</h2>
<p>V1 042023 (!still in development!)</p>
<h2>Built-with</h2>
<p>Flask, SQLite3</p>
<h2>license</h2>
<p>...</p>
