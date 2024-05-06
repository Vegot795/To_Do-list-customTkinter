import json
import os
import customtkinter
import pickle

root = customtkinter.CTk()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root.geometry("900x600")
root.minsize(300,600)
root.title("Tudu App")

# Funkcje i klasy
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)


class TaskFrame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(row=0, column=1, sticky='nsew')


        self.label = customtkinter.CTkLabel(self, text="Tudu - your personal task list")
        self.label.grid(row=0, column=1, sticky='nsew')

        self.click_button = customtkinter.CTkButton(self, text="Add new task", width=20, command=self.open_task_creator)
        self.click_button.grid(row=1, column=1, sticky='nsew')

    def open_task_creator(self):
        self.grid_forget()
        task_list_frame.grid_forget()
        task_creator_frame.grid(columnspan=3, rowspan=3, sticky='nsew')
        task_creator_frame.columnconfigure(0, weight=1)
        task_creator_frame.columnconfigure(2, weight=1)


class TaskCreatorFrame(customtkinter.CTkFrame):
    def __init__(self, root, task_instance):
        super().__init__(root)
        self.my_tasks = task_instance

        else_frame = customtkinter.CTkFrame(self)
        else_frame.grid(row=0,columnspan=3, sticky='nsew')
        else_frame.columnconfigure(0, weight=1)
        else_frame.columnconfigure(2, weight=1)


        description_frame = customtkinter.CTkFrame(self)
        description_frame.grid(row=2, columnspan=3, sticky='nsew')
        description_frame.columnconfigure(0, weight=1)
        description_frame.columnconfigure(2, weight=1)

        self.task_name_label = customtkinter.CTkLabel(else_frame, text="Task Name:")
        self.task_name_entry = customtkinter.CTkEntry(else_frame)
        self.task_name_label.grid(column=1, sticky='nsew')
        self.task_name_entry.grid(column=1, sticky='nsew')

        self.task_time_label = customtkinter.CTkLabel(else_frame, text="Task Time:")
        self.task_time_entry = customtkinter.CTkEntry(else_frame)
        self.task_time_label.grid(column=1, sticky='nsew')
        self.task_time_entry.grid(column=1, sticky='nsew')

        self.task_type_label = customtkinter.CTkLabel(else_frame, text="Task Type:")
        self.task_type_entry = customtkinter.CTkEntry(else_frame)
        self.task_type_label.grid(column=1, sticky='nsew')
        self.task_type_entry.grid(column=1, sticky='nsew')

        self.task_description_label = customtkinter.CTkLabel(description_frame, text="Task Description:")
        self.task_description_textbox = customtkinter.CTkEntry(description_frame)
        self.task_description_label.grid(row=0, column=1, sticky='w')
        self.task_description_textbox.grid(row=1, column=0, sticky='nsew', columnspan=3, rowspan=3)

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(column=1, sticky='nsew', row=3)

        self.save_button = customtkinter.CTkButton(self.button_frame, text="Save Task", width=20, command=self.save_current_task)
        self.save_button.grid()

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="Cancel", width=20, command=self.open_main_window)
        self.cancel_button.grid()

    def add_new_task(self):
        task_name = self.task_name_entry.get()
        task_description = self.task_description_textbox.get()
        task_time = self.task_time_entry.get()
        task_type = self.task_type_entry.get()

        my_tasks.add_task(task_name, task_time, task_type, task_description)
        self.my_tasks.save_task()
        task_list_frame.update_task_list()

    def open_main_window(self):
        self.grid_forget()
        task_frame.grid(row=0, column=1, sticky='nsew')
        task_list_frame.grid(row=1, column=0, sticky='nsew', columnspan=3)
        self.my_tasks.load_tasks()
        task_list_frame.update_task_list()

    def save_current_task(self):
        self.add_new_task()
        self.my_tasks.save_task()
        self.my_tasks.load_tasks()
        task_list_frame.update_task_list()


class Tasks:

    def __init__(self):
        self.tasks = []
        if not os.path.exists('saves/tasks.json'):
            self.tasks.append({
                'name': 'My Task',
                'description': 'This is a sample task',
                'time': '1 hour',
                'type': 'Personal'
            })
        self.load_tasks()

    def add_task(self, name, description, time, type):
        new_task = {
            'name': name,
            'description': description,
            'time': time,
            'type': type
        }
        self.tasks.append(new_task)

    def get_tasks(self):
        return self.tasks

    def save_task(self):
        try:
            with open('saves/tasks.json', 'w') as file:  # 'wb' is write binary mode
                json.dump(self.tasks, file)
            print("Tasks saved successfully.")
        except IOError as e:
            print(f"An error occurred while saving tasks: {e}")

    def load_tasks(self):
        if os.path.exists('saves/tasks.json'):
            with open('saves/tasks.json', 'r') as file:
                try:
                    self.tasks = json.load(file)
                except json.JSONDecodeError as e:  # Correct exception for JSON files
                    print(f"An error occurred while loading tasks: {e}")
                    self.tasks = []  # Fallback to an empty list if loading fails
        else:
            self.tasks = []  # Create an empty list if the file doesn't exist


class TaskListFrame(customtkinter.CTkFrame):

    def __init__(self, root, tasks_instance):
        super().__init__(root)
        self.grid(row=1, sticky='nsew', columnspan=3)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.my_tasks = tasks_instance
        self.configure('lightblue')


    def update_task_list(self):
        for widget in self.winfo_children():
            widget.destroy()

        current_tasks = my_tasks.get_tasks()

        self.grid_columnconfigure(0, weight=1)

        for index, task in enumerate(current_tasks):
            task_list_frame = customtkinter.CTkFrame(self)
            task_list_frame.grid(row=index, columnspan=3, sticky='nsew')
            self.columnconfigure(1, weight=1)

            left_frame = customtkinter.CTkFrame(task_list_frame)
            left_frame.grid(row=1, column=0, sticky='ns')

            right_frame = customtkinter.CTkFrame(task_list_frame)
            right_frame.grid(row=1, column=2, padx=10, sticky='nsew')
            task_list_frame.columnconfigure(1, weight=1)

            task_label = customtkinter.CTkLabel(left_frame, text=f"{task['name']}")
            task_label.grid(row=1, sticky='ns')

            task_time_label = customtkinter.CTkLabel(left_frame, text=f"{task['time']}")
            task_time_label.grid(row=2, sticky='ns')

            task_type_label = customtkinter.CTkLabel(left_frame, text=f"{task['type']}")
            task_type_label.grid(row=3, sticky='ns')

            task_description_label = customtkinter.CTkLabel(left_frame, text=f"{task['description']}")
            task_description_label.grid(row=4, pady=20)

            move_up_button = customtkinter.CTkButton(right_frame, text="↑",command=lambda idx=index: self.move_task_up(idx), width=10,height=10)
            move_up_button.grid(row=0, column=0, pady=5)

            move_down_button = customtkinter.CTkButton(right_frame, text="↓",command=lambda idx=index: self.move_task_down(idx), width=10,height=10)
            move_down_button.grid(row=2, column=0, pady=5)

            delete_button = customtkinter.CTkButton(right_frame, text="X",command=lambda idx=index: self.delete_task(idx),  width=10,height=10)
            delete_button.grid(row=1, column=0, pady=5)

    def move_task_up(self, index):
        if index > 0:
            self.my_tasks.tasks[index], self.my_tasks.tasks[index - 1] = self.my_tasks.tasks[index - 1], \
            self.my_tasks.tasks[index]
            self.my_tasks.save_task()  # Save the new order after moving the task
            self.update_task_list()

    def move_task_down(self, index):
        if index < len(self.my_tasks.tasks) - 1:
            self.my_tasks.tasks[index], self.my_tasks.tasks[index + 1] = self.my_tasks.tasks[index + 1], \
            self.my_tasks.tasks[index]
            self.my_tasks.save_task()  # Save the new order after moving the task
            self.update_task_list()

    def delete_task(self, index):
        del self.my_tasks.tasks[index]
        self.my_tasks.save_task()
        self.update_task_list()

# Okno główne


task_frame = TaskFrame(root)
my_tasks = Tasks()
task_creator_frame = TaskCreatorFrame(root, my_tasks)
task_list_frame = TaskListFrame(root, my_tasks)
task_list_frame.grid(row=1, column=0, sticky='nsew', columnspan=3)
my_tasks.load_tasks()
task_list_frame.update_task_list()


root.mainloop()