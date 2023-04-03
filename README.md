# AD-StudentManagement
<p>Development of a simple Active Directory - Student Management System in Python for teaching purposes</p>

Supports  
<ul>
<li>Import of students with their classes from csv file</li>
<li>Removal of former students and classes</li>
</ul>

Includes:
<ul>
<li>Simple CLI based UI</li>
<li>VBScripts for installing prerequisits on file server and domain controller</li>
</ul>

## Installation

<ol>
<li>Install a Windows Domain Controller and if required a file server and a Windows Client</li>
<li>Install Python on the computer on which you want to run this student management software.</li>
<li>Download or clone the software from Github.</li>
<li>Navigate in downloaded folder</li>
<li>Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```
</li>
<li>Copy or rename <i>settings-template.py</i> to <i>settings.py</i> and enter the appropriate data of your domain.</li>
<li>In VBScript <i>vbScripts/installPrerequisitesDC.vbs</i>, specify your domain name and run the script as the <b>domain administrator on the domain controller</b>.</li>
<li>Run VBScript <i>vbScripts/installPrerequisitesFS.vbs</i> as the <b>domain administrator on the file server</b>.</li>
</ol>

## Program start

```bash
python importStudents.py
```

## Testing

Start the test program with 
```bash
pytest testImportStudents.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
