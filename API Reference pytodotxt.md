# API Reference PYTODOTXT

## TodoTxt

###  *class* pytodotxt.**TodoTxt**(*filename, encoding='utf-8', parser=None*)

Convenience wrapper for a single todo.txt file

The most common use is:

    todotxt = TodoTxt("todo.txt")
    todotxt.parse()

Use the tasks property to access the parsed entries.

### **\_\_init\_\_**(*filename, encoding='utf-8', parser=None*)

Create a new TodoTxt instance from filename

**Parameters:**
- **filename**(str or pathlib.Path) – the file you wish to use
- **encoding** – what encoding to assume for the content of the file
- **parser**(TodoTxtParser) – This may be a custom parser instance to use instead of the default TodoTxtParser.

### **add**(*task*)

Add a task to this container

You could also just append to self.tasks, but this function call will also update the todotxt and linenr properties of task.

**Parameters:**
- **task**(Task) – The task that should be added to this todo.txt file

### *property* **lines**

Much like self.tasks, but already sorted by linenr and converted to string

### **parse**()

(Re)parse self.filename

This will try to detect the line separator of the file automatically and remember it as self.linesep for the time when you save the file back to disk.

**Returns:** the list of all tasks read from the file.

### **save**(*target=None, safe=True, linesep=None*)

Save all tasks to disk

If target is not provided, the filename property is being used as the target file to save to.

If safe is set (the default), the file will first be written to a temporary file in the same folder as the target file and after the successful write to disk, it will be moved in place of target. This can cause trouble though with folders that are synchronised to some cloud storage.

With linesep you can specify the line seperator. If it is not set it defaults to the systems default line seperator (or the detected line separator, if the file has been parsed from disk first).

**Parameters:**
- **target** – The file to save to, or None to use self.filename
- **safe** – Whether or not to save the file in a way that does not destroy the previous file in case on errors.
- **linesep** – The line separator, or None to use self.linesep

### **tasks**

The tasks of this file

### **write_to_stream**(*stream, linesep=None*)

Save all tasks, ordered by their line number, to the stream

**Parameters:**
- **stream** – an io.IOBase like stream that accepts bytes being written to it.
- **linesep** – the line separator, or None to use self.linesep

## Task

### *class* pytodotxt.**Task**(*line=None, linenr=None, todotxt=None*)

A task of a todo.txt file

The usual way to create a task is to create it from an initial string:

    task = Task("(B) some task")

or:

    task = Task()
    task.parse("(B) some task")

The inverse operation to parsing is to convert the task to a string:

    task = Task("(B) some task")
    assert str(task) == "(B) some task"

### **\_\_init\_\_**(*line=None, linenr=None, todotxt=None*)

Create a new task

If no parameters are provided, an empty task is created.

You may provide a todo.txtlike textual representation of a task with the line parameter, which will be parsed and all properties will be set accordingly.

In case this task belongs to a container file (todotxt parameter), you can provide the linenr, if you want to be able to refer to it later-on.

Both todotxt and linenr parameter are entirely optional and are not connected to any functionality in this class’s functions.

To access key:value attributes of the task, you can use the convenience notion of task['attr_key'] which will always result in a list. If the task doesn’t have the key attribute that list will be empty though.

**Parameters:**
- **line** – is the raw string representation (one line of a todo.txt file).
- **linenr** – is the line number within the todotxt file, if any. This is purely optional.
- **todotxt** (None or TodoTxt.) – the TodoTxt container to which this task belongs, if any.

### **add_attribute**(*key, value*)

Add the key:value attribute to the end of the task

### **add_context**(*context*)

Add @context to the end of the task

**Parameters:**
- **context** – the name of the project, without the leading @

### **add_project**(*project*)

Add +project to the end of the task

**Parameters:**
- **project** – the name of the project, without the leading +

### **append**(*text, add_space=True*)

Append text to the end of the task

**Parameters:**
- **text** – The text to append
- **add_space** – Whether or not to add a space before text.

### *property* **attributes**

A dict of all key:values attributes

The values portion of the dictionary is always a list.

### **bare_description**()

The description of the task without contexts, projects or other attributes

Some parts of the description may look like attributes, but are not, like URLs. To make sure that these are not stripped from the description, add them to KEYVALUE_ALLOW.

### **completion_date**

datetime.date of when the task was completed, or None if no completion date given

### *property* **contexts**

A list of all @context attributes

### **creation_date**

datetime.date of when the task was created, or None if no creation date given

### **description**

The descriptive portion of the task (i.e. without the completion marker, dates, and priority)

### **is_completed**

Whether or not the task is completed

### **linenr**

Line number of this task within its todo.txt file (0-based; the first task of a file will have self.linenr == 0). Do not count on this always being set!

### **parse**(*line*)

(Re)parse the task

line is the raw string representation of a task, i.e. one line of a todo.txt file.

### **priority**
Priority of the task, or None if no priority given

### *property* **projects**

A list of all +project attributes

### **remove_attribute**(*key, value=None*)

Remove attribute key from the task

If you provide a value only the attribute with that key and value is removed. If no value is provided all attributes with that key are removed.

**Parameters:**
- **key** – The name of the attribute to remove.
- **value** – The value of the attribute to remove.

**Returns:**
True on success, otherwise False

### **remove_context**(*context*)

Remove the first @context attribute from the description.

**Parameters:**
- **context** – the name of the context attribute to remove, without the leading @.

**Returns:**
True on success, otherwise False.

### **remove_project**(*project*)

Remove the first +project attribute from the description.

**Parameters:**
- **project** – the name of the project attribute to remove, without the leading +

**Returns:**
True on success, otherwise False.

### **remove_tag**(*text, regex*)

Remove the first attribute text from the description

**Parameters:**
- **regex** – The regular expression to use for matching the right type of attribute.

### **replace_attribute**(*key, value, newvalue*)

Replace the value of key:value in place with key:newvalue

### **replace_context**(*context, newcontext*)

Replace the first occurrence of @context with @newcontext

### **replace_project**(*project, newproject*)

Replace the first occurrence of @project with @newproject

### **replace_tag**(*value, newvalue, regex*)

Replace the first value attribute with newvalue

**Parameters:**
- **regex** – the regular expression to use for matching the right type of attribute

### **todotxt**

The TodoTxt instance that this task belongs to. Do not count on this always being set!

## TodoTxtParser

### *class* pytodotxt.**TodoTxtParser**(*encoding='utf-8', task_type=None*)

A parser for todo.txt-like formatted strings or files

### **\_\_init\_\_**(*encoding='utf-8', task_type=None*)

Create a new todo.txt parser

**Parameters:**
- **encoding** – The encoding to assume for the parsing process
- **task_type** – A subclass of Task to use when parsing the tasks.

### **linesep**

The line separator. After running any of the parse functions, this property will be set to the line separator that was detected in the parsed object.

### **parse**(*target)*

Parse the given object

The behaviour of the parser depends a bit on what you pass in. It might be a bit surprising, but if you pass in a str, parse will attempt to find tasks in that string.

If you want to parse a file and pass the filename, wrap it in pathlib.Path first or use parse_file directly.

When parsing is completed, you can query linesep to see what the line separator was.

**Parameters:**
- **target** (pathlib.Path, str, bytes, or any io.IOBase.) – the object to parse

**Returns:**

a list of tasks found in target

### **parse_file**(*path*)

Parse the content of the file at path

**Parameters:**
path – The file to parse

**Returns:**
a list of tasks found in file.

### **parse_str**(*text*)

Parse tasks from the given text

**Parameters:**
text – The string containing todo.txt-like tasks

**Returns:**
a list of tasks found in text

### **parse_stream**(*stream*)

Parse an io stream

**Parameters:**
stream – an io stream to read and parse tasks from

**Returns:**
a list of tasks found in stream