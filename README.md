# AD-StudentManagement
<p>Development of a simple Active Directory - Student Management System in Python for teaching purposes. It is assumed that a pupil is exactly in one school class.</p>

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
<li>Download and unzip or clone the software from Github.</li>
<li>Navigate to downloaded and unzipped or cloned folder</li>
<li>Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```
</li>
<li>Copy or rename <i>settings-template.py</i> to <i>settings.py</i> and enter the appropriate data of your domain.</li>
<li>Edit VBScript <i>vbScripts\installPrerequisitesDC.vbs</i>, specify your domain name and run the script as the <b>domain administrator on the domain controller</b>.</li>
<li>Run VBScript <i>vbScripts\installPrerequisitesFS.vbs</i> as the <b>domain administrator on the file server</b>.</li>
<li>Edit students login VBScript <i>vbScripts\studentsLogon.vbs</i>, specify your domain and your file server names.</li>
<li>Create GPO <i>StudentsLogonPolicy</i> on OU <i>Students</i>.</li>
<ul>
<li>Edit this GPO, navigate to <i>User Configuration > Policies > Windows Settings > Scripts (Logon/Logoff)</i></li>
<li>Double-click <i>Logon in the right pane</i> and click <i>Show files</i>. A folder whose name ends in <i>User\Scripts\Logon\</i> is displayed.
<li>Copy your logon script files into this folder.</li>
<li>In the Logon Properties window, click <i>Add</i>.
<li>Click <i>Browse to open the logon script directory</i>, then select your logon script file and click <i>OK</i>.
<li>Verify that the logon script now appears in the list on the Logon Properties window.</li>
<li>Close the Group Policy Management Editor window for your GPO, then close the Group Policy Management window.</li>
</ul>
</ol>

## Program start

```bash
python importStudents.py [path to csv import file]
```
Example:
```bash
python importStudents.py import/students.csv
```

## Testing

Start the test program with unit tests
```bash
testImportStudents.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
