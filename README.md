<div style="font-family:Arial, Helvetica, sans-serif; max-width:1100px; margin:auto; line-height:1.6; color:#222">

<h1 align="center">Bee Protego</h1>

<p align="center">
Malware Detection and Security Analysis Toolkit
</p>

<p align="center">
<img src="https://img.shields.io/github/stars/smilymouth/BeeProtego?style=for-the-badge">
<img src="https://img.shields.io/github/forks/smilymouth/BeeProtego?style=for-the-badge">
<img src="https://img.shields.io/github/issues/smilymouth/BeeProtego?style=for-the-badge">
<img src="https://img.shields.io/github/license/smilymouth/BeeProtego?style=for-the-badge">
</p>

<p align="center">
<img src="https://img.shields.io/badge/Security-Toolkit-blue?style=flat-square">
<img src="https://img.shields.io/badge/YARA-Enabled-green?style=flat-square">
<img src="https://img.shields.io/badge/Python-3.9+-yellow?style=flat-square">
</p>

<hr>

<div style="background:#f4f6f8; padding:15px; border-left:5px solid #2c3e50;">
<strong>Overview</strong><br><br>
Bee Protego is a lightweight cybersecurity toolkit designed for malware detection, file analysis, and security research.
It uses YARA-based rule matching to identify malicious patterns and integrates scanning, detection, and reporting into a unified workflow.
</div>

<br>

<div style="background:#eef7ff; padding:15px; border-left:5px solid #2980b9;">
<strong>Key Features</strong>
<ul>
<li>YARA-based malware detection</li>
<li>Multi-file scanning</li>
<li>Automated PDF reporting</li>
<li>Modular rule engine</li>
<li>Optional AI-based threat explanation</li>
</ul>
</div>

<hr>

<h2>Preview</h2>

<p align="center">
<img src="screenshot.jpg" width="700">
</p>

<hr>

<h2>Quick Start</h2>

<div style="background:#f8f8f8; padding:10px; border:1px solid #ddd;">
<pre>
git clone https://github.com/smilymouth/BeeProtego.git
cd BeeProtego
pip install -r requirements.txt
python BeeProtego.py
</pre>
</div>

<hr>

<h2>Detection Flow</h2>

<div style="display:flex; justify-content:space-between; text-align:center; font-size:14px;">
<div style="flex:1; background:#ecf0f1; padding:10px; margin:5px;">Input</div>
<div style="flex:1; background:#d6eaf8; padding:10px; margin:5px;">Scan</div>
<div style="flex:1; background:#d5f5e3; padding:10px; margin:5px;">Detect</div>
<div style="flex:1; background:#fcf3cf; padding:10px; margin:5px;">Process</div>
<div style="flex:1; background:#fadbd8; padding:10px; margin:5px;">Report</div>
</div>

<hr>

<h2>Performance Overview</h2>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:100%">
<tr style="background:#2c3e50; color:white;">
<th>Metric</th>
<th>Value</th>
</tr>
<tr><td>Scan Speed</td><td>Fast</td></tr>
<tr style="background:#f2f2f2;"><td>Accuracy</td><td>Rule-based precision</td></tr>
<tr><td>Resource Usage</td><td>Low to moderate</td></tr>
</table>

<hr>

<h2>AI Integration</h2>

<div style="background:#eefaf1; padding:15px; border-left:5px solid #27ae60;">
Local AI support using Ollama for threat explanation.
</div>

<div style="background:#f8f8f8; padding:10px; border:1px solid #ddd; margin-top:10px;">
<pre>
ollama pull llama3
ollama run llama3
</pre>
</div>

<hr>

<h2>License</h2>
<p>MIT License</p>

<hr>

<h2>Author</h2>
<p>
smilymouth<br>
Cybersecurity Researcher
</p>

</div>
