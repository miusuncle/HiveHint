#HiveHint

##What is HiveHint?

HiveHint is a sublime text plugin that dedicated for our current front-end project. It includes several practical features that you can use them to impove development productivity to some degrees. It is compatible with Sublime Text 2+, but it works best with Sublime Text 3. If you use Sublime Text as your coding editor, make sure have a try with it.

##Installation

Open terminal, change directory to:

  - windows: C:\Users\johndoe\AppData\Roaming\Sublime Text 3\Packages
  - mac:

Clone this plugin into current directory with the following command:

```bash
git clone https://github.com/miusuncle/HiveHint.git
```

Once finished, you can find a menu item appears as `Tools | HiveHInt`. You may need to restart Sublime Text if necessary.

##Configuration

First, make sure you have configurate and save our `hive-frontend` project as Sublime Text project.

Then, open project, and edit project by executing menu command: `Project | Edit Project`, you should config the opened file similar as follow:

```json
{
	"folders": [
		{
			"name": "SCRIPTS",
			"path": "/dir/to/hive-frontend/hm-webapp/resources/scripts"
		},
		{
			"name": "I18N",
			"path": "/dir/to/hive-frontend/hm-webapp/resources/i18n"
		},
		{
			"name": "STYLES",
			"path": "/dir/to/hive-frontend/hm-webapp/resources/styles"
		},
		{
			"name": "FONT",
			"path": "/dir/to/hive-frontend/hm-webapp/resources/font"
		},
		{
			"name": "IMAGES",
			"path": "/dir/to/hive-frontend/hm-webapp/resources/images"
		}
	]
}
```

##Feature & Usage

You can find most commands under menu item `Tools | Hive Hint`.

###Toggle Javascript and Relevant Template File

For example, if current actived file is `ah/comp/devicemanagement/DeviceList.js`, press `F1` key, the revelant template file `ah/comp/devicemanagement/templates/DeviceList.html` will be opened or switch to, vice versa.

###Quick jump to module file current cursor point to

Assume `|` is our current cursor, and we are in `"ah/util/AH|Component",` press `Alt + Q`, module file `ah/util/AHComponent.js` will be immediately opened or switch to.

###Goto Symbol Definition(only works with Sublime Text 3)

A more friendly version of sublime text 3's native `Goto Definition`(Goto | Goto Definition...) command, you can find the command under menu `Tools | Hive Hint | Goto Symbol Definition`, and the default shortcut is `Alt + Shift + Q`, feel free to have a try.

###Copy Module Id & Copy Relative Template Path

If current actived file is `ah/comp/devicemanagement/DeviceList.js`, press `Alt + Shift + Y` key(or right click, you will find a menu item called `Open Module Id` if you don't like shortcuts), then the current javascript file's module Id will be copy to clipboard, you can paste it to any file you find appropriate.

If current actived file is `ah/comp/devicemanagement/templates/DeviceList.html`, press `Alt + Shift + Y`, the corresponding tempate path(`./templates/DeviceList.html`) relative to `ah/comp/devicemanagement/DeviceList.js` will be copy to clipboard, you can replace `XXX` in `dojo/text!XXX` with the copied path.

###Insert Module Id

You can find this command under `Tools | Hive Hint | Insert Module Id`, also use its shortcut `Shift + Space` is more effictive.

Say we have the following code(see Before), we want to insert module `dojo/Deferred` before `dojo/_base/lang`, first we put two cursor before `lang`(see Preparation), then press `Shift + Space` to call out the registered module list, and find `dojo/Deferred`, press `Enter` key, we can get our result(see Result).

```js
// Before
define([
	'dojo/aspect',
	'dojo/_base/lang'
], function (
	aspect, lang
) {

});

// Preparation(`|` means cursor)
define([
	'dojo/aspect',
	|'dojo/_base/lang'
], function (
	aspect, |lang
) {

});

// Result
define([
	'dojo/aspect',
	'dojo/Deferred',
	'dojo/_base/lang'
], function (
	aspect, Deferred, lang
) {

});
```

###Register module to be used by `Insert Module Id`

You can find some pre-register module in file `HiveHint.sublime-settings`. To open that file, execute menu item `Tools | Hive Hint | Hive Hint Settings` or just press the relavant shortcut. In that file, you can follow the existing  module to add your own.

###Quick open registered module file

This command locate under `Tools | Hive Hint | Hint Preset Module Definition`, the default shortcut is `Alt + Shift + Space`, feel free to have a try.

###Some commonly used dojo snippets

You can find some predefined dojo snippets by execute menu command `Tools | Hive Hint | Config Dojo Completions`, feel free to have a try.

##There are more

You can find more features not list here by inspecting the project directory.
