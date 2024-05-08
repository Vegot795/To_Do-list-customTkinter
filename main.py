import json
import os
import customtkinter
import pickle

root = customtkinter.CTk()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root.geometry("900x600")
root.minsize(300,600)
root.title("Tudu Tudu!")

# Funkcje i klasy
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)




class TaskFrame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(row=0, column=1, sticky='nsew')


        self.title_label = customtkinter.CTkLabel(self, text="Tudu Tudu!", font=("default", 40))
        self.title2_label = customtkinter.CTkLabel(self, text="Your personal task list", font=("default", 20))
        self.title_label.grid(row=0, column=1, sticky='nsew')
        self.title2_label.grid(row=1, column=1, sticky='nsew')

        self.click_button = customtkinter.CTkButton(self, text="Add new task", width=20, command=self.open_task_creator)
        self.click_button.grid(row=3, column=1, sticky='nsew')

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
        self.configure(fg_color="purple")

        self.grid_rowconfigure(4, weight=1)

        else_frame = customtkinter.CTkFrame(self)
        else_frame.grid(row=0,columnspan=3, sticky='nsew')
        else_frame.columnconfigure(0, weight=1)
        else_frame.columnconfigure(2, weight=1)
        else_frame.configure(fg_color='green')

        self.task_name_label = customtkinter.CTkLabel(else_frame, text="Task Name:")
        self.task_name_entry = customtkinter.CTkEntry(else_frame)
        self.task_name_label.grid(column=1, sticky='nsew')
        self.task_name_entry.grid(column=1, sticky='nsew')

        self.task_type_label = customtkinter.CTkLabel(else_frame, text="Task Type:")
        self.task_type_entry = customtkinter.CTkEntry(else_frame)
        self.task_type_label.grid(column=1, sticky='nsew')
        self.task_type_entry.grid(column=1, sticky='nsew')

        #Time/Day/Month values in Task Creator

        TDM_frame = customtkinter.CTkFrame(self)
        TDM_frame.grid(row=1, columnspan=3)
        TDM_frame.configure(fg_color="red")
        TDM_frame.columnconfigure(0, weight=1)
        TDM_frame.columnconfigure(1, weight=1)
        TDM_frame.columnconfigure(2, weight=1)
        TDM_frame.columnconfigure(3, weight=1)
        TDM_frame.columnconfigure(4, weight=1)

        self.task_time_label = customtkinter.CTkLabel(TDM_frame, text="Task Time:")
        self.task_time_entry = customtkinter.CTkEntry(TDM_frame, width=140)
        self.task_time_label.grid(column=1, row=0, padx=10)
        self.task_time_entry.grid(column=1, row=1, padx=10)

        self.task_day_label = customtkinter.CTkLabel(TDM_frame, text='Task Day:')
        self.task_day_entry = customtkinter.CTkComboBox(TDM_frame, width=140)
        self.task_day_label.grid(column=2, row=0, padx=10)
        self.task_day_entry.grid(column=2, row=1, padx=10)

        self.task_month_label = customtkinter.CTkLabel(TDM_frame, text='Task Month:')
        self.task_month_entry = customtkinter.CTkEntry(TDM_frame, width=140)
        self.task_month_label.grid(column=3, row=0, padx=10)
        self.task_month_entry.grid(column=3, row=1, padx=10)

        #Description Values

        description_frame = customtkinter.CTkFrame(self)
        description_frame.grid(row=2, rowspan=2, columnspan=3, sticky='nsew')
        description_frame.columnconfigure(0, weight=1)
        description_frame.columnconfigure(2, weight=1)
        description_frame.rowconfigure(0, weight=1)
        description_frame.rowconfigure(2, weight=1)
        description_frame.configure(fg_color="blue")

        self.task_description_label = customtkinter.CTkLabel(description_frame, text="Task Description:")
        self.task_description_textbox = customtkinter.CTkTextbox(description_frame, height=300, font=("default", 15))
        self.task_description_label.grid(row=0, column=1, sticky='w')
        self.task_description_textbox.grid(sticky='nsew', columnspan=3, rowspan=4)

        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(column=1, sticky='nsew', row=5, pady=10)
        button_frame.configure(fg_color='white')

        self.save_button = customtkinter.CTkButton(button_frame, text="Save Task", width=20, command=self.save_current_task)
        self.save_button.grid()

        self.cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", width=20, command=self.open_main_window)
        self.cancel_button.grid()

    def add_new_task(self):
        task_name = self.task_name_entry.get()
        task_time = self.task_time_entry.get()
        task_day = self.task_day_entry.get()
        task_month = self.task_month_entry.get()
        task_type = self.task_type_entry.get()
        task_description = self.task_description_textbox.get("1.0", "end")

        my_tasks.add_task(task_name, task_time, task_day, task_month, task_type, task_description)
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
                'time': '1 hour',
                'day': 'monday',
                'month': 'may',
                'type': 'Personal',
                'description': 'This is a sample task'
            })
        self.load_tasks()

    def add_task(self, name, time, day, month, type, description):
        new_task = {
            'name': name,
            'time': time,
            'day': day,
            'month': month,
            'type': type,
            'description': description,
        }
        self.tasks.append(new_task)

    def get_tasks(self):
        return self.tasks

    def save_task(self):
        try:
            with open('saves/tasks.json', 'w') as file:
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
            task_list_frame.grid(row=index, columnspan=3, pady=5, sticky='nsew')
            task_list_frame.configure(fg_color="black")
            self.columnconfigure(1, weight=1)
            task_list_frame.configure(width=600, height=800)
            task_list_frame.columnconfigure(1, weight=1)




            left_frame = customtkinter.CTkFrame(task_list_frame)
            left_frame.grid(row=1, columnspan=3, padx=5, sticky='ew')
            left_frame.configure(fg_color="yellow")

            right_frame = customtkinter.CTkFrame(task_list_frame)
            right_frame.grid(row=1, column=2, padx=5, pady=5,  sticky='nsew')
            right_frame.configure(fg_color="red")

            else_frame = customtkinter.CTkFrame(left_frame)
            else_frame.pack(fill='both', expand=True, pady=5, padx=5)
            else_frame.configure(fg_color="green")
            else_frame.columnconfigure(1, weight=1)

            task_label = customtkinter.CTkLabel(else_frame, text=f"{task['name']}", font=("default", 20))
            task_label.grid(column=0, row=0, padx=10, sticky='ew')

            task_type_label = customtkinter.CTkLabel(else_frame, text=f"{task['type']}")
            task_type_label.grid(column=2, row=0, padx=10, sticky='ew')

            TDM_frame = customtkinter.CTkFrame(left_frame)
            TDM_frame.pack(fill='both', expand=True, padx=5, pady=5)
            TDM_frame.configure(fg_color="darkblue")

            task_time_label = customtkinter.CTkLabel(TDM_frame, text=f"{task['time']}")
            task_time_label.grid(column=0, row=0, padx=10, sticky='ew')

            task_day_label = customtkinter.CTkLabel(TDM_frame, text=f"{task['day']}")
            task_day_label.grid(column=1, row=0, padx=10, sticky='ew')

            task_month_label = customtkinter.CTkLabel(TDM_frame, text=f"{task['month']}")
            task_month_label.grid(column=2, row=0, padx=10, sticky='ew')

            description_frame = customtkinter.CTkFrame(left_frame)
            description_frame.pack(fill='both', expand=True, padx=5, pady=5)
            description_frame.configure(fg_color="white")

            task_description_label = customtkinter.CTkLabel(description_frame, text=f"{task['description']}", font=("default",15))
            task_description_label.pack(fill='both', expand=True)

            move_up_button = customtkinter.CTkButton(right_frame, text="↑",command=lambda idx=index: self.move_task_up(idx), width=10,height=10)
            move_up_button.pack(expand=True)

            delete_button = customtkinter.CTkButton(right_frame, text="X",command=lambda idx=index: self.delete_task(idx),  width=10,height=10)
            delete_button.pack(expand=True)

            move_down_button = customtkinter.CTkButton(right_frame, text="↓",command=lambda idx=index: self.move_task_down(idx), width=10,height=10)
            move_down_button.pack(expand=True)


    def move_task_up(self, index):
        if index > 0:
            self.my_tasks.tasks[index], self.my_tasks.tasks[index - 1] = self.my_tasks.tasks[index - 1], \
            self.my_tasks.tasks[index]
            self.my_tasks.save_task()
            self.update_task_list()

    def move_task_down(self, index):
        if index < len(self.my_tasks.tasks) - 1:
            self.my_tasks.tasks[index], self.my_tasks.tasks[index + 1] = self.my_tasks.tasks[index + 1], \
            self.my_tasks.tasks[index]
            self.my_tasks.save_task()
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
